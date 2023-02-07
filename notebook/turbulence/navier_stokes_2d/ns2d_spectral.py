import numpy as np

from .fftw_helper import FFTW_RFFT2D, FFTW_IRFFT2D

_2PI_ = np.pi * 2.0
_CFL_RK4_ = 2.8
_CFL_INCREASE_THRESHOLD_RATIO_ = 0.25
_CFL_TARGET_THRESHOLD_RATIO_ = 0.5
_CFL_REDUCE_THRESHOLD_RATIO_ = 0.75
# this is to resolve the time integral of viscosity term
_MAX_VISCOSITY_FACTOR_EXPONENT_ = np.log(1.0e5)


class NS2dSpectral:
    def __init__(self, Lx, Ly, Mx, My, nu=1e-5, hyper_vis_order=1,
                 use_fftw=True, Mx_da=None, My_da=None, **kwargs):

        if (Mx % 2 != 0) | (My % 2 != 0):
            raise Exception('both Mx and My must be even integers.')
        # fluid parameters
        self.nu = nu
        self.hyper_vis_order = hyper_vis_order
        self.use_fftw = use_fftw

        # physical domain
        self.Lx, self.Ly = Lx, Ly
        self.Mx, self.My = Mx, My
        self.v_x = np.arange(Mx)/Mx * Lx
        self.v_y = np.arange(My)/My * Ly
        self.dx, self.dy = Lx/Mx, Ly/My
        self.mtx_x, self.mtx_y = np.meshgrid(self.v_x, self.v_y)

        # kx, ky: fourier domain
        self.v_kx = np.fft.rfftfreq(Mx) * Mx / Lx * _2PI_
        self.v_ky = np.fft.fftfreq(My) * My / Ly * _2PI_
        self.Mkx, self.Mky = self.v_kx.size, self.v_ky.size
        self.dkx = self.v_kx[1]
        self.dky = self.v_ky[1]

        # 2-D for speed
        mtx_kx, mtx_ky = np.meshgrid(self.v_kx, self.v_ky)
        self.mtx_ikx, self.mtx_iky = 1j*mtx_kx, 1j*mtx_ky
        self.mtx_k2 = mtx_kx**2 + mtx_ky**2
        with np.errstate(divide='ignore'):
            self.mtx_k2_inv = 1.0/self.mtx_k2
        self.mtx_k2_inv[0, 0] = 0.0

        # misc info on fourier factors
        self.kx_max, self.ky_max = np.max(
            np.abs(self.v_kx)), np.max(np.abs(self.v_ky))
        self.k2_max = np.max(self.mtx_k2)

        # de-aliasing
        self.Mx_da = get_fourier_domain_size_for_dealiasing(self.Mx, Mx_da)
        self.My_da = get_fourier_domain_size_for_dealiasing(self.My, My_da)
        self.Mkx_da = np.fft.rfftfreq(self.Mx_da).size
        self.Mky_da = np.fft.fftfreq(self.My_da).size

        # max dt based on viscosity exponential terms from integration by parts
        self.max_dt_viscosity_factor = _MAX_VISCOSITY_FACTOR_EXPONENT_ / \
            (self.nu * self.k2_max ** self.hyper_vis_order)

        # time step
        self.dt_step = np.inf

        # time integration
        self.kw_factor = {}

        # prepare: fft & ifft
        self._prepare_fft(use_fftw,
                          'FFTW_ESTIMATE' if 'FFTW_planner_effort' not in kwargs else kwargs[
                              'FFTW_planner_effort'],
                          None if 'FFTW_threads' not in kwargs else kwargs['FFTW_threads'])

        pass

    def update_dt_step(self, mtx_vor):
        mtx_vor_k = self.fft2d(mtx_vor)
        self.update_dt_step(mtx_vor_k)

    def update_dt_step_k(self, mtx_vor_k):

        dt_curr = self.dt_step

        # Determine the dt based on the clf first
        # clf_number = clf_factor * dt < C_max
        dt_cfl_max = _CFL_RK4_ / self._get_clf_coef(mtx_vor_k)

        if dt_curr > dt_cfl_max * _CFL_REDUCE_THRESHOLD_RATIO_:
            dt_new = dt_cfl_max * _CFL_TARGET_THRESHOLD_RATIO_
        elif dt_curr < dt_cfl_max * _CFL_INCREASE_THRESHOLD_RATIO_:
            dt_new = dt_cfl_max * _CFL_TARGET_THRESHOLD_RATIO_
        else:
            dt_new = dt_curr

        # ensure that dt_new can resolve the viscosity factor
        dt_new = np.minimum(dt_new, self.max_dt_viscosity_factor)

        # check whether the new time step is different
        if np.isclose(dt_new, dt_curr):
            return

        # update required entries.
        print('\n*** time step updated: ', str(dt_new), ' from ', str(dt_curr))
        self.dt_step = dt_new
        print('')

        kw_factor = {}
        kw_factor[0] = np.ones_like(self.mtx_k2)
        kw_factor[1] = np.exp(0.5 * self.dt_step *
                              self.nu * self.mtx_k2 ** self.hyper_vis_order)
        kw_factor[2] = kw_factor[1] ** 2
        self.kw_factor = kw_factor

    def _get_clf_coef(self, mtx_vor_k):
        mtx_psi_k = self.get_psi_k(mtx_vor_k)
        u = self.ifft2d(mtx_psi_k * self.mtx_iky)
        v = self.ifft2d(-mtx_psi_k * self.mtx_ikx)

        C_factor = (np.max(np.abs(u))/self.dx + np.max(np.abs(v))/self.dy)
        return C_factor

    def get_cfl_number(self, mtx_vor_k):
        return self.dt_step * self._get_clf_coef(mtx_vor_k)

    def _prepare_fft(self, use_fftw, FFTW_planner_effort, FFTW_threads):
        if use_fftw:
            self.fftw_rfft2d = FFTW_RFFT2D(
                self.Mx, self.My, planner_effort=FFTW_planner_effort, threads=FFTW_threads)
            self.fftw_irfft2d = FFTW_IRFFT2D(
                self.Mx, self.My, planner_effort=FFTW_planner_effort, threads=FFTW_threads)

            self.fft2d = self.fftw_rfft2d.run
            self.ifft2d = self.fftw_irfft2d.run

            # for non-linear calculation to de-alias with padding
            self.fftw_rfft2d_da = FFTW_RFFT2D(
                self.Mx_da, self.My_da, planner_effort=FFTW_planner_effort, threads=FFTW_threads)
            self.fftw_irfft2d_da = FFTW_IRFFT2D(
                self.Mx_da, self.My_da, planner_effort=FFTW_planner_effort, threads=FFTW_threads)

        else:
            self.fft2d = np.fft.rfft2
            self.ifft2d = np.fft.irfft2

        # pad mask
        self.v_ky_pad_mask = np.full(self.My_da, True)
        Mky_h = get_num_nonnegative_freqs(self.My)
        self.v_ky_pad_mask[Mky_h:self.My_da-Mky_h] = False

    def get_pad(self, mtx_src):
        mtx_pad = np.zeros((self.Mky_da, self.Mkx_da), dtype=mtx_src.dtype)
        mtx_pad[self.v_ky_pad_mask, :self.Mkx] = mtx_src
        return mtx_pad

    def copy_to_pad(self, mtx_src, mtx_dst_with_pad=None):
        if mtx_dst_with_pad is not None:
            mtx_dst_with_pad.fill(0.0)
            mtx_dst_with_pad[self.v_ky_pad_mask, :self.Mkx] = mtx_src
            return None
        else:
            return self.get_pad(mtx_src)

    def take_from_pad(self, mtx_src_with_pad):
        return mtx_src_with_pad[self.v_ky_pad_mask, :self.Mkx]

    def get_deriv_x_k(self, mtx_u_k):
        return self.mtx_ikx*mtx_u_k

    def get_deriv_y_k(self, mtx_u_k):
        return self.mtx_iky*mtx_u_k

    def get_J_k(self, mtx_vor_k):

        mtx_psi_k = self.get_psi_k(mtx_vor_k)

        # Jacobian
        if self.use_fftw:

            J = self.fftw_rfft2d_da.ref_in

            self.copy_to_pad(self.mtx_iky * mtx_psi_k,
                             self.fftw_irfft2d_da.ref_in)
            j1 = self.fftw_irfft2d_da.run()
            self.copy_to_pad(self.mtx_ikx * mtx_vor_k,
                             self.fftw_irfft2d_da.ref_in)
            j2 = self.fftw_irfft2d_da.run()

            np.copyto(J, j1 * j2)

            self.copy_to_pad(self.mtx_ikx * mtx_psi_k,
                             self.fftw_irfft2d_da.ref_in)
            j1 = self.fftw_irfft2d_da.run()
            self.copy_to_pad(self.mtx_iky * mtx_vor_k,
                             self.fftw_irfft2d_da.ref_in)
            j2 = self.fftw_irfft2d_da.run()

            J -= j1 * j2

            J_k_p = self.fftw_rfft2d_da.run()

        else:
            J = self.ifft2d(self.copy_to_pad(self.mtx_iky * mtx_psi_k)) \
                * self.ifft2d(self.copy_to_pad(self.mtx_ikx * mtx_vor_k))
            J -= self.ifft2d(self.copy_to_pad(self.mtx_ikx * mtx_psi_k)) \
                * self.ifft2d(self.copy_to_pad(self.mtx_iky * mtx_vor_k))
            J_k_p = self.fft2d(J)

        J_k = self.take_from_pad(J_k_p)

        return J_k

    def get_L_k(self, dt, mtx_xi_k):

        factor_idx = int(np.round(2.0 * dt/self.dt_step))
        mtx_factor = self.kw_factor[factor_idx]

        mtx_vor_k = mtx_xi_k / mtx_factor
        L_k = - mtx_factor * self.get_J_k(mtx_vor_k)
        return L_k

    def get_psi_k(self, mtx_vor_k):
        return mtx_vor_k * self.mtx_k2_inv

    def get_vor_k(self, mtx_psi_k):
        return mtx_psi_k * self.mtx_k2

    def march_forward_k(self, mtx_vor_k):

        mtx_vor_k_new = rk4(self.get_L_k, 0.0, self.dt_step, mtx_vor_k)
        mtx_vor_k_new /= self.kw_factor[2]

        return mtx_vor_k_new

    def get_psi(self, mtx_vor):
        return self.ifft2d(self.fft2d(mtx_vor) * self.mtx_k2_inv)

    def get_vor(self, mtx_psi):
        return self.ifft2d(self.fft2d(mtx_psi) * self.mtx_k2)

    def get_vor_from_uv(self, mtx_u, mtx_v):
        return self.ifft2d(self.fft2d(mtx_v) * self.mtx_ikx - self.fft2d(mtx_u) * self.mtx_iky)

    def get_uv_from_psi(self, mtx_psi):
        mtx_psi_k = self.fft2d(mtx_psi)
        u = self.ifft2d(mtx_psi_k * self.mtx_iky)
        v = self.ifft2d(-mtx_psi_k * self.mtx_ikx)
        return u, v

    def get_energy(self, mtx_vor_k):
        # since mtx_vor_k is defined in the half domain, we need to inclue
        # additional factor 2.
        E = self.Lx * self.Ly / (self.Mx**2 * self.My ** 2)
        E *= np.sum(np.abs(mtx_vor_k)**2 * self.mtx_k2_inv)
        return E


def get_num_nonnegative_freqs(M):
    return (M-1)//2 + 1


def get_fourier_domain_size_for_dealiasing(M, M_p=None):

    M_k = (M*3-1)//2 + 1  # same as: int(np.ceil(M * 3 / 2 - 0.01))
    if M_p is None:
        return M_k

    if M_p < M_k:
        raise Exception(
            'The dealising domain size must at least larger than ' + str(M_k))
    else:
        return M_p


def rk4(fun, tn, h, yn):
    """Rugge-Kutta 4, single step

    Args:
        fun (func): function in t (float) and y (ND numpy array)
        tn (float): time
        h (float): time step
        yn (n-d array): values as of tn

    Returns:
        n-d array: values as of tn+1
    """
    k1 = fun(tn, yn)
    k2 = fun(tn + h/2.0, yn + h*k1/2.0)
    k3 = fun(tn + h/2.0, yn + h*k2/2.0)
    k4 = fun(tn + h, yn + h*k3)
    yn1 = yn + (1.0/6.0)*h*(k1 + 2*k2 + 2*k3 + k4)
    return yn1

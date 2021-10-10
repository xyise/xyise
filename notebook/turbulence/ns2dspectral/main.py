import warnings
import numpy as np
from numpy.lib.function_base import meshgrid
from scipy.integrate import RK45

from .fft_helper import FFTW_RFFT2D, FFTW_IRFFT2D

_2PI_ = 2.0 * np.pi

class NS2dSpectral:
    def __init__(self, Dx, Dy, Mx, My, nu, hyper_vis_order, dt_step = 0.1, use_fftw = True, **kwargs):

        self.Dx, self.Dy = Dx, Dy
        self.Mx, self.My = Mx, My

        self.nu = nu
        self.hyper_vis_order = hyper_vis_order
        self.use_fftw = use_fftw

        # x, y: physical domain
        self.v_x = np.arange(Mx)/Mx * Dx
        self.v_y = np.arange(My)/My * Dy
        self.mtx_x, self.mtx_y = np.meshgrid(self.v_x, self.v_y)

        # kx, ky: fourier domain
        self.v_kx = np.fft.rfftfreq(Mx) * Mx / Dx * _2PI_
        self.v_ky = np.fft.fftfreq(My) * My / Dy * _2PI_
        self.Mx_k = self.v_kx.size
        self.dkx = self.v_kx[1]
        self.dky = self.v_ky[1]
        
        # de-aliasing
        self.Mx_p = self.Mx * 3 // 2
        self.My_p = self.My * 3 // 2
        
        # 2-D for speed
        mtx_kx, mtx_ky = np.meshgrid(self.v_kx, self.v_ky)
        self.mtx_ikx, self.mtx_iky = 1j*mtx_kx, 1j*mtx_ky
        self.mtx_k2 = mtx_kx**2 + mtx_ky**2
        with np.errstate(divide='ignore'):
            self.mtx_k2_inv = 1.0/self.mtx_k2
        self.mtx_k2_inv[0,0] = 0.0

        self.dt_step = dt_step
        kw_factor = {}
        kw_factor[0] = np.ones_like(self.mtx_k2)
        kw_factor[1] = np.exp(0.5 * dt_step * nu * self.mtx_k2 ** self.hyper_vis_order)
        kw_factor[2] = kw_factor[1] ** 2
        self.kw_factor = kw_factor

        # prepare: fft & ifft
        self._prepare_fft(use_fftw, 
                    'FFTW_ESTIMATE' if 'FFTW_planner_effort' not in kwargs else kwargs['FFTW_planner_effort'], 
                    None if 'FFTW_threads' not in kwargs else kwargs['FFTW_threads'])

    def _prepare_fft(self, use_fftw, FFTW_planner_effort, FFTW_threads):
        if use_fftw:
            self.fftw_rfft2d = FFTW_RFFT2D(self.Mx, self.My, planner_effort=FFTW_planner_effort, threads=FFTW_threads)
            self.fftw_irfft2d = FFTW_IRFFT2D(self.Mx, self.My, planner_effort=FFTW_planner_effort, threads=FFTW_threads)

            self.fft2d = self.fftw_rfft2d.run
            self.ifft2d = self.fftw_irfft2d.run

            # for non-linear calculation with padding
            self.fftw_rfft2d_p = FFTW_RFFT2D(self.Mx_p, self.My_p, planner_effort=FFTW_planner_effort, threads=FFTW_threads)
            self.fftw_irfft2d_p = FFTW_IRFFT2D(self.Mx_p, self.My_p, planner_effort=FFTW_planner_effort, threads=FFTW_threads)

        else:
            self.fft2d = np.fft.rfft2
            self.ifft2d = np.fft.irfft2

        # pad mask
        self.v_ky_pad_mask = np.full(self.My_p, True)
        Myh = self.My//2
        self.v_ky_pad_mask[Myh:self.My_p-Myh] = False

    def get_pad(self, mtx_src):
        mtx_pad = np.zeros((self.My_p, self.Mx_p//2+1), dtype=mtx_src.dtype)
        mtx_pad[self.v_ky_pad_mask,:self.Mx_k] = mtx_src
        return mtx_pad

    def copy_to_pad(self, mtx_src, mtx_dst_with_pad = None):
        if mtx_dst_with_pad is not None:
            mtx_dst_with_pad.fill(0.0)
            mtx_dst_with_pad[self.v_ky_pad_mask,:self.Mx_k] = mtx_src
            return None
        else:
            mtx_pad = np.zeros((self.My_p, self.Mx_p//2+1), dtype=mtx_src.dtype)
            mtx_pad[self.v_ky_pad_mask,:self.Mx_k] = mtx_src
            return mtx_pad

    def take_from_pad(self, mtx_src_with_pad):
        return mtx_src_with_pad[self.v_ky_pad_mask, :self.Mx_k]

    def get_deriv_x_k(self, mtx_u_k):
        return self.mtx_ikx*mtx_u_k
    
    def get_deriv_y_k(self, mtx_u_k):
        return self.mtx_iky*mtx_u_k

    def get_sample_init(self, example = 'cos'):

        if example == 'cos':
            mtx_vor = np.cos(self.mtx_x) * np.cos(self.mtx_y)
        else:
            raise Exception('unknown example')

        return mtx_vor

    def get_J_k(self, mtx_vor_k):

        mtx_psi_k = self.get_psi_k(mtx_vor_k)

        # Jacobian
        if self.use_fftw:
            
            J = self.fftw_rfft2d_p.ref_in

            self.copy_to_pad(self.mtx_iky * mtx_psi_k, self.fftw_irfft2d_p.ref_in)
            j1 = self.fftw_irfft2d_p.run()
            self.copy_to_pad(self.mtx_ikx * mtx_vor_k, self.fftw_irfft2d_p.ref_in)
            j2 = self.fftw_irfft2d_p.run()
            
            np.copyto(J, j1 * j2)

            self.copy_to_pad(self.mtx_ikx * mtx_psi_k, self.fftw_irfft2d_p.ref_in)
            j1 = self.fftw_irfft2d_p.run()
            self.copy_to_pad(self.mtx_iky * mtx_vor_k, self.fftw_irfft2d_p.ref_in)
            j2 = self.fftw_irfft2d_p.run()
            
            J -= j1 * j2

            J_k_p = self.fftw_rfft2d_p.run()

        else:
            J =  self.ifft2d(self.copy_to_pad(self.mtx_iky * mtx_psi_k)) \
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
        L_k = mtx_factor * self.get_J_k(mtx_vor_k)
        return L_k

    def get_psi_k(self, mtx_vor_k):
        return mtx_vor_k * self.mtx_k2_inv
    
    def get_vor_k(self, mtx_psi):
        return mtx_psi * self.mtx_k2

    def march_forward_k(self, mtx_vor_k):

        mtx_vor_k_new = rk4(self.get_L_k, 0.0, self.dt_step, mtx_vor_k)
        mtx_vor_k_new /= self.kw_factor[2]

        return mtx_vor_k_new
    
def rk4(fun, tn, h, yn):
    k1 = fun(tn, yn)
    k2 = fun(tn + h/2.0, yn + h*k1/2.0)
    k3 = fun(tn + h/2.0, yn + h*k2/2.0)
    k4 = fun(tn + h, yn + h*k3)
    yn1 = yn + (1.0/6.0)*h*(k1 + 2*k2 + 2*k3 + k4)
    return yn1







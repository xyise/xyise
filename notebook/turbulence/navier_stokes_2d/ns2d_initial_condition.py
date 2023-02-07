import numpy as np

_2PI_ = np.pi * 2
_PI_ = np.pi


def _get_x_y_mtx(Lx, Ly, Mx, My):
    v_x, v_y = np.arange(Mx)/Mx*Lx, np.arange(My)/My*Ly
    mtx_x, mtx_y = np.meshgrid(v_x, v_y)
    return mtx_x, mtx_y


def _get_kx_ky_mtx(Lx, Ly, Mx, My, real_x=True):

    if real_x:
        v_kx = np.fft.rfftfreq(Mx) * Mx / Lx * _2PI_
    else:
        v_kx = np.fft.fftfreq(Mx) * Mx / Lx * _2PI_
    v_ky = np.fft.fftfreq(My) * My / Ly * _2PI_

    return np.meshgrid(v_kx, v_ky)


def _logistic_der(x): return 4.0 * np.exp(-x) / (1+np.exp(-x))**2
def _bell2(x): return 1.0 / (1 + x**2)


def init_kevin_helmoltz_vorticity_periodic(Lx=_2PI_, Ly=_2PI_,
                                           Mx=256, My=256, amp=0.25, freq=3,
                                           inner_flow_width=_PI_,
                                           transition_width=_2PI_/200):

    mtx_x, mtx_y = _get_x_y_mtx(Lx, Ly, Mx, My)

    # absolute length from the center
    mtx_c = mtx_y - Ly/2.0
    mtx_ca = np.abs(mtx_c)
    g = inner_flow_width / 2.0
    w = transition_width
    mtx_vor = _2PI_ * (1 + amp * np.cos(freq*(mtx_x + _PI_/4*np.sign(mtx_c)))) * \
        _logistic_der((mtx_ca-g)/w) * np.sign(mtx_c)
    mtx_vor -= np.mean(mtx_vor)

    return mtx_vor


def init_random_periodic(Lx=_2PI_, Ly=_2PI_,
                         Mx=256, My=256, amp=1.0, k0=50, dkx=10):

    mtx_x, mtx_y = _get_x_y_mtx(Lx, Ly, Mx, My)
    mtx_kx, mtx_ky = _get_kx_ky_mtx(Lx, Ly, Mx, My, True)
    mtx_k = np.sqrt(mtx_kx**2 + mtx_ky**2)

    mtx_vor_k = np.random.standard_normal(mtx_k.shape) + 1j * np.random.standard_normal(mtx_k.shape)
    # remove mean as vorticity, and remove Nyquists.
    mtx_vor_k[0, 0] = 0.0
    mtx_vor_k[Mx//2, :] = 0.0
    mtx_vor_k[:, My//2] = 0.0

    mtx_vor_k *= _bell2((mtx_k-k0)/dkx)

    mtx_vor = amp * np.fft.irfft2(mtx_vor_k)
    mtx_vor /= np.max(np.abs(mtx_vor))
    mtx_vor -= np.mean(mtx_vor)
    return mtx_vor

# def McWilliams(x, y, Re, **kwargs):
#     """
#     Generates McWilliams vorticity field, see:
#         McWilliams (1984), "The emergence of isolated coherent vortices in turbulent flow"
#     """
#     # Fourier mesh
#     nx = len(x); kx = np.fft.fftfreq(nx, d=1./nx)
#     ny = len(y); ky = np.fft.fftfreq(ny, d=1./ny)
#     nk = ny//2+1

#     # generate variable
#     k2 = kx[:nk]**2 + ky[:,np.newaxis]**2
#     fk = k2 != 0.0

#     # ensemble variance proportional to the prescribed scalar wavenumber function
#     ck = np.zeros((nx, nk))
#     ck[fk] = (np.sqrt(k2[fk])*(1+(k2[fk]/36)**2))**(-1)

#     # Gaussian random realization for each of the Fourier components of psi
#     psih = np.random.randn(nx, nk)*ck+\
#             1j*np.random.randn(nx, nk)*ck

#     # ṃake sure the stream function has zero mean
#     cphi = 0.65*np.max(kx)
#     wvx = np.sqrt(k2)
#     filtr = np.exp(-23.6*(wvx-cphi)**4.)
#     filtr[wvx<=cphi] = 1.
#     KEaux = _spec_variance(filtr*np.sqrt(k2)*psih)
#     psi = psih/np.sqrt(KEaux)

#     # inverse Laplacian in k-space
#     wh = k2 * psi

#     # vorticity in physical space
#     field = np.fft.irfft2(wh)
#     return field

    # def get_sample_init(self, example = 'cos'):

    #     if example == 'cos':
    #         mtx_vor = np.cos(self.mtx_x) * np.cos(self.mtx_y)
    #     elif example == 'random':
    #         mtx_vor = np.random.standard_normal((self.My, self.Mx))
    #         mtx_vor_k = self.fft2d(mtx_vor) * (self.mtx_k2 < np.max(self.mtx_k2)/2.0)
    #         mtx_vor = self.ifft2d(mtx_vor_k)
    #         mtx_vor -= np.mean(mtx_vor)

    #     else:
    #         raise Exception('unknown example')

    #     return mtx_vor
#mtx_vor = McWilliams(ns2d.v_x, ns2d.v_y, 1./ns2d.nu)
#mtx_vor = np.zeros((My, Mx))
#mtx_vor = 0.1*np.random.standard_normal((My, Mx))

# mtx_vor[My//4] = pi2*1 + np.sin(3*ns2d.v_x) * 0.5
# mtx_vor[3*My//4] = -(pi2*1 + np.cos(3*ns2d.v_x) * 0.5)
# mtx_vor_k = ns2d.fft2d(mtx_vor)

# amp = 0.25
# freq = 3
# mtx_u = np.ones((My, Mx))
# mtx_v = amp * np.cos(freq * ns2d.mtx_x)
# mtx_U = np.ones((My,Mx))
# mtx_U = np.sqrt(mtx_u**2 + mtx_v**2)
# mtx_v /= mtx_U
# mtx_u /= mtx_U

# width = pi2/4
# gap = pi2/4 * (1 + 0.01 * np.random.standard_normal((My,Mx)))
# mtx_r = np.abs(ns2d.mtx_y - np.pi)
# mtx_m = 1 - 0.5*(np.tanh((mtx_r-gap)/width)+1)
# mtx_v *= mtx_m
# mtx_u *= mtx_m
# mask = (ns2d.mtx_y < 3*pi2/4 + amp * np.sin(freq*ns2d.mtx_x)) \
#      & (ns2d.mtx_y >= 1*pi2/4 + amp * np.sin(freq*ns2d.mtx_x))
# mtx_v[mask] = amp * np.cos(freq*ns2d.mtx_x[mask])
# mtx_u[mask] = 1.0


#mtx_vor = ns2d.get_vor_from_uv(mtx_u, mtx_v)


# def _spec_variance(ph):
#     # only half the spectrum for real ffts, needs spectral normalisation
#     nx, nk = ph.shape
#     ny = (nk-1)*2
#     var_dens = 2 * np.abs(ph)**2 / (nx*ny)**2
#     # only half of coefs [0] and [nx/2+1] due to symmetry in real fft2
#     var_dens[..., 0] /= 2.
#     var_dens[...,-1] /= 2.

#     return var_dens.sum(axis=(-2,-1))


# def McWilliams(x, y, Re, **kwargs):
#     """
#     Generates McWilliams vorticity field, see:
#         McWilliams (1984), "The emergence of isolated coherent vortices in turbulent flow"
#     """
#     # Fourier mesh
#     nx = len(x); kx = np.fft.fftfreq(nx, d=1./nx)
#     ny = len(y); ky = np.fft.fftfreq(ny, d=1./ny)
#     nk = ny//2+1

#     # generate variable
#     k2 = kx[:nk]**2 + ky[:,np.newaxis]**2
#     fk = k2 != 0.0

#     # ensemble variance proportional to the prescribed scalar wavenumber function
#     ck = np.zeros((nx, nk))
#     ck[fk] = (np.sqrt(k2[fk])*(1+(k2[fk]/36)**2))**(-1)

#     # Gaussian random realization for each of the Fourier components of psi
#     psih = np.random.randn(nx, nk)*ck+\
#             1j*np.random.randn(nx, nk)*ck

#     # ṃake sure the stream function has zero mean
#     cphi = 0.65*np.max(kx)
#     wvx = np.sqrt(k2)
#     filtr = np.exp(-23.6*(wvx-cphi)**4.)
#     filtr[wvx<=cphi] = 1.
#     KEaux = _spec_variance(filtr*np.sqrt(k2)*psih)
#     psi = psih/np.sqrt(KEaux)

#     # inverse Laplacian in k-space
#     wh = k2 * psi

#     # vorticity in physical space
#     field = np.fft.irfft2(wh)
#     return field

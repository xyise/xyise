import numpy as np
import pyfftw



def print_complex_array(a, id):
    for i in range(a.size):
        print("{0}: {1:3d} {2:+8.4f} {3:+8.4f} I".format(id, i, np.real(a[i]), np.imag(a[i])))


def run_me():

    print("Hello, FFTW")

    N = 16

    x = pyfftw.empty_aligned(N, dtype='complex128')
    y = pyfftw.empty_aligned(N, dtype='complex128')
    z = pyfftw.empty_aligned(N, dtype='complex128')

    p_fft = pyfftw.builders.fft(x, planner_effort='FFTW_ESTIMATE')
    p_ifft = pyfftw.builders.ifft(y, planner_effort='FFTW_MEASURE')

    i = np.arange(N)
    # fft run 1
    print('fft run1: x = cos(3 * 2pi * t)')
    x[:] = np.cos(3*2*np.pi*i/N)


    y[:] = p_fft() # this is effectively 'fftw_execute'
    print_complex_array(y, 'y')

    # fft run 2
    print('fft runn 2: x = cos(5 * 2pi * t)')
    x[:] = np.cos(5*2*np.pi*i/N)


    y[:] = p_fft() # this is effectively 'fftw_execute'
    print_complex_array(y, 'y')
    
    # ifft
    print('ifft')
    z[:] = p_ifft()  # this is effectively 'fftw_execute'
    print_complex_array(z * N, 'z * N')
    print('original: x * N')
    print_complex_array(x * N, 'x * N')








if __name__ == '__main__':
    run_me()
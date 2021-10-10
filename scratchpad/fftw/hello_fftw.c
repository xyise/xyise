#include <stdio.h>
#include <math.h>
#include <complex.h>
#include <fftw3.h>

void print_complex_array(fftw_complex* a, int length, double factor, char id[]){
    for (int i = 0; i < length; ++i)
        printf("%s: %3d %+8.4f %+8.4f I\n", id, i, creal(a[i])*factor, cimag(a[i])*factor);
}

int main()
{
    printf("Hello, FFTW\n");
    
    int N = 16;
    fftw_complex *x, *y, *z_N; 
    x = (fftw_complex*) fftw_malloc(sizeof(fftw_complex) * N);
    y = (fftw_complex*) fftw_malloc(sizeof(fftw_complex) * N);
    z_N = (fftw_complex*) fftw_malloc(sizeof(fftw_complex) * N);
    
    fftw_plan p_fft = fftw_plan_dft_1d(N, x, y, FFTW_FORWARD, FFTW_ESTIMATE);
    fftw_plan p_ifft = fftw_plan_dft_1d(N, y, z_N, FFTW_BACKWARD, FFTW_MEASURE);

    int i;
    // fft run 1
    printf("fft run 1: x = cos(3 * 2pi * t)\n");
    for (i = 0; i < N; i++)
        x[i] = cos(3*2*M_PI*i/N);
    
    fftw_execute(p_fft);
    print_complex_array(y, N, 1.0, "y");

    // fft run 2
    printf("fft run 2: x = cos(5 * 2pi * t)\n");
    for (i = 0; i < N; ++i)
        x[i] = cos(5*2*M_PI*i/N);
    
    fftw_execute(p_fft);
    print_complex_array(y, N, 1.0, "y");

    // ifft
    printf("ifft\n");
    fftw_execute(p_ifft);
    print_complex_array(z_N, N, 1.0, "z_N");
    printf("original: x * N\n");
    print_complex_array(x, N, N, "x * N");


    // clean up objects. 
    fftw_destroy_plan(p_fft);
    fftw_destroy_plan(p_ifft);
    fftw_free(x); fftw_free(y); fftw_free(z_N);

    return 0;
}


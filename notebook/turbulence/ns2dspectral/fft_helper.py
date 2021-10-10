import numpy as np
import pyfftw

class FFTW_base():

    def __init__(self):

        self._in = None
        self._out = None
        self._p = None
        
    def run(self, data_in=None, copy=True, data_out=None):

        if data_in is not None:
            np.copyto(self._in, data_in)

        self._out = self._p()
        if data_out is None:
            if copy: 
                return np.array(self._out)
            else:
                return self._out
        else:
            np.copyto(data_out, self._out)
            return data_out

    @property
    def ref_in(self):
        return self._in

    @property    
    def ref_out(self):
        return self._out


class FFTW_RFFT2D(FFTW_base):

    def __init__(self, Nx, Ny, planner_effort='FFTW_ESTIMATE', threads=None):
        FFTW_base.__init__(self)

        self.Nx = Nx
        self.Ny = Ny

        self._in = pyfftw.empty_aligned((Ny, Nx), dtype='float64')        
        self._p = pyfftw.builders.rfft2(self._in, planner_effort=planner_effort, threads=threads)
        self._out = self._p()

class FFTW_IRFFT2D(FFTW_base):

    def __init__(self, Nx, Ny, planner_effort='FFTW_ESTIMATE', threads=None):
        FFTW_base.__init__(self)

        self.Nx = Nx
        self.Ny = Ny

        self._in = pyfftw.empty_aligned((Ny, Nx//2+1), dtype='complex128')        
        self._p = pyfftw.builders.irfft2(self._in, planner_effort=planner_effort, threads=threads)
        self._out = self._p()

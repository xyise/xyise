#%%
import numpy as np
import numba
import random
from numba import jit
import dask
import time


from __future__ import print_function, absolute_import

from numba import cuda
from numba.cuda.random import create_xoroshiro128p_states, xoroshiro128p_uniform_float32
import numpy as np

#%%
@jit
def sum_x(x, n):
    for i in range(n):
        a = 0.0
        for j in range(x.size):
            a += x[j]
    return a

def sum_x_np(x,n):
    for i in range(n):
        a = np.sum(x)
    return a
#%%
x = np.random.standard_normal(1000000)

#%%
n = 1000
%time sum_x(x, n)
%time sum_x_np(x, n)
#%time sum_x.py_func(x, n)

#%%
@jit(nopython=True, parallel=True)
def generate1(nsamples):
    x = np.zeros(nsamples)
    for j in numba.prange(nsamples):
        x[j] = np.random.standard_normal()
    return x

#%%


#@jit(nopython=True)
def core(m: int, rng: np.random.Generator) -> float:

    return np.sum(rng.standard_normal(m))    
    # x = 0.0
    # for j in range(m):
    #     x += rng.standard_normal()
    # return x

#@jit(nopython=True, parallel=True)

def get_streams(n, s):
    #bg = np.random.MT19937(s)
    #bg = np.random.PCG64(s)
    bg = np.random.Philox(s)
    bgs = [bg]
    for j in range(n-1):
        bgs.append(bgs[j].jumped(1))

    return [np.random.Generator(b) for b in bgs]


def run_core(n, m, s):
    bg = np.random.MT19937(s)
    bgs = [bg]
    for j in range(n-1):
        bgs.append(bgs[j].jumped(1))

    np.random.seed(s)
    xn = np.zeros(n)

    delayed_core = dask.delayed(core)

    xn = dask.compute([delayed_core(m, np.random.Generator(bgs[j])) for j in range(n) ])

    return xn

#%%



N = 1000
M = 5000000
S = 123
run_core(N, M, S)





#%time run_core.py_func(N, M)
#%%
np.random.seed(0)
np.random.standard_normal()

#%%
@numba.jit
def monte_carlo_pi(nsamples):
    acc = 0
# %%
%%time
futures = [delayed_monte_carlo_pi(int(4e8)) for i in range(4)]
results = dask.compute(futures)[0]
print(sum(results)/4) # average resuts

# %%
%%time
futures = [delayed_monte_carlo_pi(int(4e8)) for i in range(4)]
results = dask.compute(futures, num_workers=1)[0]
print(sum(results)/4) # average resuts

    for i in range(nsamples):
        x = random.random()
        y = random.random()
        if (x**2 + y**2) < 1.0:
            acc += 1
    return 4.0 * acc / nsamples

#%%
@jit(nopython=True, parallel=True)
def generate(nsamples):
    x = np.zeros(nsamples)
    for j in numba.prange(100):
        x += np.random.standard_normal(nsamples)

    return x

#%%
@jit(nopython=True, parallel=True)
def generate1(nsamples):
    x = np.zeros(nsamples)
    for j in numba.prange(nsamples):
        x[j] = np.random.standard_normal()
    return x

# %%
def monte_carlo_pi_me(nsamples):
    acc = 0
    for i in range(nsamples):
        x = random.random()
        y = random.random()
        if (x**2 + y**2) < 1.0:
            acc += 1
    return 4.0 * acc / nsamples

# %%
@jit(nopython=True)
def go_fast(a): # Function is compiled to machine code when called the first time
    trace = 0
    # assuming square input matrix
    for i in range(a.shape[0]):   # Numba likes loops
        trace += np.tanh(a[i, i]) # Numba likes NumPy functions
    return a + trace              # Numba likes NumPy broadcasting

# %%
@jit(nopython=True)
def zero_clamp(x, threshold):
    # assume 1D array.  See later in this notebook for more general function
    out = np.empty_like(x)
    for i in range(out.shape[0]):
        if np.abs(x[i]) > threshold:
            out[i] = x[i]
        else:
            out[i] = 0
    return out        

# %%
SQRT_2PI = np.sqrt(2 * np.pi)

@jit(nopython=True, parallel=True)
def gaussians(x, means, widths):
    '''Return the value of gaussian kernels.
    
    x - location of evaluation
    means - array of kernel means
    widths - array of kernel widths
    '''
    n = means.shape[0]
    result = np.exp( -0.5 * ((x - means) / widths)**2 ) / widths
    return result / SQRT_2PI / n


# %%

@jit(nopython=True, parallel=True)
def kde(x, means, widths):
    '''Return the value of gaussian kernels.
    
    x - location of evaluation
    means - array of kernel means
    widths - array of kernel widths
    '''
    n = means.shape[0]
    result = np.exp( -0.5 * ((x - means) / widths)**2 ) / widths
    return result.mean() / SQRT_2PI

kde_nothread = jit(nopython=True)(kde.py_func)

# %%
# Serial version
@jit(nopython=True)
def monte_carlo_pi_serial(nsamples):
    acc = 0
    for i in range(nsamples):
        x = random.random()
        y = random.random()
        if (x**2 + y**2) < 1.0:
            acc += 1
    return 4.0 * acc / nsamples

# Parallel version
@jit(nopython=True, parallel=True)
def monte_carlo_pi_parallel(nsamples):
    acc = 0
    # Only change is here
    for i in numba.prange(nsamples):
        x = random.random()
        y = random.random()
        if (x**2 + y**2) < 1.0:
            acc += 1
    return 4.0 * acc / nsamples

# %%
import dask
import dask.delayed

@jit(nopython=True, nogil=True)
def monte_carlo_pi(nsamples):
    acc = 0
    for i in range(nsamples):
        x = random.random()
        y = random.random()
        if (x**2 + y**2) < 1.0:
            acc += 1
    return 4.0 * acc / nsamples

print(monte_carlo_pi(int(1e6)))
#%%
delayed_monte_carlo_pi = dask.delayed(monte_carlo_pi)

# %%
%%time
futures = [delayed_monte_carlo_pi(int(4e8)) for i in range(4)]
results = dask.compute(futures)[0]
print(sum(results)/4) # average resuts

# %%
%%time
futures = [delayed_monte_carlo_pi(int(4e8)) for i in range(4)]
results = dask.compute(futures, num_workers=1)[0]
print(sum(results)/4) # average resuts

# %%

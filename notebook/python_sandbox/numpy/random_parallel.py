#%%
import numpy as np
import time
np.__version__

#%%
def long_calc(n, rng: np.random.Generator):

    x = rng.standard_normal(n)
    for j in range(400):
        y = np.exp(x)
    
    return np.mean(y)
#%%
N = 1000000
my_rng = np.random.Generator(np.random.MT19937(123))
for t in range(4):
    st = time.time()
    r = long_calc(N, my_rng)
    et = time.time()
    print(str(r) + ':' + str(et - st))

##

#%%
bgs_mt = [np.random.MT19937(123)]
for j in range(7):
    bgs_mt.append(bgs_mt[j].jumped())
rngs_mt = [np.random.Generator(bg) for bg in bgs_mt]

#%%
N = 1000000
for t in range(4):
    st = time.time()
    r = long_calc(N, rngs_mt[t])
    et = time.time()
    print(str(r) + ':' + str(et - st))



#%%
from joblib import Parallel, delayed

#%%
st = time.time()
Parallel(n_jobs=4)(
    delayed(long_calc)(N, rng) for rng in rngs_mt)

et = time.time()
print(et-st)

#%%

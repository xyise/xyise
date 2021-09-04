#%%
import numpy as np
import time

def run_me():

    n_sim = 100
    n_vs = 10000

    start = time.time()
    for n in range(10):
        gen_vec(n_sim, n_vs)
    end = time.time()
    print(end - start)

    start = time.time()
    for n in range(10):
        gen_novec(n_sim, n_vs)
    end = time.time()
    print(end - start)

def gen_vec(n_sim, n_vs):
    x = np.random.randn(n_sim, n_vs)
    return x

def gen_novec(n_sim, n_vs):
    x = np.array([np.random.randn(n_vs) for n in range(n_sim)])
    return x

#%%
gen_novec(10, 5).shape

#%%
if __name__ == '__main__':
    run_me()



#%%

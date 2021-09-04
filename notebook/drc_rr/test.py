import numpy as np
# local files
import random_repeat as rr

def test_me():
    rss = np.random.SeedSequence(1234)

    kw_rv_n = {str(i):rr.RandomVariables('normal') 
                for i in range(20000)}
    kw_rv_mm = {'mm'+str(i):rr.RandomVariables('multivariate_normal',
                {'mean':[1,2], 'cov':[[1,0.5],[0.5,1]]})
                for i in range(3,0,-1)}
    kw_rv = {**kw_rv_n, **kw_rv_mm}
    rrpr = rr.RandomRepeat(rss, 100000, kw_rv)

    print('done')

if __name__ == '__main__':
    test_me()
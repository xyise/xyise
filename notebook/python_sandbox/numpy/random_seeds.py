#%%
import numpy as np
import pickle

def main():
    nblock = 100000 * 1000
    rs = np.random.RandomState(1)
    np.random.seed(0)
    for i in range(5):
        s = rs.get_state()
        with open('s' + str(i) + '.pkl', 'wb') as f:
            pickle.dump(s, f, pickle.HIGHEST_PROTOCOL)
        z = rs.randn(nblock)
        print(z[0:5])

    for i in range(5):
        with open('s' + str(i) + '.pkl', 'rb') as f:
            s = pickle.load(f)
        rs.set_state(s)
        z = rs.randn(nblock)
        print(z[0:5])

if __name__ == '__main__':
    main()
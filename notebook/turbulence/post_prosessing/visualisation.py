import numpy as np
import matplotlib.pyplot as plt

def make_image_2d(mtx_data: np.array, v_x, v_y, 
        symmetric_color = True, cm='RdBu_r'):

    if symmetric_color:
        vmax = np.max(np.abs(mtx_data))
        vmin = -vmax
    else:
        vmax = np.max(mtx_data)
        vmin = np.min(mtx_data)

    plt.pcolormesh(v_x, v_y, mtx_data, cmap=cm, vmin = vmin, vmax = vmax, shading='gouraud')
    #plt.imshow(mtx_data, cmap=cm, vmin = vmin, vmax = vmax, interpolation='gaussian')
    #plt.imshow(mtx_data, cmap=cm)
    plt.axis('scaled')

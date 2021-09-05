"""numba files

__author__ = xyise
__copyright__ = Copyright 2021
"""


import numpy as np
from numba import jit, njit

# scalar digitize function
# source codes taken directly from https://github.com/numba
# decorations are added by the author
@njit(fastmath=True,cache=True)
def digitize_scalar_nb(x, bins, right = True):
    # bins are monotonically-increasing
    n = len(bins)
    lo = 0
    hi = n

    if right:
        if np.isnan(x):
            # Find the first nan (i.e. the last from the end of bins,
            # since there shouldn't be many of them in practice)
            for i in range(n, 0, -1):
                if not np.isnan(bins[i - 1]):
                    return i
            return 0
        while hi > lo:
            mid = (lo + hi) >> 1
            if bins[mid] < x:
                # mid is too low => narrow to upper bins
                lo = mid + 1
            else:
                # mid is too high, or is a NaN => narrow to lower bins
                hi = mid
    else:
        if np.isnan(x):
            # NaNs end up in the last bin
            return n
        while hi > lo:
            mid = (lo + hi) >> 1
            if bins[mid] <= x:
                # mid is too low => narrow to upper bins
                lo = mid + 1
            else:
                # mid is too high, or is a NaN => narrow to lower bins
                hi = mid

    return lo



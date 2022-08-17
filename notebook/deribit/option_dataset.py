import collections
from datetime import datetime
from inspect import CO_OPTIMIZED
from multiprocessing.util import is_exiting
from matplotlib import is_interactive
import numpy as np
import pandas as pd
from scipy import interpolate, stats


c_expiration_datetime = 'expiration_datetime'
c_underlying_price = 'underlying_price'
c_expiration_timestamp = 'expiration_timestamp'
c_option_type = 'option_type'
c_strike = 'strike'
c_delta = 'delta'
c_mark_iv = 'mark_iv'


def get_delta_id_df(deltas = [0.25, 0.1]) -> pd.DataFrame:

    p2str100 = lambda x: str(int(x*100 + 1e-6))

    deltas_asc = np.sort(deltas)
    deltas_des = deltas_asc[::-1]
    tags_put = [p2str100(d) + 'P' for d in deltas_asc]
    tags_call = [p2str100(d) + 'C' for d in deltas_des]

    tags = np.hstack((tags_put, 'ATMF', tags_call))

    vals_call = np.hstack((1.0 - deltas_asc, 0.5, deltas_des))
    vals_put = vals_call[::-1]

    return pd.DataFrame({'name':tags, 'call':vals_call, 'put': vals_put}).set_index('name')

# Let's create a class around the dataframe (so that we can do more). 
class OptionDataset:

    def __init__(self, df_md: pd.DataFrame):
        
        # before any operations, let's sort the dataframe by expiration and strike for convenience
        # this will sort change the ordering of the input data
        df_md.sort_values([c_expiration_timestamp, c_strike], inplace=True)
        self.df_md = df_md
        
        # group by expiry
        self.kw_md = {ex:df_ex for ex, df_ex in df_md.groupby(c_expiration_timestamp)}
        
        # for convenience, store index to timestep mapping
        self.expiration_timestamps: list = list(self.kw_md)
        
        # set forwards: keep the forward price by taking average for each expiry
        self.ds_fwd: pd.Series = df_md.groupby(c_expiration_timestamp)[c_underlying_price].mean()
        
    def __len__(self):
        return len(self.kw_md)
    
    def __getitem__(self, position: int) -> dict:
        return self.kw_md[self.expiration_timestamps[position]]


def timestamp2datetime(ts):
    return datetime.fromtimestamp(ts/1000.)


def linear_interp_flat_extrap(x: np.array, y: np.array):

    i_s = np.argsort(x)
    x_s, y_s = x[i_s], y[i_s]

    return interpolate.interp1d(x_s, y_s, bounds_error=False, 
        fill_value=(y_s[0], y_s[-1]), assume_sorted=True)

VolDelta = collections.namedtuple('VolDelta', ['delta', 'strike', 'vol', 'extrapolated'])


def get_vol_at_deltas(df_c: pd.DataFrame, deltas: np.array, interp_extrap = linear_interp_flat_extrap):
    """_summary_

    Args:
        deltas (np.array): deltas of calls
    """

    get_ie_func = lambda c_x, c_y: interp_extrap(df_c[c_x].to_numpy(), df_c[c_y].to_numpy())

    strikes = get_ie_func(c_delta, c_strike)(deltas)
    ivs = get_ie_func(c_strike, c_mark_iv)(strikes)

    extrapolated = (deltas < df_c[c_delta].min()) | (deltas > df_c[c_delta].max())

    return VolDelta(deltas, strikes, ivs, extrapolated)
    
    

    
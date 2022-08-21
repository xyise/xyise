import collections
from datetime import datetime
import numpy as np
import pandas as pd
from scipy import interpolate, stats
from matplotlib import cm
import matplotlib.pyplot as plt
import itertools


c_expiration_datetime = 'expiration_datetime'
c_underlying_price = 'underlying_price'
c_expiration_timestamp = 'expiration_timestamp'
c_option_type = 'option_type'
c_strike = 'strike'
c_delta = 'delta'
c_mark_iv = 'mark_iv'
c_mark_price = 'mark_price'

c_volatility = 'volatility'
c_price = 'price'
c_extrapolated = 'extrapolated'


# utils
def linear_interp_flat_extrap(x: np.array, y: np.array, extrapolate=True):

    i_s = np.argsort(x)
    x_s, y_s = x[i_s], y[i_s]

    fill_value = (y_s[0], y_s[-1]) if extrapolate else (np.nan, np.nan) 

    return interpolate.interp1d(x_s, y_s, bounds_error=False, 
        fill_value=fill_value, assume_sorted=True)

def get_tenor2delta(deltas: np.array) -> pd.DataFrame:

    f2str100 = lambda x: str(round(x*100))

    deltas_asc = np.sort(deltas)
    deltas_des = deltas_asc[::-1]
    tenors_p = [f2str100(d) + 'P' for d in deltas_asc]
    tenors_c = [f2str100(d) + 'C' for d in deltas_des]

    tenors = np.hstack((tenors_p, 'ATMF', tenors_c))

    vals_call = np.hstack((1.0 - deltas_asc, 0.5, deltas_des))
    vals_put = vals_call - 1.0

    return pd.DataFrame({'tenor':tenors, 'call':vals_call, 'put': vals_put}).set_index('tenor')



def timestamp2datetime(ts):
    return datetime.fromtimestamp(ts/1000.)



# Let's create a class around the dataframe (so that we can do more). 
class OptionDataset:

    def __init__(self, df_md: pd.DataFrame):
        
        # before any operations, let's sort the dataframe by expiration and strike for convenience
        # this will sort change the ordering of the input data
        df_md.sort_values([c_expiration_timestamp, c_strike], inplace=True)
        self.df_md = df_md
        
        # group by expiry, then by option type
        self.kw_md = {ex:{ot:df_ot for ot, df_ot in df_ex.groupby(c_option_type)}
            for ex, df_ex in df_md.groupby(c_expiration_timestamp)}
        
        # for convenience, store index to timestep mapping
        self.expiration_timestamps: list = list(self.kw_md)
        
        # set forwards: keep the forward price by taking average for each expiry
        self.ds_fwd: pd.Series = df_md.groupby(c_expiration_timestamp)[c_underlying_price].mean()
        
        # market data by delte tenors, risk-reversals/butterflies
        # set by set_md_by_delta
        self.interp_extrap_delta_tenors = None
        self.df_tenor2delta = None
        self.df_md_tenor = None # by tenors (10P, 25P, ATMF, 25C, 10C)
        self.df_md_rb = None # risk reversal & butterfly

    def __len__(self):
        return len(self.kw_md)
    
    def __getitem__(self, position: int) -> dict:
        return self.kw_md[self.expiration_timestamps[position]]

    def set_md_in_delta(self, 
                interp_extrap = linear_interp_flat_extrap, 
                tenor_deltas: np.array = np.array([0.25, 0.1])):

        self.interp_extrap_delta_tenors = interp_extrap
        self.df_tenor2delta = get_tenor2delta(tenor_deltas)
        # run each expiry and collect them
        df_md_tenor = {ex_ts:self._get_vol_by_tenor(ex_ts) for ex_ts in self.kw_md}
        
        # index: expiration_timestamp, columns: (fields, tenors) where fields = (strike, volatility, extrapolated)
        self.df_md_tenor = pd.concat(df_md_tenor).unstack()
        self.df_md_tenor.index.name = c_expiration_timestamp

        # create in terms of rr and fly. 
        # vol & extrapolation flags
        # v: vol, e: extrapolated
        kw_v, kw_e = {}, {}
        df_vol = self.df_md_tenor[c_volatility]
        df_ext = self.df_md_tenor[c_extrapolated] 

        tenor_deltas_str = [str(round(d*100)) for d in np.sort(tenor_deltas)[::-1]]
        A_str = df_vol.columns[len(tenor_deltas)]
        ds_av = df_vol[A_str]
        ds_ae = df_ext[A_str]

        kw_v[A_str] = ds_av
        kw_e[A_str] = ds_ae

        for tds in tenor_deltas_str:
            C_str, P_str = (tds + 'C'), (tds + 'P')
            ds_cv, ds_pv = df_vol[C_str], df_vol[P_str]
            ds_ce, ds_pe = df_ext[C_str], df_ext[P_str]

            RR_str, FLY_str = (tds + 'RR'), (tds + 'FLY')
            kw_v[RR_str] = ds_cv - ds_pv
            kw_v[FLY_str] = (ds_cv + ds_pv)/2.0 - ds_av
            kw_e[RR_str] = ds_ce | ds_pe
            kw_e[FLY_str] = ds_ce | ds_pe | ds_ae
        
        self.df_md_rb = pd.concat({c_volatility:pd.DataFrame(kw_v), c_extrapolated:pd.DataFrame(kw_e)},
                            axis=1)
        
    def get_volatility_summary(self):
        
        df_v = pd.concat((self.ds_fwd, self.df_md_tenor[c_volatility], self.df_md_rb[c_volatility]), axis=1)
        # use date
        idx_name = 'Expiry'
        df_v.index = [timestamp2datetime(ts) for ts in df_v.index]
        df_v.index.name = idx_name
        df_v.rename({c_underlying_price:'Forward'}, axis=1, inplace=True)
        
        # extrapolated data information
        df_et, df_er = self.df_md_tenor[c_extrapolated].stack(), self.df_md_rb[c_extrapolated].stack()
        kw = {}
        for ts, name in list(df_et[df_et].index) + list(df_er[df_er].index):
            kw.setdefault(ts, []).append(name)
        ds_extraps = pd.Series(kw)
        ds_extraps.index = [timestamp2datetime(ts) for ts in ds_extraps.index]

        return df_v, ds_extraps

    def _get_vol_by_tenor(self, expiration_timestamp): 
        
        df_c = self.kw_md[expiration_timestamp]['call']
        deltas_md = df_c[c_delta].to_numpy()
        strikes_md = df_c[c_strike].to_numpy()
        vols_md = df_c[c_mark_iv].to_numpy()

        deltas_tnr = self.df_tenor2delta['call']

        # interpolate
        strikes_tnr = self.interp_extrap_delta_tenors(deltas_md, strikes_md)(deltas_tnr)
        vols_tnr = self.interp_extrap_delta_tenors(deltas_md, vols_md)(deltas_tnr)
        
        extrapolated = (deltas_tnr < deltas_md.min()) | (deltas_tnr > deltas_md.max())

        return pd.DataFrame(
            index = self.df_tenor2delta.index,
            data={c_strike:strikes_tnr, c_volatility:vols_tnr, c_extrapolated:extrapolated})

    def get_md_rectangular(self, num_strikes, to_extrapolate = False, extra_pad_ratio = 1.1):

        K_min, K_max = self.get_strike_tenor_range()
        K_rec = np.linspace(K_min/extra_pad_ratio, K_max*extra_pad_ratio, num_strikes)

        # calls only
        kw_c = {ex_ts:kw['call'] for ex_ts, kw in self.kw_md.items()}

        iv_rec, delta_rec = [], []
        for ex_ts, df_c in kw_c.items():
            iv = linear_interp_flat_extrap(df_c[c_strike].to_numpy(), df_c[c_mark_iv].to_numpy(), to_extrapolate)(K_rec)
            delta = linear_interp_flat_extrap(df_c[c_strike].to_numpy(), df_c[c_delta].to_numpy(), to_extrapolate)(K_rec)
            iv_rec.append(iv), delta_rec.append(delta)

        ts_rec = np.array([ts for ts in kw_c])
        iv_rec, delta_rec = np.array(iv_rec), np.array(delta_rec)
        
        return K_rec, ts_rec, {c_volatility:iv_rec, c_delta:delta_rec}

    def get_md_call(self) -> pd.DataFrame:
        df_c = self.df_md[self.df_md[c_option_type] == 'call']
        return df_c

    def get_strike_tenor_range(self):
        df_strikes_by_tenors = self.df_md_tenor[c_strike]
        K_min, K_max = df_strikes_by_tenors.min().min(), df_strikes_by_tenors.max().max()
        return K_min, K_max


# this is just a plotting tool collection. 

class PlotTool:

    datetime_format = '%Y-%m-%d %H:%M:%S'

    def __init__(self, ods: OptionDataset, expiration_timestamp):

        self.data_set = ods
        self.expiration_timestamp = expiration_timestamp

        # data by strikes
        kw_md_ts = ods.kw_md[expiration_timestamp]
        self.df_c, self.df_p = kw_md_ts['call'], kw_md_ts['put']
        self.fwd = ods.ds_fwd[expiration_timestamp]

        # data by tenor
        self.df_tenor2delta = ods.df_tenor2delta
        self.ds_md_tenor = ods.df_md_tenor.loc[expiration_timestamp]
        self.ds_md_rb = ods.df_md_rb.loc[expiration_timestamp]

        # strike tenors including forward
        self.num_deltas = ods.df_tenor2delta.shape[0]//2
        self.tenor2color = self._get_tenor2color_map(self.num_deltas)
        self.tenor2strike = {k:v for k,v in itertools.chain(self.ds_md_tenor[c_strike].items(), [('Forward', self.fwd)])}

    def _get_tenor2color_map(self, num_deltas=2):
        cmap = cm.get_cmap('jet')

        # define based on the number of deltas
        if num_deltas == 2:
            return {k:v for k,v in itertools.chain(
                            zip(['10P', '25P', 'ATMF', '25C', '10C'], cmap(np.linspace(0.0, 1.0, 5))), 
                            [('Forward', 'k')])}

    def plot(self):
        df_c, df_p = self.df_c, self.df_p
        md_count = df_c.shape[0]

        # set the common xlim. 
        ds_tenor2strike = self.ds_md_tenor[c_strike]
        max_tenor_strike = ds_tenor2strike.max()
        xlim = [0.0, max_tenor_strike*1.1]

        ####################
        # price plot
        ####################

        ax1 = plt.subplot(311)

        ylim_idx = np.clip(np.searchsorted(df_c[c_strike], max_tenor_strike, side='left'), 0, md_count-1)
        ylim_max = np.maximum(df_c[c_mark_price].iloc[ylim_idx], df_p[c_mark_price].iloc[ylim_idx])


        line_c, = plt.plot(df_c[c_strike], df_c[c_mark_price], '.-', lw=2, ms=12, label='call')
        line_p, = plt.plot(df_p[c_strike], df_p[c_mark_price], '.-', lw=2, ms=12, label='put')
        self._add_vertical_lines_at_strike_tenors(ax1)
        plt.legend(), plt.xlabel('strike'), plt.ylabel('option price')
        plt.xlim(xlim), plt.ylim(0.0, ylim_max)
        plt.title('as of ' + timestamp2datetime(self.expiration_timestamp).strftime(self.datetime_format))

        ######################
        # implied volatility
        ######################
        ax2 = plt.subplot(312, sharex=ax1)
        plt.plot(df_c[c_strike], df_c[c_mark_iv], '.-', ms=12, c=line_c.get_color(), 
                    markerfacecolor=line_p.get_color(), markeredgecolor=line_p.get_color(), label='call & put')
        self._add_vertical_lines_at_strike_tenors(ax2)
        plt.legend(), plt.xlabel('strike'), plt.ylabel('implied volatility')
        pass

        ####################
        # delta
        ######################
        ax3 = plt.subplot(313, sharex=ax1)

        line, = plt.plot(df_c[c_strike], df_c[c_delta], '.-', lw=2, ms=12, label='call')
        line, = plt.plot(df_p[c_strike], df_p[c_delta], '.-', lw=2, ms=12, label='put')

        self._add_horizontal_lines_at_strike_deltas(ax3)
        self._add_vertical_lines_at_strike_tenors(ax3)
        self._set_and_color_yticklabels_at_strike_deltas(ax3)
        plt.grid(axis='y', zorder=-100)
        plt.legend(), plt.xlabel('strike'), plt.ylabel('delta')


    def _add_vertical_lines_at_strike_tenors(self, ax: plt.Axes):
        """to add vertical lines at each delta points and forwards

        Args:
            ax (plt.Axes): _description_
        """

        plt.sca(ax)
        for tenor, strike in self.tenor2strike.items():
            plt.axvline(strike, color=self.tenor2color[tenor], ls='--', zorder=-100, lw=2, label=tenor)



    def _add_horizontal_lines_at_strike_deltas(self, ax: plt.Axes):

        plt.sca(ax)

        ds_delta_tenors_p = self.df_tenor2delta['put'][:(self.num_deltas+1)]
        ds_delta_tenors_c = self.df_tenor2delta['call'][-(self.num_deltas+1):]

        for tenor, delta in itertools.chain(ds_delta_tenors_p.items(), ds_delta_tenors_c.items()):
            strike = self.tenor2strike[tenor]
            plt.hlines(delta, xmin=0, xmax=strike, color=self.tenor2color[tenor],
                        ls='--', zorder=-100, lw=2)
            
            plt.plot([strike], [delta], 'o', color='k', markerfacecolor='none', lw=2, ms=16, zorder=-5)

    def _set_and_color_yticklabels_at_strike_deltas(self, ax: plt.Axes):

        plt.sca(ax)
        # put ticks
        yticks = np.hstack([1., self.df_tenor2delta['call'].to_numpy(), 0.0,
                                 self.df_tenor2delta['put'], -1])
        plt.yticks(yticks)
        for i, (tnr, delta) in enumerate(self.df_tenor2delta['call'].items()):
            idx_tick = 1 + i
            ax.get_yticklabels()[idx_tick].set_color(self.tenor2color[tnr])
            idx_tick = yticks.size//2 + 1 + i
            ax.get_yticklabels()[idx_tick].set_color(self.tenor2color[tnr])

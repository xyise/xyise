import pandas as pd
import numpy as np
from netCDF4 import Dataset
from datetime import datetime, timedelta
from et_utils import *

class TemperatureData:
    def __init__(self, year: int, month: int, lon: np.ndarray, lat: np.ndarray, celsius: np.ndarray, in_deg = True):
        self.year = year
        self.month = month
        self.lon = lon
        self.lat = lat
        self.celsius = celsius
        self.in_deg = in_deg
    
    def get_data(self):
        return self.lon, self.lat, self.celsius
    
    def create_with_valid_data(self):
        idx_v = ~np.isnan(self.celsius)
        return TemperatureData(self.year, self.month, self.lon[idx_v], self.lat[idx_v], self.celsius[idx_v])

    def remove_data(self, indices_to_remove):
        idx_v = np.full(self.lon.shape, True)
        idx_v[indices_to_remove] = False
        return TemperatureData(self.year, self.month, self.lon[idx_v], self.lat[idx_v], self.celsius[idx_v])

    def num_data(self):
        return len(self.lon)

    def get_rectangular_data(self, M_lon, M_lat):
        return (x.reshape(M_lat, M_lon) for x in (self.lon, self.lat, self.celsius)) 

class SeaDataset:

    large_negative = -100.0

    def __init__(self, sea_data_file):

        sea_data = Dataset(sea_data_file, mode='r')
        
        # original ordinates
        lon1 = sea_data.variables['lon'][:].data
        lon1 = np.where(lon1 >= 180, -360+lon1, lon1) # put them into -180 to 180
        lon1 = np.roll(lon1, 90) # to make it increasing
        lat1 = sea_data.variables['lat'][:].data[::-1] # reverse to make it increasing

        # ordinates (expanded)
        lon, lat = np.meshgrid(lon1, lat1)
        lon, lat = lon.flatten(), lat.flatten()

        # data by month
        months = np.array([datetime(1800,1,1) + timedelta(days=t) for t in sea_data.variables['time'][:].data])        
        month2index = {m:i for i,m in enumerate(months)}

        tmpr2 = sea_data.variables['sst'][:].data # data are stored in 3d (month, lat, lon)

        tmpr = []
        for i in range(len(months)):
            mt = tmpr2[i] # data are
            mt = mt[::-1] # reverse in lat
            mt = np.roll(mt, 90, axis=1) # roll in lon
            mt = mt.flatten() # make it 1D
            mt = np.where(mt < self.large_negative, np.nan, mt) # set very negative into nan
            tmpr.append(mt)

        self.lon, self.lat = lon, lat
        self.M_lon, self.M_lat = lon1.size, lat1.size
        self.month2index = month2index
        self.temperature_by_month = tmpr

    def month_data(self, year: int, month: int) -> TemperatureData:
        idx = self.month2index[datetime(year, month, 1)]
        return TemperatureData(year, month, self.lon, self.lat, self.temperature_by_month[idx])
        

class LandDataset:

    missing_value = -9999

    def __init__(self, land_inv_file, land_country_file, land_dat_file, pkl_file = None, read_from_pickle=False):
        # station information, to get the longitude and latitude data
        df_stn_md = get_stn_metadata(land_inv_file, land_country_file)

        if not read_from_pickle:
            print('reading from ' + land_dat_file)
            df = get_data(land_dat_file)
            if pkl_file is not None:
                df.to_pickle(pkl_file)
        else:
            print('read from ' + pkl_file)
            df = pd.read_pickle(pkl_file)

        self.df_dat: pd.DataFrame = df
        self.df_stn_md: pd.DataFrame = df_stn_md

    def month_data(self, year:int , month: int):
        df_y = self.df_dat[self.df_dat['year'] == year]
        month_col = 'VALUE' + str(month)
        df_m = df_y[['country_code', 'station', 'year', month_col]].copy()
        df_m[month_col].replace(self.missing_value, np.nan, inplace=True)
        # merge with station data
        df_m = pd.merge(df_m, self.df_stn_md, how='left', on='station')
        # value should be scaled by 100
        return TemperatureData(year, month, df_m['lon'].to_numpy(), df_m['lat'].to_numpy(), df_m[month_col].to_numpy()/100.0)


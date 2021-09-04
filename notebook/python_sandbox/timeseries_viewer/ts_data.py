import pandas as pd
import time

def get_timestamp(dt):
    return int(time.mktime(dt.timetuple()))

class TimeSeriesData: 

    def __init__(self, 
                csv_files, 
                tag = None, 
                append_file_name = False,
                date_column = 'Date',
                date_format = '%Y/%m/%d',
                csv_sep=','):

        self.df_ts = None
        self.tag = '' if tag == None else tag + ':'
        self.date_column = date_column
        self.date_format = '%Y/%m/%d'
        self.csv_sep = csv_sep

    
    def _read_csv(self, file):
        df = pd.read_csv(file, sep=self.csv_sep)
        adt = pd.to_datetime(df[self.date_column], format=self.date_format)
        df[self.date_column] = [dt.timestamp() for dt in adt]
        df.set_index(self.date_column, inplace=True)

        return df


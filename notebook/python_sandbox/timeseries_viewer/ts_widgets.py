
import pyqtgraph as pg
import datetime
import time


class TimeAxisItem(pg.AxisItem):
    def __init__(self, text='Date', format='%Y/%m/%d', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text=text
        self.format=format
        self.setLabel(text=text, units=None)
        self.enableAutoSIPrefix(False)

    def tickStrings(self, values, scale, spacing):
#        return [datetime.datetime.fromtimestamp(value).strftime("%H:%M") for value in values]
        return [datetime.datetime.fromtimestamp(value).strftime(self.format) for value in values]
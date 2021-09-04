#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 22:07:20 2020

@author: youngsuk
"""

#%%
# %%
import numpy as np

from bokeh.plotting import figure, show
from bokeh.io import output_notebook
output_notebook()

N = 500
x = np.linspace(0, 10, N)
y = np.linspace(0, 10, N)
xx, yy = np.meshgrid(x, y)
d = np.sin(xx)*np.cos(yy)

p = figure(tooltips=[("x", "$x"), ("y", "$y"), ("value", "@image")])
p.x_range.range_padding = p.y_range.range_padding = 0

# must give a vector of image data for image parameter
p.image(image=[d], x=0, y=0, dw=10, dh=10, palette="Spectral11")

#output_file("image.html", title="image.py example")


show(p)  # open a browser
# %%
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as pltP
# plotly and cufflinks
import plotly.offline as py
import plotly.graph_objs as go
py.init_notebook_mode(connected=True)
import ipywidgets as widgets
import yahoo_finance_pynterface as yahoo
import utils.market_tools as mkt

#%%
# add the current folder
if __MY_FORTYFIVE_ROOT__ not in sys.path:
    sys.path.append(__MY_FORTYFIVE_ROOT__)
    
#%%
hist_period = ['1950-01-01', '2020-01-08']

#%%
df = yahoo.Get.Prices('^NDX', period=hist_period)

#%%
breakpoint()
mkt.bollinger_band(df['Adj Close']).iplot()

#%% 
import numpy as np

from bokeh.plotting import figure, show, output_file
from bokeh.io import output_notebook
N = 500
x = np.linspace(0, 10, N)
y = np.linspace(0, 10, N)
xx, yy = np.meshgrid(x, y)
d = np.sin(xx)*np.cos(yy)

p = figure(tooltips=[("x", "$x"), ("y", "$y"), ("value", "@image")])
p.x_range.range_padding = p.y_range.range_padding = 0

# must give a vector of image data for image parameter
p.image(image=[d], x=0, y=0, dw=10, dh=10, palette="Spectral11")

#output_file("image.html", title="image.py example")
output_notebook()

show(p)  # open a browser
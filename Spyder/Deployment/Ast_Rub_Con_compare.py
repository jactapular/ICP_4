# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 09:33:16 2018

@author: Jack
"""

import pandas as pd #dataframe and plotting
import numpy as np #data clean
import matplotlib.pyplot as plt
#import matplotlib.dates
#import datetime as dt


# =============================================================================
# clean to data by recognizing zeros and temp of 85 as nan 
# axis = 0 for row, 1 for column
# =============================================================================
def clean(data):
    data = data.replace(0,np.nan)
    data = data.replace(85,np.nan)
    data = data.dropna(axis=0,  how = 'any')
    data['Date Time'] = pd.to_datetime(data['Date Time'])
    return data;


def timeframe(start, end, data): 
    s = pd.to_datetime(start)
    e = pd.to_datetime(end)
    data = data[data['Date Time'] > s]
    data = data[data['Date Time'] < e]
    return data;
# =============================================================================
# Import csv
# =============================================================================

ast = pd.read_csv('Astro Turf.csv')
ast = clean(data = ast)

rub = pd.read_csv('Composite Rubber.csv')
rub = clean(data = rub)

con = pd.read_csv('Concrete.csv')
con = clean(data = con)

start = '2018-02-12 15:30:00'
end =   '2018-02-13 08:00:00'

ast = timeframe(start, end, ast)
rub = timeframe(start, end, rub)
con = timeframe(start, end, con)

# =============================================================================
# Plot light and temp seperately
# =============================================================================


ax = ast.plot(color = 'tab:olive', x='Date Time', y= 'Temperature')
#sensor.plot(secondary_y=True, color = 'b', x='Date Time', y= 'Light', ax=ax)
rub.plot(color = 'r', x='Date Time', y= 'Temperature', ax=ax)
con.plot(color = 'b', x='Date Time', y= 'Temperature', ax=ax)
ax.set(xlabel='Date Time (DD-MM HH)', ylabel='Temperature (°C)')
ax.legend(["Fake Grass", "Composite Rubber", "Concrete"])
plt.savefig('Comparison-preso.png', bbox_inches='tight')

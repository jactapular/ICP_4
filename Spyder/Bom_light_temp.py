# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 14:40:20 2018

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
# Import todays csv
# =============================================================================

sensor = pd.read_csv('7_Thursday.csv')
sensor = clean(data = sensor)

bom = pd.read_csv('bom.csv')
bom = clean (data = bom)

start = '2018-01-25 12:00:00'
end = '2018-01-26 12:00:00'

sensor = timeframe(start, end, sensor)
bom = timeframe(start, end, bom)

# =============================================================================
# Plot light and temp seperately
# =============================================================================


ax = sensor.plot(color = 'r', x='Date Time', y= 'Temperature')
#sensor.plot(secondary_y=True, color = 'y', x='Date Time', y= 'Light', ax=ax)
bom.plot(color = 'b', x='Date Time', y= 'Temperature', ax=ax)
ax.set(xlabel='Date Time (DD-MM HH)', ylabel='Temperature (°C)')
ax.legend(["Red Brick", "Weather Station"])
plt.savefig('bom_vs_brick_sensors_labels.pdf', bbox_inches='tight')

# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 10:07:51 2018

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

gra = pd.read_csv('Grass.csv')
gra = clean(data = gra)

con = pd.read_csv('Concrete.csv')
con = clean(data = con)

start = '2018-02-08 12:00:00'
end =   '2018-02-09 12:00:00'

gra = timeframe(start, end, gra)
con = timeframe(start, end, con)

# =============================================================================
# Plot light and temp seperately
# =============================================================================


ax = gra.plot(color = 'g', x='Date Time', y= 'Temperature')
con.plot(color = 'r', x='Date Time', y= 'Temperature', ax=ax)
#gra.plot(secondary_y=True, color = 'y', x='Date Time', y= 'Light', ax=ax)
ax.set(xlabel='Date Time (DD-MM HH)', ylabel='Temperature (°C)')
ax.legend(["Grass", "Concrete"])
plt.savefig('Comparison_Grass_Concrete.png', bbox_inches='tight')

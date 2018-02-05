# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 13:02:41 2018

@author: Jack
"""

import pandas as pd #dataframe and plotting
import numpy as np #data clean
import matplotlib.pyplot as plt


# =============================================================================
# Import todays csv
# =============================================================================

data = pd.read_csv('Project_2_0006_20180129-0841.csv')

# =============================================================================
# Remove unwanted columns
# =============================================================================
data = data.drop('Proj ID', axis=1)
data = data.drop('Unit ID', axis=1)
data = data.drop('Date Time', axis=1)
data = data.drop('Light', axis=1)


# =============================================================================
# clean to data by recognizing zeros and temp of 85 as nan 
# axis = 0 for row, 1 for column
# =============================================================================

data = data.replace(0,np.nan)
data = data.replace(85,np.nan)
data = data.dropna(axis=0,  how = 'any')
#pd.to_datetime(data['Date Time'])


# =============================================================================
# Percentage change in temp data
# =============================================================================
#5 minute intervals
#data.pct_change(periods=30).describe()


# =============================================================================
# max temp change over an interval
# =============================================================================

max_list = []
for x in range(0, 120):
    val = data.pct_change(periods=x).max()[0]
    max_list.append(val)

ave_list = []
for x in range(0, 120):
    val = data.pct_change(periods=x).mean()[0]
    ave_list.append(val)
    
ave_list = []
for x in range(0, 120):
    val = data.pct_change(periods=x).mean()[0]
    ave_list.append(val)

df = pd.DataFrame({'Max Temp Change':max_list,'Mean Temp Change':ave_list})


df.plot(title = 'Temp change', grid = 'true')

# =============================================================================
# 
# =============================================================================



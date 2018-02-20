import pandas as pd #dataframe and plotting
import numpy as np #data clean
import matplotlib.pyplot as plt
#import matplotlib.dates
#import datetime as dt

# =============================================================================
# Import todays csv
# =============================================================================

data = pd.read_csv('7_Thursday.csv')

# =============================================================================
# clean to data by recognizing zeros and temp of 85 as nan 
# axis = 0 for row, 1 for column
# =============================================================================

data = data.replace(0,np.nan)
data = data.replace(85,np.nan)
data = data.dropna(axis=0,  how = 'any')
data['Date Time'] = pd.to_datetime(data['Date Time'])
# =============================================================================
# Plot light and temp seperately
# =============================================================================
plt.figure()

with pd.plot_params.use('x_compat', True):
    data.Temperature.plot(color = 'r', x='Date Time')
    #plt.savefig('temp_plot.pdf')
    data.Light.plot(secondary_y=True, color = 'b', x='Date Time')
    #plt.savefig('light_plot.pdf')
data.Temperature.plot()

with pd.plotting.plot_params.use('x_compat', True):
    data.plot(color = 'r', x='Date Time', y= 'Temperature')
    #plt.savefig('temp_plot.pdf')
    data.plot(secondary_y=True, color = 'b', x='Date Time', y= 'Light')
    #plt.savefig('light_plot.pdf')

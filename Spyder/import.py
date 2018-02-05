import pandas as pd #dataframe and plotting
import numpy as np #data clean
import matplotlib.pyplot as plt


# =============================================================================
# Import todays csv
# =============================================================================

data = pd.read_csv('Project_2_0006_20180129-0841.csv')

# =============================================================================
# clean to data by recognizing zeros and temp of 85 as nan 
# axis = 0 for row, 1 for column
# =============================================================================

data = data.replace(0,np.nan)
data = data.replace(85,np.nan)
data = data.dropna(axis=0,  how = 'any')

# =============================================================================
# Percentage change in temp data
# =============================================================================



# =============================================================================
# Plot light and temp seperately
# =============================================================================
data.plot(x='Date Time', y='Temperature')
plt.savefig('temp_plot.pdf')
data.plot(x='Date Time', y='Light')
plt.savefig('light_plot.pdf')
#%%
import numpy as np  #for numeric computations like log, exp, sqrt
import pandas as pd #for reading & storing data, pre=processing
from sklearn.preprocessing import PolynomialFeatures
import matplotlib.pyplot as plt #for visualization
import statsmodels.api as sm
from scipy import stats

# use your own data
data = pd.read_csv('./May/HeXA/Datacollection05/stockPrice.csv', index_col='date')

# convert index type to datetime
data.index = pd.to_datetime(data.index)

data.drop(['high', 'low', 'close', 'volume'], axis = 1, inplace=True)

data.plot()

#%%
fig = plt.scatter(data.shift(1)[1:], data[1:])
plt.xlabel('Previous Day Open Price')
plt.ylabel('Open Price')

plt.show()

# monthly_data = data.resample('M').first() # resample with closing price on the first trading day of the month 
# monthly_data = data.resample('M').mean() # resample with monthly average closing price
monthly_data = data.resample('M').last() # resample with closing price on the last trading day of the month 


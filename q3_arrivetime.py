from __future__ import division
import pandas as pd
import scipy
#scipy.stats.expon
import matplotlib.pyplot as plt
import numpy as np
import datetime
import seaborn as sns

trade = pd.read_csv('trade.csv')
trade['TIME_M'] = pd.to_datetime(trade['TIME_M']) + pd.DateOffset(days=-755)
trade = trade.loc[(trade['DATE']==20160104)&(trade['TIME_M']>=pd.to_datetime('2016-01-04 10:00:00'))\
                  &(trade['TIME_M']<=pd.to_datetime('2016-01-04 16:00:00'))][['DATE','TIME_M']]
trade['pre_time']=trade['TIME_M'].shift(1)
trade['diff_time']=(trade['TIME_M']-trade['pre_time']).dt.total_seconds()
trade = trade.loc[trade['diff_time']>=0.000001]
lam = trade['diff_time'].mean()
print(lam)
print(trade)

f,(ax1,ax2) = plt.subplots(1,2, sharey =True)
ax1.hist(trade['diff_time'], bins=300)
ax1.set_title("PDF of Transaction Arrival Time")
exp = np.random.exponential(scale=lam,size=50000)
ax2.hist(exp,bins=300)
ax2.set_title("PDF of Exponential Distribution with Same Mean")
#pd.Series(trade['diff_time']).hist(bins=100, range=(0,3))
#plt.hist(exp,bins=300)
plt.show()


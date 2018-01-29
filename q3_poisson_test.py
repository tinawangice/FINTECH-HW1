from __future__ import division
import pandas as pd
import scipy
#scipy.stats.expon
import matplotlib.pyplot as plt
import numpy as np
import datetime
import seaborn as sns

trade = pd.read_csv('trade.csv')
trade['TIME_M']= pd.to_datetime(trade['TIME_M']).dt.round('5s') + pd.DateOffset(days=-755)
trade1 = trade.loc[(trade['DATE']==20160104)&(trade['TIME_M']>=pd.to_datetime('2016-01-04 10:00:00'))\
                  &(trade['TIME_M']<=pd.to_datetime('2016-01-04 16:00:00'))][['DATE','TIME_M']]

df1 = trade1[['TIME_M']].groupby(['TIME_M']).size().reset_index(name='count')

trade['TIME_M'] = trade['TIME_M']+ pd.DateOffset(days=1)
trade2 = trade.loc[(trade['DATE']==20160105)&(trade['TIME_M']>=pd.to_datetime('2016-01-05 10:00:00'))\
                  &(trade['TIME_M']<=pd.to_datetime('2016-01-05 16:00:00'))][['DATE','TIME_M']]

df2 = trade2[['TIME_M']].groupby(['TIME_M']).size().reset_index(name='count')

df = pd.concat([df1,df2],axis=0,ignore_index=True)

lam1 = 1/df['count'].mean()
print(lam1)

# print(trade)
#
# print(scipy.stats.kstest(trade.iloc[1:,-1], 'expon'))
#
#f,(ax1,ax2) = plt.subplots(1,2, sharey =True)
# ax1.hist(df['count'],bins=50)
# ax1.set_title("Distribution of Arrivals in 5s")
# pois = np.random.poisson(lam1,size=10000)
# ax2.hist(pois,bins=50)
# ax2.set_title("PDF of Poisson Distribution with Same Mean")
# #pd.Series(trade['diff_time']).hist(bins=100, range=(0,3))
# #plt.hist(exp,bins=300)
# sns.distplot(pois)
ax1 = sns.distplot(df['count'], range(0,40))
ax1.set_title("Distribution of Arrivals in 5s")
plt.show()

print(scipy.stats.kstest(df['count'], 'expon'))
print(scipy.stats.kstest(df['count'], 'norm'))

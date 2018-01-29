from __future__ import division
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

df1 = pd.read_csv('data20160104.csv', sep='\t')
df2 = pd.read_csv('data20160105.csv', sep='\t')

df = pd.concat([df1, df2], axis=0,ignore_index=True)

print(df.loc[:,['time_start','time_end','spread_mean','star_cov']])
num = len(df['spread_mean'])
var_spread =df['spread_mean'].var(ddof=1)
var_cov = df['star_cov'].var(ddof=1)

print(var_spread,"\n",var_cov,"\n",num)
stddev = np.sqrt((var_cov+var_spread)/2)
t = (df['spread_mean'].mean()-df['star_cov'].mean())/(stddev*np.sqrt(2/num))

dfree = 2*num -2
p = 1 - stats.t.cdf(t,df=dfree)

print("t = " + str(t))
print("p = " + str(2*p))


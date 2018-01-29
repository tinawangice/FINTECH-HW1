from __future__ import division
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

df = pd.read_csv('equ_price_spread0104.csv', sep='\t')
df2 = pd.read_csv('equ_price_spread0105.csv', sep='\t')

df['diff'] = df['price']-df['equl']
df['sign']=[0 if t==0 else 1 if t>0 else -1 for t in df['diff']]
df['cul_sum']=df['sign']
for i in range(1,len(df.index)):
    df.ix[i,-1]+= df.ix[i-1,-1]

df2['diff'] = df2['price']-df2['equl']
df2['sign']=[0 if t==0 else 1 if t>0 else -1 for t in df2['diff']]
df2['cul_sum']=df2['sign']
for i in range(1,len(df2.index)):
    df2.ix[i,-1]+= df2.ix[i-1,-1]

pd.Series(df['cul_sum']).plot()
pd.Series(df2['cul_sum']).plot()
plt.suptitle('Clock Time 5 seconds_Cumulative Sum of I (Walk of I)', fontsize=16)
plt.legend(['2016-01-04 10:00 to 2016-01-04 16:00', '2016-01-05 10:00 to 2016-01-05 16:00'])
plt.show()


 # count =0
    # for i in range(len(temp['spread'])):
    #     if temp.iloc[i,-1]>star_cov*0.5 and temp.iloc[i,-1]<star_cov*1.5:
    #         count+=1
    # plt.axvline(star_cov,color='k')
    # pd.Series(temp['spread']).plot(kind='density')

    # plt.show()
    # ratio = count/ len(temp['spread'])
    # print("ratio=",ratio)

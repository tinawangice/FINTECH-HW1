from __future__ import division
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
quote = pd.read_csv('quote.csv')
trade = pd.read_csv('trade.csv')
trade = trade.loc[trade['DATE']==20160105]
trade['TIME_M']= pd.to_datetime(trade['TIME_M']).dt.round('5s') + pd.DateOffset(days=-754)
trade0105 = pd.DataFrame(columns=['time', 'price'])
trade0105.time = trade['TIME_M'].drop_duplicates()

minute_price = {}
for i in range(len(trade['TIME_M'])):
    minute_price[str(trade.iloc[i,1])]=trade.iloc[i,7]

trade0105['price'] = [minute_price.get(str(t)) for t in trade0105['time']]
trade0105 = trade0105.dropna(how='any')

def interval_cov(trade0105, a='2016-01-05 10:00:00', b='2016-01-05 16:00:00'):
    trade0105['time']= pd.to_datetime(trade0105['time'])
    if pd.to_datetime(a)< min(trade0105['time']) or pd.to_datetime(b) > max(trade0105['time']):
        return None
    else:
        temp = trade0105.loc[(trade0105['time'] >= pd.to_datetime(a)) & (trade0105['time'] <= pd.to_datetime(b))][['time', 'price']]
#         print(temp)
#         cov= np.cov(temp.iloc[0:-1,-1],temp.iloc[1:,-1])[0][1]
#         star_cov = 2*((abs(cov))**0.5)
#         print("cov=",cov)
#         print("2*sqrt(-cov):",star_cov)
    return(temp)
#
# interval_cov(trade0104, a='2016-01-04 10:10:00', b='2016-01-04 10:40:00')
df_price = interval_cov(trade0105).set_index('time')
print('\n\nprice_df')
print(df_price.head())

quote = quote.loc[(quote['DATE']==20160105)&(quote['ASK']>0)&(quote['BID']>0)]
quote['TIME_M']= pd.to_datetime(quote['TIME_M']).dt.round('5s') + pd.DateOffset(days=-754)
quote0105 = pd.DataFrame(columns=['time', 'ask', 'bid'])
quote0105.time = quote['TIME_M'].drop_duplicates()

ask_price={}
bid_price={}
ask_price[str(quote.iloc[1,1])]=quote.iloc[1,7]

for i in range(len(quote['TIME_M'])):
    ask_price[str(quote.iloc[i,1])]=quote.iloc[i,7]
    bid_price[str(quote.iloc[i,1])]=quote.iloc[i,5]

quote0105['ask'] = [ask_price.get(str(t)) for t in quote0105['time']]
quote0105['bid'] = [bid_price.get(str(t)) for t in quote0105['time']]
quote0105['equl'] = 0.5 * (quote0105['ask'] + quote0105['bid'])
quote0105['spread'] = quote0105['ask'] - quote0105['bid']


def interval_spread(quote0105, a='2016-01-05 10:00:00', b='2016-01-05 16:00:00'):
    if pd.to_datetime(a)< min(quote0105['time']) or pd.to_datetime(b) > max(quote0105['time']):
        return None
    else:
        temp = quote0105.loc[(quote0105['time'] >= pd.to_datetime(a)) & (quote0105['time'] <= pd.to_datetime(b))]
        return(temp)

df_equ = interval_spread(quote0105, a='2016-01-05 10:00:00', b='2016-01-05 16:00:00').set_index('time')
print(df_equ.head())

df = pd.concat([df_price, df_equ], axis=1,ignore_index=False).dropna(how='any')

print(df.head())

df.to_csv('equ_price_spread0105.csv', sep='\t')


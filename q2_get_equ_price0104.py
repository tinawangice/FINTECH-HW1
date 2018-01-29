from __future__ import division
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
quote = pd.read_csv('quote.csv')
trade = pd.read_csv('trade.csv')
trade = trade.loc[trade['DATE']==20160104]
trade['TIME_M']= pd.to_datetime(trade['TIME_M']).dt.round('5s') + pd.DateOffset(days=-755)
trade0104 = pd.DataFrame(columns=['time', 'price'])
trade0104.time = trade['TIME_M'].drop_duplicates()

minute_price = {}
for i in range(len(trade['TIME_M'])):
    minute_price[str(trade.ix[i,'TIME_M'])]=trade.ix[i,'PRICE']

trade0104['price'] = [minute_price.get(str(t)) for t in trade0104['time']]
trade0104 = trade0104.dropna(how='any')

def interval_cov(trade0104, a='2016-01-04 10:00:00', b='2016-01-04 14:00:00'):
    trade0104['time']= pd.to_datetime(trade0104['time'])
    if pd.to_datetime(a)< min(trade0104['time']) or pd.to_datetime(b) > max(trade0104['time']):
        return None
    else:
        temp = trade0104.loc[(trade0104['time'] >= pd.to_datetime(a)) & (trade0104['time'] <= pd.to_datetime(b))][['time', 'price']]
#         print(temp)
#         cov= np.cov(temp.iloc[0:-1,-1],temp.iloc[1:,-1])[0][1]
#         star_cov = 2*((abs(cov))**0.5)
#         print("cov=",cov)
#         print("2*sqrt(-cov):",star_cov)
    return(temp)
#
# interval_cov(trade0104, a='2016-01-04 10:10:00', b='2016-01-04 10:40:00')
df_price = interval_cov(trade0104).set_index('time')
print('\n\nprice_df')
print(df_price.head())

quote = quote.loc[(quote['DATE']==20160104)&(quote['ASK']>0)&(quote['BID']>0)]
quote['TIME_M']= pd.to_datetime(quote['TIME_M']).dt.round('5s') + pd.DateOffset(days=-755)
quote0104 = pd.DataFrame(columns=['time', 'ask','bid'])
quote0104.time = quote['TIME_M'].drop_duplicates()

ask_price={}
bid_price={}
ask_price[str(quote.iloc[1,1])]=quote.iloc[1,7]

for i in range(len(quote['TIME_M'])):
    ask_price[str(quote.iloc[i,1])]=quote.iloc[i,7]
    bid_price[str(quote.iloc[i,1])]=quote.iloc[i,5]

quote0104['ask'] = [ask_price.get(str(t)) for t in quote0104['time']]
quote0104['bid'] = [bid_price.get(str(t)) for t in quote0104['time']]
quote0104['equl'] = 0.5*(quote0104['ask']+quote0104['bid'])
quote0104['spread'] = quote0104['ask']-quote0104['bid']


def interval_spread(quote0104, a='2016-01-04 10:00:00', b= '2016-01-04 16:00:00'):
    if pd.to_datetime(a)< min(quote0104['time']) or pd.to_datetime(b) > max(quote0104['time']):
        return None
    else:
        temp = quote0104.loc[(quote0104['time'] >= pd.to_datetime(a)) & (quote0104['time'] <= pd.to_datetime(b))]
        return(temp)

df_equ = interval_spread(quote0104, a='2016-01-04 10:00:00', b= '2016-01-04 16:00:00').set_index('time')
print(df_equ.head())

df = pd.concat([df_price, df_equ], axis=1,ignore_index=False).dropna(how='any')

print(df.head())

df.to_csv('equ_price_spread0104.csv', sep='\t')


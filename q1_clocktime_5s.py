from __future__ import division
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
quote = pd.read_csv('quote.csv')
trade = pd.read_csv('trade.csv')
trade['pre_price']=trade['PRICE'].shift(1)
trade['diff']=trade['PRICE']-trade['pre_price']
trade = trade.loc[trade['DATE']==20160104]

def minus_days(a='2016-01-05'):
    today = str(datetime.datetime.now()-datetime.datetime.strptime(a, '%Y-%m-%d'))
    today = today.split(' ')
    return int(today[0])

day_diff = minus_days(a='2016-01-05')

trade['TIME_M']= pd.to_datetime(trade['TIME_M']).dt.round('5s') + pd.DateOffset(days=-day_diff)
trade0104 = pd.DataFrame(columns=['time', 'price'])
trade0104.time = trade['TIME_M'].drop_duplicates()

minute_price = {}
for i in range(len(trade['TIME_M'])):
    minute_price[str(trade.ix[i,'TIME_M'])]=trade.ix[i,'PRICE']

trade0104['price'] = [minute_price.get(str(t)) for t in trade0104['time']]
trade0104 = trade0104.dropna(how='any')
trade0104['pre_price']=trade0104['price'].shift(1)
trade0104['diff']= trade0104['price'] - trade0104['pre_price']

def interval_cov(price0104, a='2016-01-04 10:10:00', b= '2016-01-04 10:40:00'):
    price0104['time']= pd.to_datetime(price0104['time'])
    if pd.to_datetime(a)< min(price0104['time']) or pd.to_datetime(b) > max(price0104['time']):
        return None
    else:
        temp = price0104.loc[(price0104['time']>=pd.to_datetime(a))&(price0104['time']<=pd.to_datetime(b))][['time','diff']]
        print(temp)
        cov= np.cov(temp.iloc[0:-1,-1],temp.iloc[1:,-1])[0][1]
        star_cov = 2*((abs(cov))**0.5)
        print("cov=",cov)
        print("2*sqrt(-cov):",star_cov)
        return(star_cov)

interval_cov(trade0104, a='2016-01-04 10:10:00', b='2016-01-04 10:40:00')


quote = quote.loc[(quote['DATE']==20160104)&(quote['ASK']>0)&(quote['BID']>0)]
quote['TIME_M']= pd.to_datetime(quote['TIME_M']).dt.round('5s') + pd.DateOffset(days=-day_diff)
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
quote0104['spread'] = quote0104['ask']- quote0104['bid']

def interval_spread(quote0104, a='2016-01-04 10:10:00', b= '2016-01-04 10:40:00'):
    if pd.to_datetime(a)< min(quote0104['time']) or pd.to_datetime(b) > max(quote0104['time']):
        return None
    else:
        temp = quote0104.loc[(quote0104['time'] >= pd.to_datetime(a)) & (quote0104['time'] <= pd.to_datetime(b))]
        return(temp)

interval_spread(quote0104, a='2016-01-04 10:10:00', b= '2016-01-04 10:40:00')


def compare_s_cov(quote0104,trade0104,a0='2016-01-04 10:10:00', b0= '2016-01-04 10:40:00'):
        star_cov = interval_cov(trade0104, a=a0, b=b0)
        temp = interval_spread(quote0104, a=a0, b=b0)

        # count =0
        # for i in range(len(temp['spread'])):
        #     if temp.iloc[i,-2]>star_cov*0.5 and temp.iloc[i,-2]<star_cov*1.5:
        #         count+=1
        #
        # plt.axvline(star_cov,color='k')
        # pd.Series(temp['spread']).plot(kind='density')
        # plt.legend(['2*sqrt(-cov)', 'PDF of spread'])
        # plt.suptitle('Clock_time Comparasion during %s to %s' %(a0,b0), fontsize=16)
        # plt.show()
        # ratio = count/ len(temp['spread'])
        # print("ratio=",ratio)
        # return ratio
        return star_cov, temp['spread'].tolist()

compare_s_cov(quote0104, trade0104, a0='2016-01-04 10:10:00', b0='2016-01-04 10:40:00')


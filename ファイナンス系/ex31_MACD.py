from pandas_datareader import data
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import talib as ta

#日経平均の取得
start = '2020-07-01'
end = '2021-07-01'

df = data.DataReader('^N225', 'yahoo', start, end)

date = df.index
close = df['Adj Close']

#移動平均の設定
span01 = 5
span02 = 25
span03 = 50
df['sma01']= close.rolling(window=span01).mean()
df['sma02']= close.rolling(window=span02).mean()
df['sma03']= close.rolling(window=span03).mean() 

df['macd'], df['macdsignal'], df['macdhist']=ta.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)

#MACD
plt.figure(figsize=(30, 15))
plt.subplot(2,1,1)

plt.plot(date, close,label='Close', color= '#99b898')
plt.legend()

plt.subplot(2,1,2)
plt.fill_between(date, df['macdhist'], color= 'grey', alpha= 0.5, label= 'MACD_hist')
plt.hlines(0,date[0],date[-1],'black',linestyles='dashed')
plt.legend()
    

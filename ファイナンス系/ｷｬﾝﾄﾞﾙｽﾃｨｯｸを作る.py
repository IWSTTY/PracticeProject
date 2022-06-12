from pandas_datareader import data
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
import numpy as np
# %matplotlib inline

import warnings
warnings.simplefilter('ignore')

#日経平均の取得
start = '2022-05-20'
end = '2022-05-30'

df = data.DataReader('^N225', 'yahoo', start, end)

date = df.index
close = df['Adj Close']

#ローソク足を作成
mpf.plot(df,type='candle',volume=False,mav=(5,25),figratio=(24,8),style='yahoo')

#=====================================================================================
import yahoo_fin.stock_info as si

symbol = 'IBM'
hist_data = si.get_data(symbol)
hist_data

#ローソク足を作成
mpf.plot(hist_data,type='candle',volume=False,mav=(5,25),figratio=(24,8),style='mike')

#=======================================================================================
import requests
from datetime import datetime
import time

url= 'https://api.cryptowat.ch/markets/bitflyer/btcfxjpy/ohlc'
response = requests.get(url, params= {'periods': 60 })

#Cryptowatchから〇分足のデータを取得する
def get_price(min, i):
	data = response.json()
	last_data = data["result"][str(min)][i]

	return {'close_time' : last_data[0],
	        'open_price' : last_data[1],
            'high_price' : last_data[2],
            'low_price' : last_data[3],
	        'close_price' : last_data[4] }

#日時、終値、始値を表示する関数
def print_price(data):
    print('時間：' + datetime.fromtimestamp(data['close_time']).strftime('%Y/%m/%d %H:%M')
          + '始値：' + str(data['open_price'])
          + '終値：' + str(data['close_price']))

def check_candle(data):
    realbody_rate = abs(data['close_price'] - data['open_price']) / (data['high_price']-data['low_price'])
    increase_rate = data['close_price'] / data['open_price'] - 1
    
    if data['close_price'] < data['open_price'] : return False
    elif increase_rate < 0.0005 : return False
    elif realbody_rate < 0.5 : return  False
    else : return True

i = 1
while i < 500:
    data = get_price(60, i)
    print_price(data)

    i += 1
    time.sleep(0)
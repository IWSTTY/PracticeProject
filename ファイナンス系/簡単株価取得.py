import requests
from datetime import datetime
import time
import pandas as pd

url= 'https://api.cryptowat.ch/markets/bitflyer/btcfxjpy/ohlc'
response = requests.get(url, params= {'periods': 60 })

Date_List = []
Open_List = []
High_List = []
Low_List = []
Close_List = []

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

i = 1
while i < 500:
    data = get_price(60, i)
    # print_price(data)
    Date_List.append(datetime.fromtimestamp(data['close_time']).strftime('%Y/%m/%d %H:%M'))
    Open_List.append(data['open_price'])
    High_List.append(data['high_price'])
    Low_List.append(data['low_price'])
    Close_List.append(data['close_price'])
    
    if i == 499:
        df = pd.DataFrame(list(zip(Open_List, High_List, Low_List,Close_List)),
                                columns = ['Open','High', 'Low', 'Close'],index=Date_List)
        df.to_csv('sample000.csv')
    i += 1
    time.sleep(0)
    
    
    
import os
from matplotlib.axis import XAxis
import requests
import pprint
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import mplfinance as mpf
import csv
#------------------------------------------------------------------------
#カラム名をリネームしてExcel出力する関数
def REname_and_toExcel(df1,symbolword):
    df_2=df1.rename(columns={
        0:'日付',
        1:'始値',
        2:'高値',
        3:'低値',
        4:'終値',
        5:'出来高'})
    #print(df_2)
    ExName = str(f'{symbolword}.xlsx')
    df_2.to_excel(ExName)
    return ExName

#カラム名をリネームしてCSV出力する関数
def REname_and_toCSV(df1,symbolword):
    df_2=df1.rename(columns={
        0:'Date',
        1:'Open',
        2:'High',
        3:'Low',
        4:'Close',
        5:'Volume'})
    #print(df_2)
    CsvName = str(f'{symbolword}.csv')
    df_2.to_csv(CsvName)
    return CsvName
#------------------------------------------------------------------------
symbol = input('シンボルを入力：')
#マイクロソフト—MSFT　アップル-AAPL　グーグル-GOOGL テスラ-TSLA
#アマゾン-AMZN 大成建設-TISCF 鹿島建設-KAJMF 清水建設-SHMUF
#symbol ='MSFT'
api_key = os.environ['ALPHA_VANTAGE_KEY']
url = 'https://www.alphavantage.co/query?'\
        f'function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}'
data = requests.get(url).json()
# pprint.pprint(data)

#データをリストに格納
daily_data = dict(reversed(data['Time Series (Daily)'].items()))
# pprint.pprint(daily_data)
date_list = daily_data.keys()
open_list = [float(x['1. open']) for x in daily_data.values()]
high_list = [float(x['2. high']) for x in daily_data.values()]
low_list = [float(x['3. low']) for x in daily_data.values()]
close_list = [float(x['4. close']) for x in daily_data.values()]
volume_list = [float(x['5. volume']) for x in daily_data.values()]

#リストをまとめてデータフレームに格納
ZipList=list(zip(date_list,open_list,high_list,low_list,close_list,volume_list))
df_1 = pd.DataFrame(ZipList)
#pprint.pprint(df_1)
CsvName= REname_and_toCSV(df_1,symbol)#Excel出力関数
df_3 = pd.read_csv(CsvName,index_col=0,parse_dates=True,)
#print(df_3)

#インデックスをDateTimeIndexに変換
df_3['Date']=pd.to_datetime(df_3['Date'])
#print(type(df_3.index))
df_3.set_index('Date',inplace=True)
#print(type(df_3.index))

#ローソク足を作成
mpf.plot(df_3,type='candle',volume=True,mav=(5,25),
         figratio=(24,8),style='yahoo',savefig=f'{symbol}-candlestick.png')
#mpf.show()


print("end")
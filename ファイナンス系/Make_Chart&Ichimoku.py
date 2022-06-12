import mplfinance as mpf
from pandas_datareader import data
import talib as ta
import matplotlib.pyplot as plt

import warnings
warnings.simplefilter('ignore')


#B-BAND,MACD,RSI,CandleStickを作成
def MakeCharts(df,co_code):
    #B-BAND
    df['upper'],df['middle'],df['lower'] = ta.BBANDS(df['Close'], timeperiod = 25,
                                                 nbdevup=2, nbdevdn=2, matype=0)
    #MACD
    df['macd'], df['macdsignal'], df['macdhist']=ta.MACD(df['Close'], fastperiod=12, 
                                                        slowperiod=26, signalperiod=9)
    #RSI
    df['RSI'] = ta.RSI(df['Close'], timeperiod=25)
    
    apds = [mpf.make_addplot(df['upper'], color = 'g'),  #ﾎﾞﾘﾝｼﾞｬｰ
        mpf.make_addplot(df['middle'], color = 'b'),
        mpf.make_addplot(df['lower'], color = 'r'),
        mpf.make_addplot(df['macdhist'], type='bar', color='dimgray',   #MACD
                         width=0.7, panel=1, alpha=0.5, ylabel='MACD'),
        mpf.make_addplot(df['RSI'], panel=2, type='line', ylabel='RSI',color='blue')  #RSI
        ]

    mpf.plot(df, type='candle', figsize=(30, 15), style='mike',volume = True, addplot = apds,
         volume_panel=3, panel_ratios=(5,2,2,1), savefig=f'{co_code}_CHARTS.png') 

def MakeIchimoku(df,co_code):
    date = df.index
    high = df['High']
    low = df['Low']
    #基準線
    max26 = high.rolling(window=26).max()
    min26 = low.rolling(window=26).min()
    df['basic_line'] = (max26 + min26) / 2
    #転換線
    high9 = high.rolling(window=9).max()
    low9 = low.rolling(window=9).min()
    df['turn_line'] = (high9 + low9) / 2
    #先行ｽﾊﾟﾝ
    df['span1'] = (df['basic_line'] + df['turn_line']) / 2
    high52 = high.rolling(window=52).max()
    low52 = low.rolling(window=52).min()
    df['span2'] = (high52 + low52) / 2
    #遅行線
    df['slow_line'] = df['Close'].shift(-25)
    ##作図
    lines = [mpf.make_addplot(df['basic_line']),  #基準線
            mpf.make_addplot(df['turn_line']),   #転換線
            mpf.make_addplot(df['slow_line']),   #遅行線
            ]

    labels = ['basic', 'turn', 'slow', 'span']

    fig, ax = mpf.plot(df, type='candle', figsize=(16,6), style='mike', xrotation=0,
                   addplot=lines, returnfig=True,
                   fill_between=dict(y1=df['span1'].values, y2=df['span2'].values,
                                     alpha=0.5, color='gray'),savefig=f'{co_code}_Ichimoku.png')

    ax[0].legend(labels)
    
#以下は設定です
start = '2021-04-30'
end = '2022-04-30'
co_code = '7203.JP'  #株価コード
df = data.DataReader(co_code, 'stooq')
df = df[(df.index >= start) & (df.index <= end)] 

# MakeCharts(df,co_code)
MakeIchimoku(df,co_code)
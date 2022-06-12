#株価に関する色んなチャートを作成する
#移動平均、MACD,RSI,B-BAND,CandleStick

from pandas_datareader import data
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import talib as ta
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
import mplfinance as mpf

import warnings
warnings.simplefilter('ignore')

#色んなチャートを作成する関数
def company_stock(start, end, company_code):
    path = 'C://Users//ユーザー名//Documents//MyPython//'
    df = data.DataReader(company_code, 'stooq')
    df = df[(df.index >= start) & (df.index <= end)] 
    
    date = df.index
    close = df['Close']
    
   #移動平均の設定
    span01 = 5
    span02 = 25
    span03 = 50
    df['sma01']= close.rolling(window=span01).mean()
    df['sma02']= close.rolling(window=span02).mean()
    df['sma03']= close.rolling(window=span03).mean() 
    
    #DF加工⇒MACD,RSI,B-BAND,CandleStick
    df['macd'], df['macdsignal'], df['macdhist']=ta.MACD(close, fastperiod=12, 
                                                     slowperiod=26, signalperiod=9)
    df['RSI'] = ta.RSI(close, timeperiod=span02)
    df['upper'],df['middle'],df['lower'] = ta.BBANDS(close, timeperiod = span02,
                                                 nbdevup=2, nbdevdn=2, matype=0)
    df_candle = df[['High', 'Low', 'Open', 'Close', 'Volume']]
    tcdf = df[['upper', 'middle', 'lower']]
    apd = mpf.make_addplot(tcdf)
    
    #チャート色んなの
    plt.figure(figsize=(40, 60))

    plt.subplot(5,1,1)##移動平均線
    plt.plot(date, close,label='Close', color= '#99b898')
    plt.plot(date, df['sma01'],label= 'sma01',color= '#e84a5f')
    plt.plot(date, df['sma02'],label= 'sma02',color= '#ff847c')
    plt.plot(date, df['sma03'],label= 'sma03',color= '#feceab')
    plt.legend()

    plt.subplot(5,1,2)##出来高ヒストグラム
    plt.bar(date, df['Volume'],label= 'Volume',color= 'grey')
    plt.legend()

    plt.subplot(5,1,3)##MACD
    plt.fill_between(date, df['macdhist'], color= 'grey', alpha= 0.5, label= 'MACD_hist')
    plt.hlines(0,date[0],date[-1],'black',linestyles='dashed')
    plt.legend()

    plt.subplot(5,1,4)##RSI
    plt.plot(date, df['RSI'], label= 'RSI',color= 'red')
    plt.ylim(0, 100)
    plt.hlines([30, 50, 70], date[0], date[-1], "gray", linestyles="dashed")
    plt.legend()

    plt.subplot(5,1,5)##B-BAND
    plt.plot(date, close, label = 'Close', color = '#99b898')
    plt.fill_between(date, df['upper'],df['lower'], color = 'gray', alpha = 0.3)
    plt.legend()
    plt.savefig(f'stock_{company_code}.png')
    
    ##Candle Stick
    mpf.plot(df_candle, addplot=apd, type='candle',volume = True,
             style= 'yahoo', figsize=(30, 15), savefig=f'{company_code}-candlestick.png')


#企業名を取得する関数   
def get_comapany_name(company_code):
    options = Options()
    options.add_argument('--headless')

    #URL
    CrPh=r'C://Users//ユーザー名//Documents//MyPython//chromedriver'
    # browser = webdriver.Chrome(CrPh)
    browser = webdriver.Chrome(CrPh,options=options)#ﾍｯﾄﾞﾚｽﾓｰﾄﾞ
    browser.get('https://stooq.pl/')
    
    elem_co_name0 = browser.find_element_by_id('cmp0a')
    elem_co_name0.send_keys(f'{company_code}')
    btn = browser.find_element_by_id('f13')
    btn.click()
    sleep(3)
    elem_co_name1 = browser.find_element_by_xpath("/html/body/table/tbody/tr[2]/td[2]/table/tbody/tr/td/table/tbody/tr/td/table[3]/tbody/tr/td[2]/b/font")
    co_name = elem_co_name1.text
    browser.quit()
    return co_name

co_code = '7203.JP'#←会社のシンボルを入力
company_stock('2021-05-20', '2022-05-20', f'{co_code}')
print(get_comapany_name(co_code)) 
print('end')
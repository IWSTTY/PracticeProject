from pandas_datareader import data
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options

def company_stock(start, end, company_code):
    path = 'C://Users//ユーザー名//Documents//MyPython//'
    df = data.DataReader(company_code, 'stooq')
    df = df[(df.index >= start) & (df.index <= end)] 
    
    date = df.index
    price = df['Close']
    
   #移動平均の設定
    span01 = 5
    span02 = 25
    span03 = 50
    df['sma01']= price.rolling(window=span01).mean()
    df['sma02']= price.rolling(window=span02).mean()
    df['sma03']= price.rolling(window=span03).mean() 
    
    #日経平均と移動平均（5,25,50日）+出来高を図化
    plt.figure(figsize=(20, 10))
    plt.subplot(2,1,1)

    plt.plot(date, price,label='Adj-close', color= '#99b898')
    plt.plot(date, df['sma01'],label= 'sma01',color= '#e84a5f')
    plt.plot(date, df['sma02'],label= 'sma02',color= '#ff847c')
    plt.plot(date, df['sma03'],label= 'sma03',color= '#feceab')

    plt.title(f'{company_code}', color= 'black', size= 40, loc= 'center' )
    plt.xlabel('date', color= 'grey',size= 30)
    plt.ylabel('price', color= 'grey',size= 30)
    plt.legend()

    plt.subplot(2,1,2)
    plt.bar(date, df['Volume'],label= 'Volume',color= 'grey')
    plt.ylabel('Volume', color= 'grey',size= 30)
    plt.legend()
    
    plt.savefig(f'stock_{company_code}.png')

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

co_code = '1801.JP'
company_stock('2021-05-20', '2022-05-20', f'{co_code}')
print(get_comapany_name(co_code)) 
print('end')
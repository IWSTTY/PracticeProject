import random
import datetime
import pandas as pd
import calendar
import string
import pprint
from urllib import request
import csv
from bs4 import BeautifulSoup
import re

#空のリストをつくる
Dep_Date=[]#出発日
ap_No=[]#便名
Dep_AP=[]#出発空港
Arr_AP=[]#到着空港
NoP=[]#旅客数
Cag_W=[]#貨物重量
# AirPort=['HND','CTS','AKJ','HIJ','OKA','FUK','CMP','NRT']#空港
AirPort=[]#空港

#空港の3桁コード（IATA）をDataFrameで抽出してAirPortというリストに格納
url='https://kumariair.com/blog/archives/20190608.html'
response = request.urlopen(url)
soup = BeautifulSoup(response,"html.parser")

for j in range(160,179):
    table=soup.find("table",attrs={"id":f"tablepress-{j}"})
    ths=table.find_all('th')
    tbl_Col2 = table.find_all('td',attrs={"class":f"column-2"})
    
    for tc2 in tbl_Col2:
        AirPort.append(tc2.string)
#-------------------------------------------------------

#今の日時をフォーマット変えて出力（不採用）
# DT=datetime.datetime.now()
# DT2= "{0:%Y/%m/%d %H:%M}".format(DT)

def GetTime():#ランダムな日付を取得する関数
    rd_Y=random.randint(2020,2022)
    rd_M=random.randint(1,12)
    #年と月から月終わりの日付を取得↓
    x=(calendar.monthrange(rd_Y,rd_M)[1])
    rd_D=random.randint(1,x)
    rd_T=random.randint(5,23)
    rd_DT=str(rd_Y)+'/'+str(rd_M)+'/'+str(rd_D)+' '+str(rd_T)+':00'
    rd_Dt_time=datetime.datetime.strptime(rd_DT,'%Y/%m/%d %H:%M')
    return rd_Dt_time

#アルファベットからランダム文字列を返す関数
def randstr(length):
    return ''.join([chr(random.randint(65, 90)) for _ in range(length)])

#ランダムな要素をリストに格納するループ（要素100個分）  
for i in range(1,101):
    
    a3=random.randint(100,999)
    a_NoP=random.randint(100,999)
    a_CW=random.randint(1000,9999)
    
    Dep_Date.append(GetTime())#出発日
    ap_No.append(randstr(3)+str(a3))#便名
    Dep_AP.append(random.choice(AirPort))#出発空港
    Arr_AP.append(random.choice(AirPort))#到着空港
    NoP.append(str(a_NoP))#旅客数
    Cag_W.append(str(a_CW))#貨物重量
    rd_M=0

Dep_Date.sort()#日付を降順にソート

#リストをまとめてデータフレームに格納してExcelに出力
ZipList=list(zip(Dep_Date,ap_No,Dep_AP,Arr_AP,NoP,Cag_W))
df_1 = pd.DataFrame(ZipList)
df_2=df_1.rename(columns={
    0:'出発日',
    1:'便名',
    2:'出発',
    3:'到着',
    4:'旅客数',
    5:'貨物重量'})
#print(df_2)
df_2.to_excel('sample_ap0.xlsx')

print('end')


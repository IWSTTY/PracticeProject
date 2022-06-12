#簿記の講師サイトから講師情報を抽出する

import requests
from bs4 import BeautifulSoup
import pprint
import pandas as pd

#ページ毎のtrタグを渡して講師情報をリストに格納する関数
def GetdataList(tr_tags):
    rowLis = []
    dataLis = []
    for i in range(4,24):
        rows = tr_tags[i].find_all('td')
        for row in rows:
            dataLis.append(row.text)
        rowLis.append(dataLis)
        dataLis=[]
    return rowLis

#URLを取得
List = [0, 20, 40, 60, 80]
trLis = []
SumLis = []
y = 0
for x in List:
    url = ('https://www.boki-teacher.com/tokyo/su3_list.cgi?'
        f'action=showlast&cat=&txtnumber=log&next_page={x}'
        '&t_type=list&sort=117&reverse=')

    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    tr_tags = soup.find_all('tr')

    #テーブル先頭行を取得（最初のページのみ）
    if x == 0:
        columnsLis = []
        tds = tr_tags[3].find_all('td') 
        for td in tds:
            columnsLis.append(td.text)

    trLis = GetdataList(tr_tags)#関数で講師情報のリスト取得
    SumLis.extend(trLis)#新しいリスト↑を蓄積

#リストをDataFrame化    
df = pd.DataFrame(SumLis,columns =columnsLis)
df = df.drop(['E-mail', 'No.'], axis=1)
df = df.rename(columns={'名前（ハンドルネーム）': 'Name'})

df_w = df[df['性別'] == '女性']#女性で抽出
df_w = df_w.sort_values('年齢')#年齢でソート

df_w.to_csv('Bokki.csv',encoding='shift-jis')
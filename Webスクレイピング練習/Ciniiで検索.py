#Ciniiで検索

import requests
import pprint
import pandas as pd
import readline

def main():
    word=input('検索キーワード：')
    # print(word)
    url='https://ci.nii.ac.jp/books/opensearch/search?format=json&q={word}&sortorder=3&count=100'
    res = requests.get(url)
    
    #例外を送出
    res.raise_for_status()
    
    books=res.json()
    # pprint.pprint(books)
    graph=books['@graph'][0]
    #書籍なしの場合の例外処理
    if 'items' not in graph.keys():
        print('該当書籍なし')
        return
    #Excelに必要なデータを出力
    df = pd.DataFrame(graph['items'])
    (df.loc[:,['title','dc:creator','dc:date']]
        .rename(columns={
            'title':'タイトル',
            'dc:creator':'著者名',
            'dc:date':'出版年',})
        .to_excel(f'{word}.xlsx'))
    # pd.set_option('display.max_columns',30)
    # print(df)

if __name__ == '__main__':
    main()

print('end')
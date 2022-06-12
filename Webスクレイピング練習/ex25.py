import shutil
import pandas as pd
from glob import glob
import pprint
from collections import defaultdict

def update_order(order,filepath):
    #注文読み込み
    df_order = pd.read_excel(filepath)
    for key,value in df_order.to_dict().items():
        order [key] += value[0]
    #ファイルの移動
    # shutil.move(filepath,'C://Users//hahih//Documents//MyPython//sources//order_old')
    return order

#注文表の読み込み
filepaths_order = glob('C://Users//hahih//Documents//MyPython//sources//order_new//order*.xlsx')
order = defaultdict(int)
for filepath in filepaths_order:
    order = update_order(order,filepath)

#在庫表の読み込み
filepath_stock = 'C://Users//hahih//Documents//MyPython//sources//stock.xlsx'
df_stock = pd.read_excel(filepath_stock)
stock = df_stock.iloc[-1:,2:]

#注文と在庫の差し引き
order = pd.DataFrame(order,index=[0], columns = stock.columns)
order = order.fillna(0)
stock = stock.reset_index(drop=True)
update = stock - order

pprint.pprint(update)
import pandas as pd
import openpyxl

#平均年収
url1='https://finance.yahoo.co.jp/stocks/ranking/averageIncome'
df1 = pd.read_html(url1)

#時価総額
url2='https://finance.yahoo.co.jp/stocks/ranking/marketCapitalHigh'
df2 = pd.read_html(url2)


with pd.ExcelWriter("data3.xlsx") as writer:
    df1[0][["順位","名称・コード・市場","平均年収(千円)","従業員数(単独)"]]\
        .to_excel(writer,encoding="SHIFT-JIS",sheet_name="平均年収")
    df2[0][["順位","名称・コード・市場","時価総額(百万円)","単元株数"]]\
        .to_excel(writer,encoding="SHIFT-JIS",sheet_name="時価総額")
print("end")
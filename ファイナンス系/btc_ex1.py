import datetime
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# データファイルを読み込みます。
data_file = open("C:\\Users\\hahih\\Documents\\MyPython\\sample.csv", "r", encoding="ms932", errors="", newline="" )
yomikomi_data = csv.reader(data_file, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)

# 読み込んだファイルをリスト形式に変換します。
#文字列を数値（int＆float）に変換します。
data = [ e for e in yomikomi_data ]
#print(data)
for row in data:
   row[1] = int(row[1])#始値
   row[2] = int(row[2])#高値
   row[3] = int(row[3])#安値
   row[4] = int(row[4])#終値
   row[5] = float(row[5])#出来高
rosoku_ashi = pd.DataFrame(data)
# print(rosoku_ashi)

#パラメータ ー
entry_kikan = int(input('エントリーの高値安値の値を入力して下さい。（半角数字/単位：時間）> '))
kessai_kikan = int(input('決済の安値高値の値を入力して下さい。（半角数字/単位：時間）> '))

#取引手数料（片道0.1%で設定）
cost_fee = 0.1*0.01

#スプレッドの設定（価格の0.02%を想定）
spread = 0.02*0.01

#スリッページの設定（価格の0.2%を想定）
slippage = 0.2*0.01

#各変数の定義と初期値
position = 0
price = 0
profit = 0
unrealized_profits = list()
realized_profits = list()
timestamps = list()
owarine_list = list()
win = list()
lose = list()
hold_times = list()
long_position = list()
short_position = list()
win_number = 0
loss_number = 0

#ここから検証のメインパート
for i in range(max(entry_kikan,kessai_kikan),len(rosoku_ashi)-1):
   saitakane_entry_kikan = max(rosoku_ashi[2][i-entry_kikan:i])
   saitakane_kessai_kikan = max(rosoku_ashi[2][i-kessai_kikan:i])
   saiyasune_entry_kikan = min(rosoku_ashi[3][i-entry_kikan:i])
   saiyasune_kessai_kikan = min(rosoku_ashi[3][i-kessai_kikan:i])
   owarine = rosoku_ashi[4][i]
   takane_rosoku_ashi = rosoku_ashi[2][i]
   yasune_rosoku_ashi = rosoku_ashi[3][i]
   #エントリーシグナル
   signal_buy_entry = owarine>saitakane_entry_kikan
   signal_sell_entry = owarine<saiyasune_entry_kikan 
   #手仕舞いシグナル
   long_position_exit = yasune_rosoku_ashi<saiyasune_kessai_kikan
   short_position_exit = takane_rosoku_ashi>saitakane_kessai_kikan
   timestamp = rosoku_ashi[0][i+1]
#    if timestamp == '2020/12/12 20:00':
#        print("stop")
#    else:
#        continue
   
   openprice = rosoku_ashi[1][i+1]
   
   if (position == -1 and short_position_exit) or (position == 1 and long_position_exit):
      hold_time = datetime.datetime.strptime(timestamp,'%Y-%m-%d %H:%M:%S')
      
      #ここの時間の設定おかしい　12/12 20：00から秒単位取得しない？？？　↑ココ5/7
      hold_times.append(hold_time.day)
      print("決済しました。時刻："+str(timestamp))
      print("保有時間："+str(hold_time))
      
      if position == -1 and short_position_exit:
          short_position.append(1)
          spread_cost = saitakane_kessai_kikan*spread
          slippage_cost = saitakane_kessai_kikan*slippage
          soneki = position*((saitakane_kessai_kikan + spread_cost) - price + slippage_cost) - cost_fee*(price + saitakane_kessai_kikan)
          profit += soneki
          print("決済額："+str(saitakane_kessai_kikan))
          print("損益："+str(soneki))
      if position == 1 and long_position_exit:
          long_position.append(1)
          spread_cost = saiyasune_kessai_kikan*spread
          slippage_cost = saiyasune_kessai_kikan*slippage
          soneki = position*(saiyasune_kessai_kikan - (price + spread_cost) - slippage_cost) - cost_fee*(price + saiyasune_kessai_kikan)
          profit += soneki
          print("決済額："+str(saiyasune_kessai_kikan))
          print("損益："+str(soneki))
      if soneki>0:
          win_number +=1
          win.append(soneki)
      else:
          loss_number +=1
          lose.append(soneki)
          
      position = 0

   if position == 0:
       if signal_buy_entry:
           position = 1
           price = openprice
           entry_time = timestamp
           print("買いエントリー！時刻："+str(timestamp))
           print("価格："+str(price))
       if signal_sell_entry:
           position = -1
           price = openprice
           entry_time = timestamp
           print("売りエントリー！時刻："+str(timestamp))
           print("価格："+str(price))

   unrealized_profits.append(profit+position*(owarine-price))
   realized_profits.append(profit)
   timestamps.append(timestamp)
   owarine_list.append(owarine)
date_label = list()

# 検証結果をグラフに表示します。
for i in range(0,len(timestamps)):
  # 日付と時刻に分割します。
  date, time  = timestamps[i].split()
  # ラベルを作成します。
  date_label.append(date)
x = np.arange(len(date_label))
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.plot(x,realized_profits,label='realized_profit')
ax.plot(x,unrealized_profits,label='unrealized_profit')
ax.plot(x,owarine_list,linestyle='dotted',label='BTC/JPY')
ax.set_ylabel("yen")
ax.set_xlabel("date")
plt.ticklabel_format(style='plain',axis='y')#指数表記しない設定にします。
ax.legend()
ax.grid(True)
#  X軸の間隔をあける&文字を回転させます。
plt.xticks(x[::1000], date_label[::1000], rotation=75)
# グラフが枠に納まるようにします。
plt.tight_layout()
# # グラフをpngファイルにします。
plt.savefig('entry_kikan' + str(entry_kikan)+'_kessai_kikan'+str(kessai_kikan)+'.png')
# グラフを表示します。
plt.show()
#最大ドローダウンを計算します。
drawdown = 0
drawdown_max = 0
assets_max=0
for i in range(0,len(unrealized_profits)):
  assets_max = max(assets_max,unrealized_profits[i])
  drawdown = assets_max - unrealized_profits[i]
  drawdown_max = max(drawdown_max,drawdown)

print(str(entry_kikan) + "時間の高値安値エントリー"+ str(kessai_kikan) + "時間の安値高値決済の検証結果")

# トレード回数
print('トレード回数',win_number+loss_number)

# 損益
print('損益(プロフィット）',profit)

# 最大ドローダウン
print('最大ドローダウン',drawdown_max)

# 勝率
if win_number+loss_number == 0:
    print('0で割るな')
else:
    print('勝率：'+str(100*win_number/(win_number+loss_number)) + '%')

# 平均利益
print('平均勝ちトレード',sum(win)/len(win))

# 平均損失
print('平均負けトレード',-sum(lose)/len(lose))

# 最大利益
print('最大勝ちトレード',max(win))

# 最大損失
print('最大負けトレード',-min(lose))

# PF
print('プロフィットファクター',-sum(win)/sum(lose))

#総保有時間
print('ポジション総保有期間(Day)',hold_times)
print('合計：' + str(sum(hold_times)) + '日')
120
#平均保有時間
print('ポジション平均保有期間(Day)',(sum(hold_times)+win_number+loss_number)/(win_number+loss_number))

#売り買い比率
print('買いエントリー回数',sum(long_position))
print('売りエントリー回数',sum(short_position))
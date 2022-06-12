import os
from matplotlib.axis import XAxis
import requests
import pprint
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Application(tkinter.Frame):
    def __init__(self,root=None):
        super().__init__(root,width=680,height=280)
        self.root=root
        self.pack()
        self.pack_propagate(0)
        self.create_widgets()
        
    def create_widgets(self):
        # テキストボックス
        self.text_box = tkinter.Entry(self)
        self.text_box['width']=10
        self.text_box.pack()
        
        #実行ボタン
        submit_btn=tkinter.Button(self)
        submit_btn['text']='実行'
        submit_btn['command']=self.display_graph
        submit_btn.pack()
        
        #グラフ
        plt.rcParams['font.size']=7
        self.fig,self.ax = plt.subplots(figsize=(12,4))
        self.canvas = FigureCanvasTkAgg(self.fig,master=self)
        self.canvas.get_tk_widget().pack()
        
    def display_graph(self):
        symbol = self.text_box.get()  
        api_key = os.environ['ALPHA_VANTAGE_KEY']
        
        #ｲﾝﾌﾟｯﾄﾎﾞｯｸｽからシンボルを入力する用
        url = 'https://www.alphavantage.co/query?'\
            f'function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}'
        
        #デバッグ用
        #url = 'https://www.alphavantage.co/query?'\
        #    f'function=TIME_SERIES_DAILY&symbol=MSFT&apikey={api_key}'
        
        data = requests.get(url).json()
        #breakpoint()
        pprint.pprint(data)
        #breakpoint()
        
        daily_data = dict(reversed(data['Time Series (Daily)'].items()))
        date_list = daily_data.keys()
        close_list = [float(x['4. close']) for x in daily_data.values()]
        
        self.ax.clear()         
        self.ax.plot(date_list,close_list)
        self.ax.xaxis.set_major_locator(mdates.DayLocator(interval=15))
        self.ax.grid()
        #fig.savefig('./stock.png') セーブ用
        self.canvas.draw()
    
def main():
    root=tkinter.Tk()
    root.title('株価監視app')
    root.geometry('700x300')
    app = Application(root=root)
    app.mainloop()
    
if __name__ == '__main__':
    main()
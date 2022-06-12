#CSVファイルを100個作るよ
import openpyxl

for i in range(1,101):
    book = openpyxl.Workbook()
    sheet=book.active
    hat_name= 'hat('+str(i)+')'
    sheet['A1']=hat_name
    sheet['B1']=10*i
    path = r'C:\\Users\\hahih\\Documents\\MyPython\\cata\\'
    book_name='cata(' + str(i) + ')' + '.xlsx'
    book.save(path + book_name)
    
print('end')
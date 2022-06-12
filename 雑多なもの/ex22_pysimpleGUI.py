import PySimpleGUI as sg

size=(10,5)
font=('meiryo',13)

layout = [
    [sg.FileBrowse('ファイル',font=font), sg.InputText(key='filePath',font=font)],
    [sg.FolderBrowse('フォルダ',font=font), sg.InputText(key='folderPath',font=font)],
    [sg.Text('3つの数字で計算します',font=font)],
    [sg.Radio('足し算',font=font, key = 'add', group_id='calc',default=True),
     sg.Radio('引き算',font=font, key = 'sub', group_id='calc'),
     sg.Radio('掛け算',font=font, key = 'multi', group_id='calc'),
     sg.Radio('割り算',font=font, key = 'div', group_id='calc')],
    [sg.Checkbox('入力1',font=font,key='C1',default=True), sg.InputText(default_text='1',font=font, key='I1')],
    [sg.Checkbox('入力2',font=font,key='C2',default=True), sg.InputText(default_text='10',font=font, key='I2')],
    [sg.Checkbox('入力3',font=font,key='C3',default=True), sg.InputText(default_text='100',font=font, key='I3')],
    # [sg.Multiline(default_text='MULTI',font=font)],
    [sg.Button('計算する',font=font,key='btn1')],
    [sg.Text('計算結果',font=font), sg.InputText(font=font,key='result')],
    [sg.Button(image_filename='KEDbtn.png', image_size=(400,400),key='btn2')]
]

window= sg.Window('楓が計算してやろう',layout)

while True:
    event,value = window.read()
    if event == None:
        break
    if event == 'btn1':
        i1 = bool(value['I1'])
        i2 = bool(value['I2'])
        i3 = bool(value['I3'])
        sum = 0
        
        if value['add'] == True:
            if value['C1'] == True:
                sum += i1
            if value['C2'] == True:
                sum += i2
            if value['C3'] == True:
                sum += i3
        if value['sub'] == True:
            if value['C1'] == True:
                sum -= i1
            if value['C2'] == True:
                sum -= i2
            if value['C3'] == True:
                sum -= i3
        if value['multi'] == True:
            if value['C1'] and value['C2']== True:
                sum = i1 * i2
            if value['C2'] and value['C3']== True:
                sum = i2 * i3
            if value['C1'] and value['C3'] == True:
                sum = i1 * i3
            if value['C1'] and value['C2'] and value['C3'] == True:
                sum = i1 * i2 * i3
        if value['div'] == True:
            if value['C1'] and value['C2']== True:
                sum = i1 / i2
            if value['C2'] and value['C3']== True:
                sum = i2 / i3
            if value['C1'] and value['C3'] == True:
                sum = i1 / i3
            if value['C1'] and value['C2'] and value['C3'] == True:
                sum = i1 / i2 / i3
                
        print(sum)
        window['result'].update(sum)

window.close
    
    
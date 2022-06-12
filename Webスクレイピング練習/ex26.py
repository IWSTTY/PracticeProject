from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
import pandas as pd

options = Options()
options.add_argument('--headless')

#URL
CrPh=r'C://Users//hahih//Documents//MyPython//chromedriver'
browser = webdriver.Chrome(CrPh)
# browser = webdriver.Chrome(CrPh,options=options)#ﾍｯﾄﾞﾚｽﾓｰﾄﾞ
browser.get('https://scraping-for-beginner.herokuapp.com/login_page')

## idとpw入力してログイン
elem_username = browser.find_element_by_id('userbirthday')
elem_username.send_keys('imanishi')

elem_password = browser.find_element_by_id('password')
elem_password.send_keys('kohei')

elem_login_btn = browser.find_element_by_id('login-btn')
elem_login_btn.click()

#情報取得（一括）
elems_th = browser.find_elements_by_tag_name('th')
keys = []
for elem_th in elems_th:
    key = elem_th.text
    keys.append(key)

elems_td = browser.find_elements_by_tag_name('td')
values = []
for elem_td in elems_td:
    value = elem_td.text
    values.append(value)

#CSV出力
df = pd.DataFrame()
df['項目'] = keys
df['値'] = values
df.to_csv('講師情報.csv',index=False, encoding='utf_8_sig')


# sleep(3)
# browser.quit()
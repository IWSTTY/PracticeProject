from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.alert import Alert

url = 'file:///C://Users//hahih//Documents//MyPython//coffee.html'

CrPh=r'C://Users//hahih//Documents//MyPython//chromedriver'
driver = webdriver.Chrome(CrPh)
driver.get(url)

# プルダウン要素からSelectインスタンスを取得
element = driver.find_element_by_name("num")
select_num = Select(element)
# select_by_value 等のメソッドで操作
select_num.select_by_value("2")
element = driver.find_element_by_xpath("/html/body/form/input[1]")
element.click()


chk_sugar = driver.find_element_by_css_selector("input[name='included'][value='sugar']")
chk_milk = driver.find_element_by_css_selector("input[name='included'][value='milk']")
chk_cream = driver.find_element_by_css_selector("input[name='included'][value='cream']")
chk_sugar.click()
chk_cream.click()
print(chk_milk.is_selected())
print(chk_cream.is_selected())
element = driver.find_element_by_name("remarks")
element.send_keys("やや熱めでお願いします")
time.sleep(1)
elements = driver.find_element_by_css_selector("input[type='submit']")
# elements = driver.find_element_by_css_selector("input[type='reset']")
elements.click()
# ドライバからAlertインスタンスを取得し、acceptメソッドでOK押下
Alert(driver).accept()


time.sleep(3)
driver.close()
driver.quit()
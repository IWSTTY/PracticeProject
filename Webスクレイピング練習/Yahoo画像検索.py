from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_path = 'C://Users//hahih//Documents//MyPython//chromedriver.exe'

options = Options()
options.add_argument('--incongnito')

driver = webdriver.Chrome(executable_path=chrome_path, options=options)

url ='https://search.yahoo.co.jp/image'
driver.get(url)

query = 'プログラミング'

search_box = driver.find_element_by_class_name("SearchBox__searchInput")
search_box.send_keys(query)
search_box.submit()


sleep(5)
driver.quit()
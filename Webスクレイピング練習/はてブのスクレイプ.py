# import requests
# from bs4 import BeautifulSoup
# import csv
# import re

# url="https://ja.wikipedia.org"

# response=requests.get(url)
# soup=BeautifulSoup(response.content,"html.parser")

# top_entry= soup.find("div",attrs={"id": "on_this_day"})
# entries= top_entry.find_all("li")
# today_list=[]

# for i,entry in enumerate(entries):
#     today_text = entry.get_text().replace("（","(").replace("）",")")
#     match = re.search("\(([1-9].*?)年\)",today_text)
    
#     #today_text = entry.get_text().replace("（","(").replace("）",")") 
#     #match = re.search("\(([ 1-9].*?) 年\)",today_text)

#     if match:
#         today_list.append([i+1,entry.get_text(),match.group(1)])
#     else:
#         today_list.append([i+1,entry.get_text()])
    
# with open("output2.csv","w",encoding="shift_JIS") as file:
#     writer = csv.writer(file,lineterminator="\n")
#     writer.writerows(today_list)

# -----------------------------------------------------------------
import requests
from bs4 import BeautifulSoup
import csv
import re

url="https://b.hatena.ne.jp"

response=requests.get(url)
soup=BeautifulSoup(response.content,"html.parser")

top_entry=soup.find("section",attrs={"class": "entrylist-unit"})
entries=top_entry.find_all("div",attrs={"class": "entrylist-contents"})

#人気記事のブロックをループ処理してタイトルを取得
for entry in entries:
    title_tag = entry.find("h3",attrs={"class": "entrylist-contents-title"})
    title = title_tag.find("a").get("title")
    print(title)
    
    bookmark_tag=entry.find("span",attrs={"class": "entrylist-contents-users"})
    bookmark_link=bookmark_tag.find("a").get("href") 
    bookmark_url=url+bookmark_link
    response=requests.get(bookmark_url)
    soup=BeautifulSoup(response.content,"html.parser")
    comments=soup.find_all("span",attrs={"class": "entrylist-comment-text"})
    
    for comment in comments:
        print(comment.get_text())

print('end')
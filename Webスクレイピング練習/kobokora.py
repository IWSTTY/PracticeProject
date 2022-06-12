#コボコラ画像を一括で抽出し、フォルダ保存

from genericpath import exists
from urllib import response
import requests
from bs4 import BeautifulSoup
import urllib
from pathlib import Path
import uuid

output_folder=Path("コボコラまとめ")
output_folder.mkdir(exist_ok=True)

url="https://matome.eternalcollegest.com/post-2148680035897592301"
response=requests.get(url)
soup=BeautifulSoup(response.content,"html.parser")

content=soup.find("div",attrs={"id":"container"})
#content=soup.find("div",attrs={"class":"n-img"})
images = content.find_all("img")

image_list=[]
for image in images:
    
    if "data-src" in str(image):
        long_image_url=urllib.parse.urljoin(url,image["data-src"])
    elif "imgsrc" in str(image):
        long_image_url=urllib.parse.urljoin(url,image["imgsrc"])
    elif "src" in str(image):
        long_image_url=urllib.parse.urljoin(url,image["src"])
    else:
        continue        
    image_data=requests.get(long_image_url)
    image_list.append(long_image_url)
    with open(str("./コボコラまとめ/")+str(uuid.uuid4())+str(".jpeg"),"wb") as file:
        file.write(image_data.content)
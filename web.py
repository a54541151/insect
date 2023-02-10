import requests
from bs4 import BeautifulSoup

r = requests.get("https://www.ptt.cc/bbs/MobileComm/index.html")
# print(r.text)


soup = BeautifulSoup(r.text,"html.parser")
# print(soup)

# sel = soup.select("div.nrec span")  #div class裡面的nrec裡面的span
sel = soup.select("div.nrec span")
# print(sel)

for s in sel:
    print(s["class"]," : ",s.text)  #印出class
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~")
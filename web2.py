import requests
from bs4 import BeautifulSoup
import sys
import pymongo

articles = []
errors = []
last_page_link = ""
time = 0

if int(sys.argv[1]) > 5000 :
    time = 5000
else :
    time = int(sys.argv[1])

def capData() :
    r = requests.get("https://www.ptt.cc/bbs/joke/index.html")
    
    global time
    while time > 0:
        
        soup = BeautifulSoup(r.text,"html.parser")
        index_soup = soup.select("div.title a")

        last_page_soup = soup.select("a.btn")


        for l in last_page_soup:
            if "‹ 上頁" == l.text  :
                last_page_link = l["href"]
                

        for i in index_soup:
            r = requests.get("https://www.ptt.cc"+i["href"])
            
            soup = BeautifulSoup(r.text,"html.parser")
            
            article_meta_vlaue_soup = soup.select("span.article-meta-value")

            
            article_main_content_soup = soup.select("div#main-content")

            
            article_comment_soup = soup.select("div.push")


            
            start = 0
            end = article_main_content_soup[0].text.find("--\n※ 發信站")

            
            content = article_main_content_soup[0].text[start:end]

            n = 0 
            while n < len(content) :
                if content[n] == "時" and content[n+1] == "間" :
                    start = n + 27
                    break
                n += 1

                    
            content = article_main_content_soup[0].text[start:end]

            try :
                article = {
                    "author" :  article_meta_vlaue_soup[0].text,
                    "title" :  article_meta_vlaue_soup[2].text,
                    "date" :  article_meta_vlaue_soup[3].text,
                    "content" : content,
                    "comments" : str(article_comment_soup),
                    "link" : "https://www.ptt.cc"+i["href"]
                }

                articles.append(article)
            except :
                errors.append("https://www.ptt.cc"+i["href"])

        r = requests.get("https://www.ptt.cc"+last_page_link)
        time -= 1
        print(time)
        #print(len(article_link))

def saveToDB() :
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")

    mydb = myclient["愛愛"]

    mycol = mydb["要愛愛"]
    
    mycol.drop()

    mycol.insert_many(articles)

def main() :
    capData()
    saveToDB()
    print("Total articles : " + str(len(articles)))
    
    print("Total errors : " + str(len(errors)))
    
if __name__ == '__main__':
    main()
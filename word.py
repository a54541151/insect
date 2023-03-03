import jieba
import jieba.analyse
import pymongo


articles = []

def loadNewWordToJeiba():
    lines = []
    with open('word.txt', encoding="utf-8") as f:
        lines = f.readlines()

    n = 0
    while n < len(lines) :
        lines[n] = lines[n].replace("\n", "")
        n += 1
    
    for line in lines :
        jieba.add_word(line)

def cut(article):
    #print(a["_id"])
    seg_list = jieba.cut(article["content"], cut_all=False)
    #print("Default Mode: " + "/ ".join(seg_list))

    tfidf_list = jieba.analyse.extract_tags(article["content"], topK=20, withWeight=False, allowPOS=())

    #print(tfidf_list)

    return tfidf_list


def getFromDB() :
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")

    mydb = myclient["鬼怪"]

    mycol = mydb["鬼怪愛愛"]

    for x in mycol.find():
        articles.append(x)


def saveToDB() :
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")

    mydb = myclient["鬼怪"] #雲端資料夾

    mycol = mydb["鬼怪愛愛"] #雲端資料夾內名稱

    for article in articles :
        tfidf_list = cut(article)
        myquery = { "_id": article["_id"] }
        newvalues = { "$set": { "tfidf": tfidf_list } }

        mycol.update_one(myquery, newvalues)
    print('done')

def main() :
    loadNewWordToJeiba()
    getFromDB()
    saveToDB()
    
if __name__ == '__main__':
    main()
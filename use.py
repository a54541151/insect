import gensim



model = gensim.models.Word2Vec.load("word2vec.zh.300.model")


# print(model.wv.vectors.shape)

# print(model.wv.vectors)


# print(model.wv.most_similar("伍哥"))  #自動找出關鍵字前10,找不到會跑出Keyerror

# words = list(model.wv.index_to_key)

# print(f"總共收錄了 {len(words)} 個詞彙")

# print("印出 10 個收錄詞彙:")
# print(words[:10])


#查找文中有無關鍵字
# word = "Jason蕭"

# try:
#     vec = model.wv[word]
# except KeyError as e:
#     print(e)
##############################

    
print(model.wv.most_similar("大奶", topn=10)) #找關鍵字前10名


print(model.wv.similarity("致理", "大奶")) #找兩個關鍵字相關的詞彙
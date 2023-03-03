from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage
)

import pymongo

import gensim

from dotenv import load_dotenv
import os
import time
    
start = int( time.time() )
print("loading model")
model = gensim.models.Word2Vec.load("word2vec.zh.300.model")
end = int( time.time() )
print("done")
print("total used "+ str( end - start ) + "s" )


load_dotenv()
CHANNEL_ACCESS_TOKEN = os.environ["CHANNEL_ACCESS_TOKEN"]
CHANNEL_SECRECT = os.environ["CHANNEL_SECRECT"]

app = Flask(__name__)

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRECT)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")

    mydb = myclient["鬼怪"]

    mycol = mydb["鬼怪愛愛"]

    targets = event.message.text.split(" ")

    """
    for target in targets :
        try:
            words = model.wv.most_similar(target, topn=3)
            for word in words :
                targets.append(word[0])
        except KeyError as e:
            print(e)
    """

    await_words = []
    for target in targets :
        try:
            words = model.wv.most_similar(target, topn=3)
            for word in words :
                await_words.append(word[0])
        except KeyError as e:
            print(e)
    
    targets = targets + await_words

    targets = list(dict.fromkeys(targets))

    print(targets)

    relpy_text = ""

    myquery = { "tfidf": { "$in": targets } }

    n = 0
    for match in mycol.find(myquery) :
        print(match["title"])
        relpy_text = relpy_text + '\n'+ str(n) + ' : ' + match["title"] + '\n' + match["link"]
        n += 1

    if len(relpy_text) == 0 :
        relpy_text = "什麼都找不到... QQ"

    try_to_find = ""

    n = 0
    while n < len(targets) :
        if n + 1 != len(targets) :
            try_to_find = try_to_find + targets[n] + ", "
        else :
            try_to_find = try_to_find + targets[n]
        n += 1

    relpy_text = "嘗試幫你找有關{" + try_to_find + "}的文章,結果如下\n\n" + relpy_text

    line_bot_api.reply_message(
    event.reply_token,
    TextMessage(text=relpy_text),
    )

if __name__ == "__main__":
    app.run()
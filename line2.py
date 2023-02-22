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

from dotenv import load_dotenv
import os

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

    mydb = myclient["ptt"]

    mycol = mydb["mobel"]

    x = event.message.text.split(" ")

    myquery = { "tfidf": { "$in": x } }

    article = []
    text = ""

    n = 0
    for match in mycol.find(myquery) :
        print(match["title"])
        article.append(match)
        text = text + '\n'+ str(n) + ' : ' + match["title"] + '\n' + match["link"]
        #n += 1


    line_bot_api.reply_message(
    event.reply_token,
    TextSendMessage(text=text),
    )

if __name__ == "__main__":
    app.run()
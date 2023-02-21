from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)


app = Flask(__name__)

line_bot_api = LineBotApi('40arE0O50T4TfiFBif5CsDljPDebfLQjvsXiwHYm4+f1gx7Igha95IMY50eqV2850sFBE2w3xvx/gT0rzHCs2prZlHV9DKpzRYhue7oQT4EJtSNT4lGpG1JjPkjonjwZmP2ElpIFhVgmL5AnuqofVQdB04t89/1O/w1cDnyilFU=')
#Channel access token
handler = WebhookHandler('df7e636961ed250bd0a818031433f926')
#Channel secret


@app.route("/callback", methods=['POST'])
def callback():  #網路鉤子Webhook URL
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

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
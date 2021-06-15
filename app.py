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

# Channel Access Token
line_bot_api = LineBotApi('zHqY7wgjPMPbbBMpFHetuOnQtI/8hVDqoQM76ROnl8bo9Ohb1J5TL0tCo9dLBdBT55flNlOBbgtj9jaHUdaDB/kf4JYC/pmc+m/NtTjvcw3EOhUoZjv2oayYlIzl2Sar2bNwVyV+GH+oSA6+MUzTyQdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('5b272c42a50a09305322425eae56cabb')


# 監聽所有來自 /callback 的 Post Request
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
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    text=event.message.text

    if (text=="Hi"):
        reply_text = "Hello"
    elif(text=="你好"):
        reply_text = "哈囉"
    elif(text=="機器人"):
        reply_text = "叫我嗎"
    elif(text=="only one of cp"):
        reply_text = "申燁、九愛"
    else:
        reply_text = text
#如果非以上的選項，就會學你說話

    message = TextSendMessage(reply_text)
    line_bot_api.reply_message(event.reply_token, message)

   

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    
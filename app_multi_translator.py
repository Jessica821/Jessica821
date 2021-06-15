from flask import Flask, request, abort

from translate import Translator

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
line_bot_api = LineBotApi('/CDXHuipQ26DRyQCpxGZk4JnwyP0IIbR+1Nw9NVHbBVrX2cgP5yEXypMXdy9rcTL55flNlOBbgtj9jaHUdaDB/kf4JYC/pmc+m/NtTjvcw00vj0KeTGM6nzXLh3mgr3JtZb4GyiR9pNatVu0mwimNAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('5b272c42a50a09305322425eae56cabb')




#translator = Translator (from_lang='zh-Hant', to_lang='en')
lang='en'


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
    global lang
    if event.message.text == "中翻英":
        msg = TextSendMessage(text = '語言設定為英文') 
        lang = 'en'
    elif event.message.text == "中翻日":
        msg =  TextSendMessage(text = '語言設定為日文')
        lang='ja'
    elif event.message.text == "中翻韓":
        msg =  TextSendMessage(text = '語言設定為韓文')
        lang='ko'
    else:
        translator = Translator (from_lang='zh-Hant', to_lang=lang)
        msg =  TextSendMessage(text = translator.translate(event.message.text))     
    line_bot_api.reply_message(event.reply_token, msg)




# requirements.txt 中要加入 translate , 也就是要 pip install traslate
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    
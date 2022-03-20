from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerSendMessage
)

app = Flask(__name__)

line_bot_api = LineBotApi('7zPdP7HOYVrMBU8MIx9k3Th+SnHC24iAA+V6wfi0T/qmNEHAYqE2IfbZbDRWrX3491AbL2PmclxCkoaqff+yasZxhdZkzsZME2QG6Oqg5IZ28aDefWeSEj1LIE6JXCUZPnR370/KDOr0d/tXfVaFqgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('32559a05287b5497b52612826f7d75b7')


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
    msg = event.message.text
    r = "很抱歉，你說什麼"

    if "給我貼圖" in msg:
        sticker_message = StickerSendMessage(
            package_id='1',
            sticker_id='1'
        )

        line_bot_api.reply_message(
            event.reply_token,
            sticker_message)

        return

    if msg in ["hi", "Hi"]:
        r = "嗨"
    elif msg == "你吃飯了嗎":
        r = "還沒"
    elif msg == "你是誰":
        r = "我是機器人"
    elif "訂位" in msg:
        r = "您想訂位，是嗎?" 


    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


if __name__ == "__main__":
    app.run()
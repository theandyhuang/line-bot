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
    s = "你吃飯了嗎?"
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=msg))


if __name__ == "__main__":
    app.run()
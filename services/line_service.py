from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    ApiClient, 
    MessagingApi, 
    Configuration, 
    ReplyMessageRequest
)
from routes.route import route_map
from core.config import settings
from linebot.v3 import WebhookHandler
from linebot.v3.webhooks import MessageEvent, TextMessageContent

configuration = Configuration(access_token=settings.ACCESS_TOKEN)
handler = WebhookHandler(channel_secret=settings.CHANNEL_SECRET)

from fastapi import HTTPException


async def callback(body, x_line_signature):
    body_str = body.decode('utf-8')
    try:
        handler.handle(body_str, x_line_signature)
    except InvalidSignatureError:
        print("Invalid signature.")
        raise HTTPException(status_code=400, detail="Invalid signature.")

    return 'OK'

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    user_text = event.message.text.strip()
    reply_text = None
    parts = user_text.split(" ")
    command = parts[0]
    args = parts[1:]
    handler_func = route_map.get(command)
    if handler_func:
        try:
            reply_text = handler_func(*args)
        except Exception as e:
            reply_text = None
            return None
    
    if reply_text != None:
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[reply_text]
                )
            )
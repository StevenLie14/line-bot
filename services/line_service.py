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
import asyncio


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
    parts = user_text.split(" ")
    command = parts[0]
    args = parts[1:]
    handler_func = route_map.get(command)
    print(command, args)

    if handler_func:
        try:
            if asyncio.iscoroutinefunction(handler_func):
                asyncio.create_task(
                    run_async_handler(handler_func, args, event)
                )
            else:
                reply_text = handler_func(*args)
                send_reply(event.reply_token, reply_text)
        except Exception as e:
            print(f"Error in handler_func: {e}")
            return None

def send_reply(reply_token, reply_text):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=reply_token,
                messages=[reply_text]
            )
        )

async def run_async_handler(handler_func, args, event):
    try:
        reply_text = await handler_func(*args)
        if reply_text is not None:
            send_reply(event.reply_token, reply_text)
    except Exception as e:
        print(f"Error in async handler: {e}")
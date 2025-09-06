from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    ApiClient, 
    MessagingApi, 
    Configuration, 
    ReplyMessageRequest,
    TextMessageV2,
    PushMessageRequest
)
from routes.route import ROUTE_MAPS
from core.config import settings
from linebot.v3 import WebhookHandler
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from utils.helper import parse_user_command
import asyncio
import inspect


configuration = Configuration(access_token=settings.LINE_ACCESS_TOKEN)
handler = WebhookHandler(channel_secret=settings.LINE_CHANNEL_SECRET)

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
    command = parse_user_command(event.message.text)
    handler_func = ROUTE_MAPS.get(command)
    print(event)

    if handler_func:
        try:
            if asyncio.iscoroutinefunction(handler_func):
                asyncio.create_task(
                    run_async_handler(handler_func, event)
                )
            else:
                reply_text = None
                if "event" in inspect.signature(handler_func).parameters:
                    reply_text = handler_func(event=event)
                else:
                    reply_text = handler_func()
                if reply_text is not None:
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
        
def send_message(id, messages: list[TextMessageV2]):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.push_message(
            push_message_request=PushMessageRequest(to=id,messages=messages)
        )

async def run_async_handler(handler_func, event):
    try:
        reply_text = None
        if "event" in inspect.signature(handler_func).parameters:
            reply_text = await handler_func(event=event)
        else:
            reply_text = await handler_func()
        if reply_text is not None:
            send_reply(event.reply_token, reply_text)
    except Exception as e:
        print(f"Error in async handler: {e}")
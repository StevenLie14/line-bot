import asyncio
import inspect
from fastapi import HTTPException
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    ApiClient,
    MessagingApi,
    Configuration,
    ReplyMessageRequest,
    TextMessageV2,
    PushMessageRequest,
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from routes import LineRouteRegistry
from core import settings
from utils import Helper


class LineService:
    def __init__(self, route_registry: LineRouteRegistry):
        self.configuration = Configuration(access_token=settings.LINE_ACCESS_TOKEN)
        self.handler = WebhookHandler(channel_secret=settings.LINE_CHANNEL_SECRET)
        self.route_registry = route_registry
        self._register_handlers()

    async def callback(self, body, x_line_signature: str):
        body_str = body.decode("utf-8")
        try:
            self.handler.handle(body_str, x_line_signature)
        except InvalidSignatureError:
            raise HTTPException(status_code=400, detail="Invalid signature.")
        return "OK"

    def _register_handlers(self):
        @self.handler.add(MessageEvent, message=TextMessageContent)
        def handle_message(event):
            command = Helper.parse_user_command(event.message.text)
            handler_func = self.route_registry.get_route(command)
            print(f"Received event: {event}")

            if handler_func is None:
                return

            try:
                if asyncio.iscoroutinefunction(handler_func):
                    asyncio.create_task(self._run_async_handler(handler_func, event))
                else:
                    reply_text = self._call_sync_handler(handler_func, event)
                    if reply_text is not None:
                        self.send_reply(event.reply_token, reply_text)
            except Exception as e:
                print(f"Error in handler_func: {e}")

    def _call_sync_handler(self, handler_func, event):
        if "event" in inspect.signature(handler_func).parameters:
            return handler_func(event=event)
        return handler_func()

    async def _run_async_handler(self, handler_func, event):
        try:
            if "event" in inspect.signature(handler_func).parameters:
                reply_text = await handler_func(event=event)
            else:
                reply_text = await handler_func()
            if reply_text is not None:
                self.send_reply(event.reply_token, reply_text)
        except Exception as e:
            print(f"Error in async handler: {e}")

    def send_reply(self, reply_token, reply_text: TextMessageV2):
        with ApiClient(self.configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            line_bot_api.reply_message(
                ReplyMessageRequest(reply_token=reply_token, messages=[reply_text])
            )

    def send_message(self, id: str, messages: list[TextMessageV2]):
        with ApiClient(self.configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            line_bot_api.push_message(
                push_message_request=PushMessageRequest(to=id, messages=messages)
            )

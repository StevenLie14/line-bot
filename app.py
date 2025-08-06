from fastapi import FastAPI, HTTPException
import uvicorn
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException, Header
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from linebot.v3.messaging import (
    ApiClient, 
    MessagingApi, 
    Configuration, 
    ReplyMessageRequest, 
    TextMessageV2, MentionSubstitutionObject, AllMentionTarget
)

from linebot.v3.messaging.models import TextMessageV2

app = FastAPI(title="Bot API")
load_dotenv(override=True)


get_access_token = os.getenv('ACCESS_TOKEN')
configuration = Configuration(access_token=get_access_token)
get_channel_secret = os.getenv('CHANNEL_SECRET')
handler = WebhookHandler(channel_secret=get_channel_secret)

@app.post("/callback")
async def callback(request: Request, x_line_signature: str = Header(None)):
    body = await request.body()
    print(body)
    body_str = body.decode('utf-8')
    try:
        handler.handle(body_str, x_line_signature)
    except InvalidSignatureError:
        print("Invalid signature.")
        raise HTTPException(status_code=400, detail="Invalid signature.")

    return 'OK'

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event: MessageEvent):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        print(event)

        message = TextMessageV2(
            text="Maklo, {everyone}!",
            substitution={
                "everyone": MentionSubstitutionObject(
                    mentionee=AllMentionTarget(type="all")
                )
            }
        )

        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[message]
            )
        )

@app.get("/")
def read_root():
    return {"message": "Hello RnD!"}


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
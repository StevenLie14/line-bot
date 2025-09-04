import uvicorn
from fastapi import FastAPI
from controllers.line_controller import router
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from contextlib import asynccontextmanager
from repositories import request_repository

scheduler = AsyncIOScheduler()

@scheduler.scheduled_job("cron",hour="12",minute="47",second="30")
async def test():
    data = await request_repository.get_active_request()
    print(data)

@asynccontextmanager
async def lifespan(_:FastAPI):
    print("Starting scheduler")
    
    scheduler.start()
    yield
    print("Stopping scheduler")
    scheduler.shutdown(wait=False)

app = FastAPI(title="Bot API",lifespan=lifespan)

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
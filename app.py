import uvicorn
from fastapi import FastAPI
from controllers.line_controller import router
from controllers.request_controller import router as request_router
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from contextlib import asynccontextmanager
from repositories import request_repository
from fastapi.routing import APIRoute

scheduler = AsyncIOScheduler()

@scheduler.scheduled_job("cron",hour="7",minute="20",second="0")
async def reminder_job():
    data = await request_repository.get_active_request()
    print(data)

@asynccontextmanager
async def lifespan(_:FastAPI):
    print("Starting scheduler")
    
    scheduler.start()
    yield
    print("Stopping scheduler")
    scheduler.shutdown(wait=False)

app = FastAPI(title="Bot API",lifespan=lifespan,root_path="/line")

app.include_router(router)
app.include_router(request_router)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
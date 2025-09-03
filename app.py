import uvicorn
from fastapi import FastAPI
from controllers.line_controller import router

from apscheduler.schedulers.background import BackgroundScheduler
from contextlib import asynccontextmanager

def test():
    print("halo")
@asynccontextmanager
async def lifespan(_:FastAPI):
    print("Starting scheduler")
    scheduler = BackgroundScheduler()
    scheduler.add_job(id="reminder_request",func=test, trigger="interval",seconds=10)
    scheduler.start()
    yield
    print("Stopping scheduler")
    scheduler.shutdown(wait=False)

app = FastAPI(title="Bot API",lifespan=lifespan)

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
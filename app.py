import uvicorn
from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from contextlib import asynccontextmanager
from controllers import GroupController, UserController, LineController, RequestController, ResmanController
from routes import LineRouteRegistry
from services import LineService, GroupService, UserService, RequestService, ResmanService
from repositories import GroupRepository, UserRepository, RequestRepository, ResmanRepository
from core import settings

line_route_registry = LineRouteRegistry()

group_repository = GroupRepository()
user_repository = UserRepository()
request_repository = RequestRepository()
resman_repository = ResmanRepository()

line_service = LineService(line_route_registry)
group_service = GroupService(group_repository)
user_service = UserService(user_repository, resman_repository, group_repository)
request_service = RequestService(request_repository, line_service, user_service, group_repository)
resman_service = ResmanService(resman_repository)

line_controller = LineController(line_service)
group_controller = GroupController(group_service)
user_controller = UserController(user_service)
request_controller = RequestController(request_service)
resman_controller = ResmanController(resman_service)

line_route_registry.register_routes(line_controller.get_routes())
line_route_registry.register_routes(group_controller.get_routes())
line_route_registry.register_routes(user_controller.get_routes())
line_route_registry.register_routes(request_controller.get_routes())
line_route_registry.register_routes(resman_controller.get_routes())

scheduler = AsyncIOScheduler()

@scheduler.scheduled_job("cron",hour="7",minute="20",second="0")
async def reminder_job():
    await request_controller.get_active_tickets()

@asynccontextmanager
async def lifespan(_:FastAPI):
    print("Starting scheduler")
    
    scheduler.start()
    yield
    print("Stopping scheduler")
    scheduler.shutdown(wait=False)


app = FastAPI(title="Bot API",lifespan=lifespan,root_path="/line")

app.include_router(request_controller.router)
app.include_router(line_controller.router)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
import uvicorn
from fastapi import FastAPI
from controllers.line_controller import router
app = FastAPI(title="Bot API")

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
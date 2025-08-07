from fastapi import APIRouter
from fastapi import Request, Header
from services import line_service


router = APIRouter()

@router.post("/callback")
async def callback(request: Request, x_line_signature: str = Header(None)):
    body = await request.body()
    return await line_service.callback(body, x_line_signature)
    

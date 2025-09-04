from pydantic import BaseModel

class User(BaseModel):
    id: str
    initial: str
    name: str

    
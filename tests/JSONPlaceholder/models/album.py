from pydantic import BaseModel


class Album(BaseModel):
    userId: int
    id: int
    title: str

from pydantic import BaseModel


class Comment(BaseModel):
    postId: int
    id: int
    name: str
    email: str
    body: str

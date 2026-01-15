from pydantic import BaseModel, HttpUrl


class Photo(BaseModel):
    albumId: int
    id: int
    title: str
    url: HttpUrl
    thumbnailUrl: HttpUrl

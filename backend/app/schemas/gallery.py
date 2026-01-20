from pydantic import BaseModel
from datetime import datetime

class AlbumCreate(BaseModel):
    name: str
    visibility: str = "public"

class AlbumOut(BaseModel):
    id: int
    name: str
    visibility: str
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True

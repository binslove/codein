from pydantic import BaseModel
from datetime import datetime

class PostCreate(BaseModel):
    title: str
    content: str

class PostOut(BaseModel):
    id: int
    title: str
    content: str
    board_id: int
    author_id: int
    view_count: int
    is_pinned: bool
    created_at: datetime

    class Config:
        from_attributes = True

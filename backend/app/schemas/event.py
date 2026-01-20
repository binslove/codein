from pydantic import BaseModel
from datetime import datetime

class EventCreate(BaseModel):
    title: str
    description: str
    start_time: datetime
    end_time: datetime

class EventOut(BaseModel):
    id: int
    title: str
    description: str
    start_time: datetime
    end_time: datetime
    owner_id: int

    class Config:
        from_attributes = True

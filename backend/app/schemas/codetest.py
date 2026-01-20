from pydantic import BaseModel
from datetime import datetime

class TestCreate(BaseModel):
    title: str
    start_time: datetime
    end_time: datetime

class ProblemCreate(BaseModel):
    title: str
    description: str
    answer: str

class SubmissionCreate(BaseModel):
    code: str

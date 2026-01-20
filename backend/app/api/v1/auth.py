from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token
from app.db.session import async_session
from pydantic import BaseModel, EmailStr, Field

router = APIRouter()

class Register(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)
    name: str
    student_id: str
    major: str
    generation: str

@router.post("/register")
async def register(data: Register):
    async with async_session() as db:
        res = await db.execute(select(User).where(User.email == data.email))
        if res.scalar_one_or_none():
            raise HTTPException(400, "Email exists")
        user = User(
            email=data.email,
            hashed_password=hash_password(data.password),
            name=data.name,
            student_id=data.student_id,
            major=data.major,
            generation=data.generation,
        )
        db.add(user)
        await db.commit()
        return {"status": "created"}

@router.post("/login")
async def login(data: Register):
    async with async_session() as db:
        res = await db.execute(select(User).where(User.email == data.email))
        user = res.scalar_one_or_none()
        if not user or not verify_password(data.password, user.hashed_password):
            raise HTTPException(401, "Invalid credentials")
        return {
            "access_token": create_access_token({"sub": str(user.id)}),
            "refresh_token": create_refresh_token({"sub": str(user.id)}),
        }

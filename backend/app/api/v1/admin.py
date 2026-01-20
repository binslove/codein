from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.core.deps import get_db, require_roles
from app.models.user import User
from app.models.board import Post
from app.models.codetest import Submission

router = APIRouter(dependencies=[Depends(require_roles("admin","superadmin"))])

@router.get("/stats")
async def stats(db: AsyncSession = Depends(get_db)):
    users = (await db.execute(select(func.count(User.id)))).scalar()
    posts = (await db.execute(select(func.count(Post.id)))).scalar()
    submissions = (await db.execute(select(func.count(Submission.id)))).scalar()
    return {
        "users": users,
        "posts": posts,
        "submissions": submissions
    }

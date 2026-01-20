from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.deps import get_db
from app.models.board import Post
from app.models.gallery import Album
from app.models.event import Event

router = APIRouter()

@router.get("/")
async def search(q: str, db: AsyncSession = Depends(get_db)):
    posts = (await db.execute(select(Post).where(Post.title.contains(q)))).scalars().all()
    albums = (await db.execute(select(Album).where(Album.name.contains(q)))).scalars().all()
    events = (await db.execute(select(Event).where(Event.title.contains(q)))).scalars().all()

    return {
        "posts": posts,
        "albums": albums,
        "events": events
    }

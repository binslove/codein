from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.deps import get_db, get_current_user
from app.models.board import Post, Board
from app.schemas.board import PostCreate, PostOut

router = APIRouter()

@router.post("/{board_id}", response_model=PostOut)
async def create_post(
    board_id: int,
    data: PostCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    post = Post(
        title=data.title,
        content=data.content,
        board_id=board_id,
        author_id=user.id,
    )
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return post

@router.get("/{board_id}")
async def list_posts(board_id: int, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Post).where(Post.board_id == board_id))
    return res.scalars().all()

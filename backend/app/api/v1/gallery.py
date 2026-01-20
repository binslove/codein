from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import os, uuid
from app.core.deps import get_db, get_current_user
from app.models.gallery import Album, Photo
from app.schemas.gallery import AlbumCreate, AlbumOut

router = APIRouter()

MEDIA_ROOT = "media"
os.makedirs(MEDIA_ROOT, exist_ok=True)

@router.post("/albums", response_model=AlbumOut)
async def create_album(data: AlbumCreate, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    album = Album(name=data.name, visibility=data.visibility, owner_id=user.id)
    db.add(album)
    await db.commit()
    await db.refresh(album)
    return album

@router.post("/albums/{album_id}/photos")
async def upload_photo(
    album_id: int,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    ext = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    path = os.path.join(MEDIA_ROOT, filename)

    with open(path, "wb") as f:
        f.write(await file.read())

    photo = Photo(album_id=album_id, url=path, thumbnail_url=path)
    db.add(photo)
    await db.commit()
    return {"url": path}

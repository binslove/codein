from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.deps import get_db, get_current_user
from app.models.event import Event, Attendance
from app.schemas.event import EventCreate, EventOut

router = APIRouter()

@router.post("/", response_model=EventOut)
async def create_event(data: EventCreate, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    event = Event(
        title=data.title,
        description=data.description,
        start_time=data.start_time,
        end_time=data.end_time,
        owner_id=user.id,
    )
    db.add(event)
    await db.commit()
    await db.refresh(event)
    return event

@router.post("/{event_id}/attend")
async def attend_event(event_id: int, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    attend = Attendance(event_id=event_id, user_id=user.id, status="attending")
    db.add(attend)
    await db.commit()
    return {"status": "attending"}

@router.get("/")
async def list_events(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Event))
    return res.scalars().all()

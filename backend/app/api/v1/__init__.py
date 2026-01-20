from fastapi import APIRouter
from app.api.v1 import auth, boards, gallery, events, codetest, admin, search

router = APIRouter()
router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(boards.router, prefix="/boards", tags=["boards"])
router.include_router(gallery.router, prefix="/gallery", tags=["gallery"])
router.include_router(events.router, prefix="/events", tags=["events"])
router.include_router(codetest.router, prefix="/codetest", tags=["codetest"])
router.include_router(admin.router, prefix="/admin", tags=["admin"])
router.include_router(search.router, prefix="/search", tags=["search"])

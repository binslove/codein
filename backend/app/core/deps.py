from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

from app.core.config import settings
from app.db.session import async_session
from app.models.user import User

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


# Bearer 토큰(Authorization: Bearer <token>)을 읽는다.
# auto_error=False로 해두면 토큰이 없을 때 우리가 "Missing token"을 직접 띄울 수 있음.
bearer_scheme = HTTPBearer(auto_error=False)


async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db),
):
    token = credentials.credentials if credentials else None
    if not token:
        raise HTTPException(status_code=401, detail="Missing token")

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    res = await db.execute(select(User).where(User.id == int(user_id)))
    user = res.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


def require_roles(*roles):
    async def guard(user=Depends(get_current_user)):
        if user.role not in roles:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user

    return guard


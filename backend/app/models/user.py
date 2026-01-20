from sqlalchemy import String, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)

    name: Mapped[str] = mapped_column(String)
    student_id: Mapped[str] = mapped_column(String)
    major: Mapped[str] = mapped_column(String)
    generation: Mapped[str] = mapped_column(String)

    role: Mapped[str] = mapped_column(String, default="member")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

from sqlalchemy import String, Integer, Text, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.models.base import Base

class Board(Base):
    __tablename__ = "boards"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    is_public: Mapped[bool] = mapped_column(Boolean, default=True)

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String)
    content: Mapped[str] = mapped_column(Text)

    board_id: Mapped[int] = mapped_column(ForeignKey("boards.id"))
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    is_pinned: Mapped[bool] = mapped_column(Boolean, default=False)
    is_hidden: Mapped[bool] = mapped_column(Boolean, default=False)
    view_count: Mapped[int] = mapped_column(Integer, default=0)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    board = relationship("Board")
    author = relationship("User")

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, DateTime, Text
from datetime import datetime
import secrets


class Base(DeclarativeBase):
    pass


class FeedbackItem(Base):
    __tablename__ = "feedback_items"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    internal_token: Mapped[str] = mapped_column(String(255), unique=True)
    original_question: Mapped[str] = mapped_column(Text)
    old_answer: Mapped[str] = mapped_column(Text)
    edited_answer: Mapped[str] = mapped_column(Text)
    note: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="pending")
    suggested_by: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    resolved_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)


class QAQueue(Base):
    __tablename__ = "qa_queue"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    question: Mapped[str] = mapped_column(Text)
    answer: Mapped[str] = mapped_column(Text)
    category: Mapped[str] = mapped_column(String(255))
    subcategory: Mapped[str] = mapped_column(String(255))
    subtopic: Mapped[str] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


engine = create_async_engine("sqlite+aiosqlite:////home/kate/T1-hackathon/backend/data/feedback.db")
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session


def generate_token() -> str:
    return secrets.token_urlsafe(32)

from typing import List, Optional, Any, Type, cast
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeMeta, declarative_base, registry
from sqlalchemy.future import select

PERSIST_DIRECTORY = "./chroma_db"

mapper_registry = registry()
Base = mapper_registry.generate_base()

class Memory(Base):
    __tablename__ = 'memories'
    id = Column(Integer, primary_key=True)
    content = Column(String)
    category = Column(String)
    importance = Column(Float)

# Setup de async SQLite database
engine = create_async_engine('sqlite+aiosqlite:///memories.db')
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_session() -> AsyncSession:
    session = async_session()
    return session

async def add_memory(content: str, category: str, importance: float) -> None:
    async with async_session() as session:
        new_memory = Memory(content=content, category=category, importance=importance)
        session.add(new_memory)
        await session.commit()

async def get_memories_by_category(category: str) -> List[Memory]:
    async with async_session() as session:
        result = await session.execute(
            select(Memory).filter_by(category=category)
        )
        return list(result.scalars().all())

async def update_memory_importance(memory_id: int, importance: float) -> None:
    async with async_session() as session:
        memory = await session.get(Memory, memory_id)
        if memory:
            memory.importance = importance
            await session.commit()

async def delete_memory(memory_id: int) -> None:
    async with async_session() as session:
        memory = await session.get(Memory, memory_id)
        if memory:
            await session.delete(memory)
            await session.commit()

async def create_memory(content: str, category: str, importance: float) -> Memory:
    return Memory(content=content, category=category, importance=importance)

async def get_all_memories() -> List[Memory]:
    async with async_session() as session:
        result = await session.execute(select(Memory))
        return list(result.scalars().all())
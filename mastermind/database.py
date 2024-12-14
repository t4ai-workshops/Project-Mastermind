from typing import List, Optional, Any, Type
from sqlalchemy import create_engine, Column, Integer, String, Float # type: ignore
from sqlalchemy.ext.declarative import declarative_base # type: ignore
from sqlalchemy.orm import sessionmaker, Session, DeclarativeMeta # type: ignore

PERSIST_DIRECTORY = "./chroma_db"

Base: DeclarativeMeta = declarative_base()

class Memory(Base):
    __tablename__ = 'memories'
    id = Column(Integer, primary_key=True)
    content = Column(String)
    category = Column(String)
    importance = Column(Float)

# Setup de SQLite database
engine = create_engine('sqlite:///memories.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def add_memory(content: str, category: str, importance: float) -> None:
    new_memory = Memory(content=content, category=category, importance=importance)
    session.add(new_memory)
    session.commit()

def get_memories_by_category(category: str) -> List[Memory]:
    result = session.query(Memory).filter_by(category=category).all()
    return list(result)

async def update_memory_importance(session: Session, memory_id: int, importance: float) -> None:
    memory = session.query(Memory).filter(Memory.id == memory_id).first()
    if memory:
        memory.importance = importance
        session.commit()

async def delete_memory(session: Session, memory_id: int) -> None:
    memory = session.query(Memory).filter(Memory.id == memory_id).first()
    if memory:
        session.delete(memory)
        session.commit()

def create_memory(content: str, category: str, importance: float) -> Memory:
    return Memory(content=content, category=category, importance=importance)

async def get_all_memories(session: Session) -> List[Memory]:
    result = session.query(Memory).all()
    return list(result)
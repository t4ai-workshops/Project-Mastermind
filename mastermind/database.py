from typing import Optional
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

PERSIST_DIRECTORY = "./chroma_db"

Base = declarative_base()

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

def get_memories_by_category(category: str) -> list:
    return session.query(Memory).filter_by(category=category).all()

def update_memory_importance(memory_id: int, new_importance: float) -> bool:
    memory = session.query(Memory).filter_by(id=memory_id).first()
    if memory:
        memory.importance = new_importance
        session.commit()
        return True
    return False

def delete_memory(memory_id: int) -> bool:
    memory = session.query(Memory).filter_by(id=memory_id).first()
    if memory:
        session.delete(memory)
        session.commit()
        return True
    return False

def create_memory(content: str, category: str, importance: float) -> Memory:
    return Memory(content=content, category=category, importance=importance)

def get_memory_by_id(memory_id: int) -> Optional[Memory]:
    # Implementatie om een geheugen op te halen
    ...

def update_memory_importance(memory_id: int, new_importance: float) -> bool:
    # Implementatie om het belang van een geheugen te updaten
    ...

def delete_memory(memory_id: int) -> bool:
    # Implementatie om een geheugen te verwijderen
    ...
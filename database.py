from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

# Таблица записей дневника
class DiaryEntry(Base):
    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, default=1)
    date = Column(Date, unique=True, nullable=False)
    teacher = Column(String(100))
    content = Column(Text)
    # Связь с тегами и ресурсами
    keywords = relationship("Keyword", back_populates="entry", cascade="all, delete")
    resources = relationship("Resource", back_populates="entry", cascade="all, delete")

class Keyword(Base):
    __tablename__ = 'keywords'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, default=1)
    word = Column(String(50), index=True)
    entry_id = Column(Integer, ForeignKey('entries.id'))
    entry = relationship("DiaryEntry", back_populates="keywords")

class Resource(Base):
    __tablename__ = 'resources'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, default=1)
    url = Column(String(255))
    entry_id = Column(Integer, ForeignKey('entries.id'))
    entry = relationship("DiaryEntry", back_populates="resources")

# Инициализация БД
engine = create_engine('sqlite:///lernradar.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, func
from src.database.base import Base


class Tweet(Base):
    __tablename__ = 'tweet'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(length=255))
    content = Column(String(length=255))
    image_url = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())


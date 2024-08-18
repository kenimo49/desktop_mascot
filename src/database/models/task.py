from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, func
from src.database.base import Base
from sqlalchemy.orm import relationship


class Task(Base):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)  # タスクのタイトル
    description = Column(Text, nullable=True)  # タスクの詳細
    status = Column(String, nullable=False, default="未完了")  # タスクの状態（例: 未完了、完了）
    created_at = Column(TIMESTAMP, server_default=func.now())  # タスク作成日時
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())  # タスク更新日時

    sub_tasks = relationship("SubTask", back_populates="task", cascade="all, delete-orphan")  # サブタスクとのリレーションシップ
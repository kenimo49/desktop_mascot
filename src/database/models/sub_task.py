from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey, func
from sqlalchemy.orm import relationship
from src.database.base import Base

class SubTask(Base):
    __tablename__ = 'sub_task'

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(Integer, ForeignKey('task.id'), nullable=False)  # タスクIDへの外部キー
    title = Column(String, nullable=False)  # サブタスクのタイトル
    description = Column(Text, nullable=True)  # サブタスクの詳細
    status = Column(String, nullable=False, default="未完了")  # サブタスクの状態（例: 未完了、完了）
    created_at = Column(TIMESTAMP, server_default=func.now())  # 作成日時
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())  # 更新日時

    task = relationship("Task", back_populates="sub_tasks")  # タスクとのリレーションシップ

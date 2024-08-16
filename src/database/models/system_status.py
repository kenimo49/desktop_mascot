from sqlalchemy import Column, Integer, String, Boolean
from src.database import Base


class SystemStatus(Base):
    # 初期化状態等のシステムステータスを管理するテーブル
    __tablename__ = 'system_status'

    id = Column(Integer, primary_key=True, autoincrement=True)
    status_key = Column(String(50), unique=True, nullable=False)
    status_value = Column(Boolean, nullable=False, default=False)
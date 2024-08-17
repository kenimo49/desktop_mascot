from sqlalchemy import Column, Integer, Boolean
from src.database.base import Base


class KeyloggerSetting(Base):
    __tablename__ = 'keylogger_setting'

    id = Column(Integer, primary_key=True, autoincrement=True)
    is_enabled = Column(Boolean, nullable=False, default=False)  # ON/OFFの状態を保存
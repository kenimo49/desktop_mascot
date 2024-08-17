from sqlalchemy import Column, Integer, String, Enum, Integer
from src.database.base import Base
from src.database.enums.timer_name import TimerName  # enumを定義したファイルをインポート


class TimerSettings(Base):
    __tablename__ = 'timer_settings'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Enum(TimerName), nullable=False)  # Enumを使用
    interval = Column(Integer, nullable=False)  # ミリ秒単位で保存


from sqlalchemy import Column, Integer, String, TypeDecorator, Enum as SQLAEnum
from src.database.base import Base
from src.database.enums.timer_name import TimerName

# TimerName Enum のカスタムタイプデコレータ
class TimerNameType(TypeDecorator):
    impl = String

    def process_bind_param(self, value, dialect):
        if isinstance(value, TimerName):
            return value.internal_name
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            return TimerName.get_by_internal_name(value)
        return value


class TimerSettings(Base):
    __tablename__ = 'timer_settings'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(TimerNameType(), nullable=False, unique=True)  # Enumを使用
    interval = Column(Integer, nullable=False)  # ミリ秒単位で保存


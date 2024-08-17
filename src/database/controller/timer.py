from src.database.models.timer_setting import TimerSettings
from src.database import session
from src.database.enums.timer_name import TimerName


def get_timer_interval(timer_name: TimerName) -> int:
    timer_setting = session.query(TimerSettings).filter_by(name=timer_name).first()
    if timer_setting:
        return timer_setting.interval
    else:
        # デフォルトの値を返す（設定が存在しない場合）
        return 30000  # 30秒

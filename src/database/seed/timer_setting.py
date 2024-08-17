from src.database.models.timer_setting import TimerSettings
from src.database import session
from src.database.enums.timer_name import TimerName


def seed_timer_setting():
    one_second = 1000
    initial_settings = [
        TimerSettings(name=TimerName.UPDATE_TIMER, interval=50),
        TimerSettings(name=TimerName.AUTO_TALK_TIMER, interval=30 * one_second),
        TimerSettings(name=TimerName.MOVE_TIMER, interval=5 * 60 * one_second)
    ]

    session.bulk_save_objects(initial_settings)
    session.commit()

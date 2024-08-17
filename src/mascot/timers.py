from PyQt6.QtCore import QTimer
from src.mascot.talk import auto_talk
from src.mascot.animation.moving_around import start_moving_around
from src.mascot.animation.base import init_animation, update_position
from src.database.enums.timer_name import TimerName
from src.database.controller.timer import get_timer_interval
from src.database.models.timer_setting import TimerSettings
from src.database import session


def setup_timers(mascot):
    # タイマー設定を取得
    auto_talk_timer_setting = session.query(TimerSettings).filter_by(name=TimerName.AUTO_TALK_TIMER).first()
    move_timer_setting = session.query(TimerSettings).filter_by(name=TimerName.MOVE_TIMER).first()

    # アニメーションを更新するタイマー
    init_animation(mascot)
    update_timer = QTimer(mascot)
    update_timer_interval = get_timer_interval(TimerName.UPDATE_TIMER)
    if update_timer_interval > 0:
        update_timer.timeout.connect(lambda: update_position(mascot))
        update_timer.start(update_timer_interval)  # データベースから取得した間隔で更新

    # 自動で吹き出しを表示するタイマー
    auto_talk_timer = QTimer(mascot)
    if auto_talk_timer_setting and auto_talk_timer_setting.interval > 0:
        auto_talk_timer.timeout.connect(lambda: auto_talk(mascot))
        auto_talk_timer.start(auto_talk_timer_setting.interval)

    # 動き回るタイマー
    move_timer = QTimer(mascot)
    if move_timer_setting and move_timer_setting.interval > 0:
        move_timer.timeout.connect(lambda: start_moving_around(mascot))
        move_timer.start(move_timer_setting.interval)

    return update_timer, auto_talk_timer, move_timer

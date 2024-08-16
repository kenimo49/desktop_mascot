from PyQt6.QtCore import QTimer
from src.mascot.talk import auto_talk
from src.mascot.animation.moving_around import start_moving_around, init_moving_around
from src.mascot.animation.base import init_animation
from src.mascot.animation.base import update_position


def setup_timers(mascot):
    # アニメーションを更新するタイマー
    init_animation(mascot)
    update_timer = QTimer(mascot)
    update_timer.timeout.connect(lambda: update_position(mascot))
    update_timer.start(50)  # 50ミリ秒ごとに更新

    # 30秒ごとに自動で吹き出しを表示するタイマー
    auto_talk_timer = QTimer(mascot)
    auto_talk_timer.timeout.connect(lambda: auto_talk(mascot))
    auto_talk_timer.start(30000)  # 30秒ごとに発動

    # 5分ごとに10秒間動き回るタイマー
    init_moving_around(mascot)
    move_timer = QTimer(mascot)
    move_timer.timeout.connect(lambda: start_moving_around(mascot))
    move_timer.start(300000)  # 5分ごとに発動

    return update_timer, auto_talk_timer, move_timer
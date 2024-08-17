from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QPoint
from PyQt6.QtGui import QPixmap
import random


def init_moving_around(mascot):
    print("init_moving_around")
    # 右回りに動くためのアニメーション
    mascot.is_moving = False  # 動作中かどうかを示すフラグを追加
    mascot.movement_animation = QPropertyAnimation(mascot, b"pos")


def start_moving_around(mascot):
    print("start_moving_around")
    if not mascot.is_moving:  # すでに動作中でない場合のみ開始
        mascot.is_moving = True
        random.choice([move_left, move_right, move_down])(mascot)  # ランダムに一つの動作を選択して実行


def animate_move(mascot, target_x, target_y, next_move_callback):
    print("animate_move")
    mascot.label.setPixmap(QPixmap("image/shiro/running_shiro.png"))
    # 以前の接続を解除
    try:
        mascot.movement_animation.finished.disconnect()
    except TypeError:
        pass  # まだ接続されていない場合は何もしない

    # アニメーションの設定
    mascot.movement_animation.setDuration(2000)  # 2秒間の移動
    mascot.movement_animation.setStartValue(mascot.pos())
    mascot.movement_animation.setEndValue(QPoint(target_x, target_y))
    mascot.movement_animation.setEasingCurve(QEasingCurve.Type.Linear)
    mascot.movement_animation.finished.connect(next_move_callback)
    mascot.movement_animation.start()


def move_right(mascot):
    target_x = mascot.screen_width - mascot.width()
    target_y = mascot.y()
    animate_move(mascot, target_x, target_y, lambda: stop_moving_around(mascot))


def move_down(mascot):
    target_x = mascot.x()
    target_y = mascot.screen_height - mascot.height()
    animate_move(mascot, target_x, target_y, lambda: stop_moving_around(mascot))


def move_left(mascot):
    target_x = 0
    target_y = mascot.y()
    animate_move(mascot, target_x, target_y, lambda: stop_moving_around(mascot))


def move_up(mascot):
    target_x = mascot.x()
    target_y = 0
    animate_move(mascot, target_x, target_y, lambda: stop_moving_around(mascot))


def stop_moving_around(mascot):
    print("stop_moving_around")
    mascot.is_moving = False  # 動作を停止
    mascot.label.setPixmap(QPixmap("image/shiro/default_shiro.png"))


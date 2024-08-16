from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QPoint

def start_moving_around(mascot):
    print("start_moving_around")
    if not mascot.is_moving:  # すでに動作中でない場合のみ開始
        mascot.is_moving = True
        move_left(mascot)

def animate_move(mascot, target_x, target_y, next_move_callback):
    print("animate_move")
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
    print("move_right")
    target_x = mascot.screen_width - mascot.width()
    target_y = mascot.y()
    animate_move(mascot, target_x, target_y, lambda: move_down(mascot))

def move_down(mascot):
    target_x = mascot.x()
    target_y = mascot.screen_height - mascot.height()
    animate_move(mascot, target_x, target_y, lambda: move_left(mascot))

def move_left(mascot):
    target_x = 0
    target_y = mascot.y()
    animate_move(mascot, target_x, target_y, lambda: move_up(mascot))

def move_up(mascot):
    target_x = mascot.x()
    target_y = 0
    animate_move(mascot, target_x, target_y, lambda: stop_moving_around(mascot))

def stop_moving_around(mascot):
    print("stop_moving_around")
    mascot.is_moving = False  # 動作を停止


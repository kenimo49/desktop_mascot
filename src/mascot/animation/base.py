def init_animation(mascot):
    # アニメーション用の変数を初期化
    mascot.offset = 0
    mascot.direction = 1


def update_position(mascot):
    # 左右に揺れるアニメーションの更新
    mascot.offset += mascot.direction * 2
    if abs(mascot.offset) > 10:
        mascot.direction *= -1
    mascot.move(mascot.x() + mascot.direction * 2, mascot.y())



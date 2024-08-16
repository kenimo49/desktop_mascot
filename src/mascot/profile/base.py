from PyQt6.QtCore import QTimer
from src.dialog.speech_bubble import SpeechBubble


def init_profile(mascot):
    # キャラクターのレベルを保持する変数を追加
    mascot.level = 1


def show_level(mascot):
    # レベルを表示する吹き出しを作成
    if mascot.speech_bubble:
        mascot.speech_bubble.close()

    mascot.speech_bubble = SpeechBubble(f"Lv.{mascot.level}", None, mascot)
    mascot.speech_bubble.adjustSize()

    # 吹き出しの位置をウィンドウの中央上部に設定（さらに上に移動）
    bubble_x = mascot.x() + mascot.width() // 2 - mascot.speech_bubble.width() // 2
    bubble_y = mascot.y() - mascot.speech_bubble.height() - 10  # 10ピクセル上に調整
    mascot.speech_bubble.move(bubble_x, bubble_y)
    mascot.speech_bubble.show()

    # 5秒後に吹き出しを閉じるタイマーを設定
    QTimer.singleShot(5000, mascot.speech_bubble.close)
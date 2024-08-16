import random
from PyQt6.QtCore import QTimer
from src.dialog.speech_bubble import SpeechBubble
from src.database import session
from src.database.models.tweet_model import Tweet


def talk(mascot, message, image_paths=None, close_timeout: int = 0):
    # 既存の吹き出しがあれば削除
    if mascot.speech_bubble:
        mascot.speech_bubble.close()

    # カスタム吹き出しの作成
    mascot.speech_bubble = SpeechBubble(message, image_paths)

    # 吹き出しの位置を調整
    bubble_x = mascot.x() + mascot.width() // 2 - mascot.speech_bubble.width() // 2
    bubble_y = mascot.y() - mascot.speech_bubble.height()
    mascot.speech_bubble.move(bubble_x, bubble_y)
    mascot.speech_bubble.show()

    # close_timeout秒後に吹き出しを閉じるタイマーを設定
    if close_timeout > 0:
        QTimer.singleShot(close_timeout, mascot.speech_bubble.close)


def auto_talk(mascot):
    # dbからメッセージを取得
    query_result = session.query(Tweet).all()
    # ランダムにメッセージを選択して吹き出しに表示
    message = random.choice(query_result)
    image_paths = message.get_images()
    talk(mascot, message.content, image_paths, close_timeout=5000)
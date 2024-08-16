import random
from PyQt6.QtCore import QTimer
from src.speech_bubble import SpeechBubble
from src.database import session
from src.database.models.tweet_model import Tweet


def talk(mascot, message, image_path, close_timeout: int = 0):
    # 既存の吹き出しがあれば削除
    if mascot.speech_bubble:
        mascot.speech_bubble.close()

    mascot.speech_bubble = SpeechBubble(message, image_path)
    mascot.speech_bubble.adjustSize()  # サイズを自動調整
    mascot.speech_bubble.move(mascot.x() + mascot.width() // 2 - mascot.speech_bubble.width() // 2,
                              mascot.y() - mascot.speech_bubble.height())
    mascot.speech_bubble.show()

    # {close_timeout}秒後に吹き出しを閉じるタイマーを設定
    if close_timeout > 0:
        QTimer.singleShot(close_timeout, mascot.speech_bubble.close)


def auto_talk(mascot):
    # dbからメッセージを取得
    query_result = session.query(Tweet).all()
    # ランダムにメッセージを選択して吹き出しに表示
    message = random.choice(query_result)
    image_path = "image/character1.jpg"
    talk(mascot, message.content, image_path, close_timeout=5000)
from src.database import session
from src.database.models.tweet_model import Tweet


def seed_tweets():
    # 初期データの定義
    initial_tweets = [
        Tweet(title="初めてのツイート", content="これは最初のツイートです"),
        Tweet(title="Python学習", content="Pythonは楽しいですね！"),
        Tweet(title="ランチタイム", content="今日はカレーを食べました。"),
        Tweet(title="仕事終了", content="今日は疲れた..."),
        Tweet(title="映画鑑賞", content="最近のおすすめ映画は何ですか？")
    ]

    # データベースに初期データを挿入
    session.bulk_save_objects(initial_tweets)
    session.commit()


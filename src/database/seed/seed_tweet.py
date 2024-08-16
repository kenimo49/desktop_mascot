from src.database import session
from src.database.models.tweet_model import Tweet


def seed_tweets():
    # 初期データの定義
    initial_tweets = [
        Tweet(title="文章力アップ", content="文章力を30点から70点に引き上げてくれる本", image_url="image/tweet/文章力UP.jfif"),
    ]

    # データベースに初期データを挿入
    session.bulk_save_objects(initial_tweets)
    session.commit()


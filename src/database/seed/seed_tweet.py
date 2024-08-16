from src.database import session
from src.database.models.tweet_model import Tweet


def seed_tweets():
    # 初期データの定義
    tweet = Tweet(title="文章力アップ", content="文章力を30点から70点に引き上げてくれる本")
    tweet.set_images(["image/tweet/文章力UP.jfif"])

    tweet2 = Tweet(title="「失敗」の掘り下げ方", content="成果を出す人は「失敗」の掘り下げ方が上手い")
    tweet2.set_images(["image/tweet/失敗の10大原因.jfif"])

    tweet3 = Tweet(title="chatGPT改善", content="AIの頭を良くする天才プロンプト6選")
    tweet3.set_images(["image/tweet/chatGPT改善1.jfif", "image/tweet/chatGPT改善2.jfif", "image/tweet/chatGPT改善3.jfif"])

    tweet4 = Tweet(title="AIマンガ", content="Anifusionを使ってみてください")

    tweet5 = Tweet(title="集中力", content="集中力を30秒で取り戻す脳ハック")
    tweet5.set_images(["image/tweet/集中力回復.jfif"])

    # データベースに初期データを挿入
    session.bulk_save_objects([tweet, tweet2, tweet3, tweet4, tweet5])
    session.commit()


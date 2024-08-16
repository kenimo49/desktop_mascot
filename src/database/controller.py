from src.database.init import session
from src.database.models import Tweet


# データベースに新しいTweetを作成する関数
def create_tweet(title, content, image_url=None):
    new_tweet = Tweet(
        title=title,
        content=content,
        image_url=image_url
    )
    session.add(new_tweet)
    session.commit()
    return new_tweet


# データベースからすべてのTweetを取得する関数
def get_all_tweets():
    return session.query(Tweet).all()


# IDを指定してTweetを取得する関数
def get_tweet_by_id(tweet_id):
    return session.query(Tweet).filter(Tweet.id == tweet_id).first()


# IDを指定してTweetを更新する関数
def update_tweet(tweet_id, title=None, content=None, image_url=None):
    tweet = session.query(Tweet).filter(Tweet.id == tweet_id).first()
    if tweet:
        if title:
            tweet.title = title
        if content:
            tweet.content = content
        if image_url:
            tweet.image_url = image_url
        session.commit()
        return tweet
    return None


# IDを指定してTweetを削除する関数
def delete_tweet(tweet_id):
    tweet = session.query(Tweet).filter(Tweet.id == tweet_id).first()
    if tweet:
        session.delete(tweet)
        session.commit()
        return True
    return False

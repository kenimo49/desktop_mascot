from sqlalchemy.orm import sessionmaker
from src.database.base import Base, engine
from src.database.models.tweet_model import Tweet  # ここでモデルをインポート

# セッションの作成
Session = sessionmaker(bind=engine)
session = Session()


def initialize_database():
    # テーブルが存在しない場合にのみテーブルを作成
    Base.metadata.create_all(bind=engine)
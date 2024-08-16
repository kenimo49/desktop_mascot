import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

# SQLiteエンジンの作成
engine = sqlalchemy.create_engine('sqlite:///database.sqlite3', echo=True)

# ベースクラスの作成
Base = declarative_base()
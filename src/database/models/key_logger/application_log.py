from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, func
from src.database.base import Base


class ApplicationLog(Base):
    __tablename__ = 'application_log'

    id = Column(Integer, primary_key=True, autoincrement=True)
    application_name = Column(String, nullable=False)  # アプリケーション名
    window_title = Column(String, nullable=False)  # ウィンドウタイトル
    url = Column(String, nullable=True)  # ブラウザの場合、URLを保存
    input_text = Column(Text, nullable=False)  # 入力されたテキスト
    timestamp = Column(TIMESTAMP, server_default=func.now())  # 入力時のタイムスタンプ
    context = Column(String, nullable=True)  # 入力のコンテキスト（フォーム、検索ボックスなど）

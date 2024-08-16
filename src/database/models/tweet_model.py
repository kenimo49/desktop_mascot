import json
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, func
from src.database.base import Base


class Tweet(Base):
    # つぶやきの情報を管理するテーブル
    __tablename__ = 'tweet'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(length=255))
    content = Column(String(length=255))
    images = Column(Text, nullable=True)  # JSON形式の画像URLリストをテキストとして保存
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    def set_images(self, image_list):
        """画像のリストをJSON形式の文字列として保存"""
        self.images = json.dumps(image_list)

    def get_images(self):
        """JSON形式の文字列を画像のリストに変換して返す"""
        if self.images:
            return json.loads(self.images)
        return []


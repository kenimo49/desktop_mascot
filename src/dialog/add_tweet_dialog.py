from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QFileDialog
from src.database import session
from src.database.models.tweet_model import Tweet

class AddTweetDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("つぶやきの追加")
        self.setFixedSize(300, 400)

        layout = QVBoxLayout(self)

        self.title_edit = QLineEdit(self)
        self.title_edit.setPlaceholderText("タイトルを入力してください")
        layout.addWidget(QLabel("タイトル:", self))
        layout.addWidget(self.title_edit)

        self.content_edit = QTextEdit(self)
        self.content_edit.setPlaceholderText("内容を入力してください")
        layout.addWidget(QLabel("内容:", self))
        layout.addWidget(self.content_edit)

        self.image_path_edit = QLineEdit(self)
        layout.addWidget(QLabel("画像:", self))
        layout.addWidget(self.image_path_edit)

        browse_button = QPushButton("画像を選択", self)
        browse_button.clicked.connect(self.browse_image)
        layout.addWidget(browse_button)

        self.add_button = QPushButton("追加", self)
        self.add_button.clicked.connect(self.add_tweet)
        layout.addWidget(self.add_button)

    def browse_image(self):
        image_path, _ = QFileDialog.getOpenFileName(self, "画像を選択", "", "Image Files (*.png *.jpg *.bmp *.jfif *.jpeg *.gif *.webp)")
        if image_path:
            self.image_path_edit.setText(image_path)

    def add_tweet(self):
        title = self.title_edit.text().strip()
        content = self.content_edit.toPlainText().strip()
        image_path = self.image_path_edit.text().strip()

        if title and content:
            new_tweet = Tweet(title=title, content=content)
            if image_path:
                new_tweet.set_images([image_path])
            session.add(new_tweet)
            session.commit()
            self.accept()

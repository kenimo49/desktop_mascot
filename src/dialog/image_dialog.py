from PyQt6.QtWidgets import QLabel, QVBoxLayout, QDialog
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt, QSize


class ImageDialog(QDialog):
    def __init__(self, image_path, text=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("拡大表示")
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        # レイアウトを作成
        layout = QVBoxLayout(self)

        # テキストが指定されている場合、テキストラベルを追加
        if text:
            self.text_label = QLabel(text, self)
            font = QFont("Arial", 12)
            self.text_label.setFont(font)
            layout.addWidget(self.text_label)

        # 画像を表示するラベルを作成
        self.image_label = QLabel(self)
        pixmap = QPixmap(image_path)

        # 画面のサイズに合わせて画像を縮小（必要ならば）
        screen = self.screen().availableGeometry()
        max_size = QSize(screen.width() * 0.8, screen.height() * 0.8)  # 画面サイズの80%を最大サイズとする
        pixmap = pixmap.scaled(max_size, Qt.AspectRatioMode.KeepAspectRatio)
        self.image_label.setPixmap(pixmap)

        # レイアウトに追加
        layout.addWidget(self.image_label)
        self.setLayout(layout)

        # ウィンドウサイズを画像に合わせる
        self.adjustSize()
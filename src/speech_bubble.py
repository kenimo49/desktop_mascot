from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget, QLineEdit
from PyQt6.QtGui import QPixmap, QPainter, QColor, QPolygon, QFont
from PyQt6.QtCore import Qt, QPoint, QSize

class SpeechBubble(QWidget):
    def __init__(self, text, image_path=None, parent=None):
        super().__init__(parent)
        self.text = text
        self.image_path = image_path
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # レイアウトと入力ボックスを設定
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        # テキストの表示
        self.text_label = QLabel(self.text, self)
        font = QFont("Arial", 10)
        self.text_label.setFont(font)
        self.layout.addWidget(self.text_label)

        # 画像が指定されている場合、QLabelで表示
        if self.image_path:
            self.image_label = QLabel(self)
            pixmap = QPixmap(self.image_path)
            # 画像サイズを調整（必要に応じて調整）
            max_image_size = (300, 300)  # 最大サイズを指定
            pixmap = pixmap.scaled(max_image_size[0], max_image_size[1], aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)
            self.image_label.setPixmap(pixmap)
            self.layout.addWidget(self.image_label)

        # 入力ボックスを追加
        self.input_box = QLineEdit(self)
        self.input_box.setPlaceholderText("メッセージを入力してください...")
        self.input_box.returnPressed.connect(self.handle_input)
        self.layout.addWidget(self.input_box)

        # サイズ調整
        self.adjustSize()

    def handle_input(self):
        # 入力されたテキストを取得
        input_text = self.input_box.text()
        self.input_box.clear()
        # 入力内容に応じて応答を設定
        if input_text == "おはよう":
            self.text_label.setText("おはようございます")
        else:
            self.text_label.setText(f"あなたは「{input_text}」と入力しました。")

        # 吹き出しを再描画して応答を表示
        self.update()

    def sizeHint(self):
        # 吹き出しのサイズをテキストと画像、入力ボックスに基づいて設定
        return QSize(300, 300)  # ウィジェットのサイズを設定

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = self.rect()

        # 吹き出しの描画
        bubble_color = QColor(255, 255, 255)
        painter.setBrush(bubble_color)
        painter.setPen(Qt.PenStyle.NoPen)

        # 吹き出しの形状をさらにコンパクトに調整
        painter.drawRoundedRect(rect.adjusted(5, 5, -5, -15), 10, 10)

        # 吹き出しの三角形部分もコンパクトに
        triangle = QPolygon([QPoint(rect.width() // 2 - 5, rect.height() - 15),
                             QPoint(rect.width() // 2 + 5, rect.height() - 15),
                             QPoint(rect.width() // 2, rect.height())])
        painter.drawPolygon(triangle)


from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget, QLineEdit, QHBoxLayout
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

        # テキストと画像のコンテナ
        text_image_layout = QHBoxLayout()
        self.layout.addLayout(text_image_layout)

        # 画像が指定されている場合、QLabelで表示
        if self.image_path:
            self.image_label = QLabel(self)
            pixmap = QPixmap(self.image_path)
            self.image_label.setPixmap(pixmap)
            text_image_layout.addWidget(self.image_label)

        # テキストの表示
        self.text_label = QLabel(self.text, self)
        font = QFont("Arial", 10)
        self.text_label.setFont(font)
        text_image_layout.addWidget(self.text_label)

        # 入力ボックスを追加
        self.input_box = QLineEdit(self)
        self.input_box.setPlaceholderText("メッセージを入力してください...")
        self.input_box.returnPressed.connect(self.handle_input)
        self.layout.addWidget(self.input_box)
        self.adjustSize()

    def handle_input(self):
        # 入力されたテキストを取得
        input_text = self.input_box.text()
        self.input_box.clear()
        # 入力内容に応じて応答を設定
        if input_text == "おはよう":
            self.text = "おはようございます"
        else:
            self.text = f"あなたは「{input_text}」と入力しました。"

        # 吹き出しを再描画して応答を表示
        self.update()

    def sizeHint(self):
        padding = 10
        triangle_height = 10
        # return QSize(self.text_width + padding * 2, self.text_height + padding * 2 + triangle_height)
        return QSize(300, 150)  # ウィジェットのサイズを設定

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

        # テキストの描画
        painter.setPen(Qt.GlobalColor.black)
        font = QFont("Arial", 10)
        painter.setFont(font)
        # painter.drawText(rect.adjusted(5, 5, -5, -20), Qt.AlignmentFlag.AlignCenter, self.text)
        painter.drawText(rect.adjusted(10, 10, -10, -(rect.height() - self.input_box.height() - 20)),
                         Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop, self.text)
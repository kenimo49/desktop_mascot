from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QMenu, QVBoxLayout, QWidget, QLineEdit, QHBoxLayout
from PyQt6.QtGui import QPixmap, QPainter, QColor, QPolygon, QFont
from PyQt6.QtCore import Qt, QTimer, QPoint, QSize
from PyQt6.QtGui import QAction, QFontMetrics
import random
import sys

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


class AnimatedMascot(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Animated  Mascot")
        self.setGeometry(100, 100, 340, 370)  # ウィンドウサイズを画像サイズに合わせる
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)

        # マスコットの画像を読み込む
        self.label = QLabel(self)
        pixmap = QPixmap("image/character02.png")
        self.label.setPixmap(pixmap)
        self.label.setGeometry(0, 0, pixmap.width(), pixmap.height())
        self.setFixedSize(pixmap.width(), pixmap.height())

        # 画面サイズを取得し、ウィンドウを右下に配置
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()
        self.move(screen_width - self.width(), screen_height - self.height())

        # アニメーション用変数
        self.offset = 0
        self.direction = 1

        # タイマーを設定してアニメーションを更新
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_position)
        self.timer.start(50)  # 50ミリ秒ごとに更新

        # 30秒ごとに自動で吹き出しを表示するタイマーを設定
        self.auto_talk_timer = QTimer(self)
        self.auto_talk_timer.timeout.connect(self.auto_talk)
        self.auto_talk_timer.start(30000)  # 30秒ごとに発動

        # ドラッグ機能を追加
        self.label.mousePressEvent = self.start_drag
        self.label.mouseMoveEvent = self.do_drag

        # 右クリックメニュー設定
        self.label.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.label.customContextMenuRequested.connect(self.show_context_menu)

        # 吹き出しウィジェットを初期化（非表示）
        self.speech_bubble = None

        # 疑似会話用メッセージのリスト
        self.messages = [
            "こんにちは！今日はどう？",
            "何か面白い話がある？",
            "次のプロジェクトは順調？",
            "ちょっと休憩しようか？",
            "コーヒー飲みたいなぁ"
        ]

    def update_position(self):
        # 左右に揺れるアニメーションの更新
        self.offset += self.direction * 2
        if abs(self.offset) > 10:
            self.direction *= -1
        self.move(self.x() + self.direction * 2, self.y())

    def start_drag(self, event):
        self.drag_start_x = event.position().x()
        self.drag_start_y = event.position().y()

    def do_drag(self, event):
        x = self.x() + (event.position().x() - self.drag_start_x)
        y = self.y() + (event.position().y() - self.drag_start_y)
        self.move(x, y)

    def show_context_menu(self, position):
        menu = QMenu(self)

        # 「話す」アクションを作成
        talk_action = QAction("話す", self)
        talk_action.triggered.connect(self.talk)

        # 「終了」アクションを作成
        quit_action = QAction("終了", self)
        quit_action.triggered.connect(self.close)

        # メニューにアクションを追加
        menu.addAction(talk_action)
        menu.addAction(quit_action)

        # メニューを表示
        menu.exec(self.mapToGlobal(position))

    def talk(self):
        # 既存の吹き出しがあれば削除
        if self.speech_bubble:
            self.speech_bubble.close()

        # ランダムにメッセージを選択して吹き出しに表示
        message = random.choice(self.messages)
        # 画像のパスを指定して吹き出しを作成
        image_path = "image/character1.jpg"
        self.speech_bubble = SpeechBubble(message, image_path)
        self.speech_bubble.adjustSize()  # サイズを自動調整
        self.speech_bubble.move(self.x() + self.width() // 2 - self.speech_bubble.width() // 2,
                                self.y() - self.speech_bubble.height())
        self.speech_bubble.show()

        # 5秒後に吹き出しを閉じるタイマーを設定
        QTimer.singleShot(5000, self.speech_bubble.close)

    def auto_talk(self):
        # 自動で表示される吹き出しの内容を設定
        self.talk()
        # 例: 自動メッセージを設定する場合
        # if self.speech_bubble:
        #     self.speech_bubble.text = "自動メッセージ"
        #     self.speech_bubble.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AnimatedMascot()
    window.show()
    sys.exit(app.exec())
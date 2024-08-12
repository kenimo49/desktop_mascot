from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QMenu, QMessageBox, QWidget
from PyQt6.QtGui import QPixmap, QPainter, QColor, QPolygon, QFont
from PyQt6.QtCore import Qt, QTimer, QPoint
from PyQt6.QtGui import QAction, QFontMetrics
import random
import sys

class SpeechBubble(QWidget):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.text = text
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # テキストのサイズを計算してウィジェットのサイズを調整
        font = QFont("Arial", 10)
        font_metrics = QFontMetrics(font)
        text_width = font_metrics.horizontalAdvance(text)
        text_height = font_metrics.height()

        # 吹き出しの余白を追加
        padding = 20
        self.setMinimumSize(text_width + padding * 2, text_height + padding * 2 + 20)  # +20は吹き出しの三角部分の高さ

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = self.rect()

        # 吹き出しの描画
        bubble_color = QColor(255, 255, 255)
        painter.setBrush(bubble_color)
        painter.setPen(Qt.PenStyle.NoPen)

        # 吹き出しの形状
        painter.drawRoundedRect(rect.adjusted(10, 10, -10, -20), 15, 15)

        # 吹き出しの三角形部分
        triangle = QPolygon([QPoint(rect.width() // 2 - 10, rect.height() - 20),
                             QPoint(rect.width() // 2 + 10, rect.height() - 20),
                             QPoint(rect.width() // 2, rect.height())])
        painter.drawPolygon(triangle)

        # テキストの描画
        painter.setPen(Qt.GlobalColor.black)
        font = QFont("Arial", 10)
        painter.setFont(font)
        painter.drawText(rect.adjusted(20, 20, -20, -40), Qt.AlignmentFlag.AlignCenter, self.text)

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
        self.speech_bubble = SpeechBubble(message)
        # サイズを自動調整
        self.speech_bubble.adjustSize()
        self.speech_bubble.move(self.x() + self.width() // 2 - self.speech_bubble.width() // 2,
                                self.y() - self.speech_bubble.height())
        self.speech_bubble.show()
        self.speech_bubble.update()  # 再描画を強制

        # 5秒後に吹き出しを閉じるタイマーを設定
        QTimer.singleShot(5000, self.speech_bubble.close)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AnimatedMascot()
    window.show()
    sys.exit(app.exec())
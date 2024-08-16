from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QMenu
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation
from PyQt6.QtGui import QAction
from src.speech_bubble import SpeechBubble
from src.mascot.talk import talk, auto_talk
from src.mascot.movement import start_moving_around


class AnimatedMascot(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Animated  Mascot")
        self.setGeometry(100, 100, 340, 370)  # ウィンドウサイズを画像サイズに合わせる
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)

        # キャラクターのレベルを保持する変数を追加
        self.level = 1

        # マスコットの画像を読み込む
        self.label = QLabel(self)
        pixmap = QPixmap("image/character02.png")
        self.label.setPixmap(pixmap)
        self.label.setGeometry(0, 0, pixmap.width(), pixmap.height())
        self.setFixedSize(pixmap.width(), pixmap.height())

        # 画面サイズを取得し、ウィンドウを右下に配置
        self.screen_geometry = QApplication.primaryScreen().availableGeometry()
        self.screen_width = self.screen_geometry.width()
        self.screen_height = self.screen_geometry.height()
        self.move(self.screen_width - self.width(), self.screen_height - self.height())

        # アニメーション用変数
        self.offset = 0
        self.direction = 1
        self.is_moving = False  # 動作中かどうかを示すフラグを追加

        # タイマー
        # タイマーを設定してアニメーションを更新
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_position)
        self.timer.start(50)  # 50ミリ秒ごとに更新

        # 30秒ごとに自動で吹き出しを表示するタイマーを設定
        self.auto_talk_timer = QTimer(self)
        self.auto_talk_timer.timeout.connect(lambda: auto_talk(self))
        self.auto_talk_timer.start(30000)  # 30秒ごとに発動

        # 5分ごとに10秒間動き回るタイマーを設定
        self.move_timer = QTimer(self)
        self.move_timer.timeout.connect(lambda: start_moving_around(self))
        self.move_timer.start(300000)  # 5分ごとに発動

        # 右回りに動くためのアニメーション
        self.movement_animation = QPropertyAnimation(self, b"pos")

        # ドラッグ機能を追加
        self.label.mousePressEvent = self.start_drag
        self.label.mouseMoveEvent = self.do_drag

        # 右クリックメニュー設定
        self.label.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.label.customContextMenuRequested.connect(self.show_context_menu)

        # 吹き出しウィジェットを初期化（非表示）
        self.speech_bubble = None

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

        # レベル表示用のアクションを作成
        level_action = QAction(f"レベル: {self.level}", self)
        level_action.triggered.connect(self.show_level)

        # 「話す」アクションを作成
        talk_action = QAction("話す", self)
        talk_action.triggered.connect(lambda: talk(self))

        # 「終了」アクションを作成
        quit_action = QAction("終了", self)
        quit_action.triggered.connect(self.close)

        # メニューにアクションを追加
        menu.addAction(level_action)
        menu.addAction(talk_action)
        menu.addAction(quit_action)

        # メニューを表示
        menu.exec(self.mapToGlobal(position))

    def show_level(self):
        # レベルを表示する吹き出しを作成
        if self.speech_bubble:
            self.speech_bubble.close()

        self.speech_bubble = SpeechBubble(f"Lv.{self.level}", None, self)
        self.speech_bubble.adjustSize()

        # 吹き出しの位置をウィンドウの中央上部に設定（さらに上に移動）
        bubble_x = self.x() + self.width() // 2 - self.speech_bubble.width() // 2
        bubble_y = self.y() - self.speech_bubble.height() - 10  # 10ピクセル上に調整
        self.speech_bubble.move(bubble_x, bubble_y)
        self.speech_bubble.show()

        # 5秒後に吹き出しを閉じるタイマーを設定
        QTimer.singleShot(5000, self.speech_bubble.close)

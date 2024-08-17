from PyQt6.QtWidgets import QMainWindow, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt


def setup_display(mascot, window_title="Animated Mascot", window_size=(340, 370), image_path="image/shiro/default_shiro.png"):
    # ディスプレイの基本設定
    mascot.setWindowTitle(window_title)
    mascot.setGeometry(100, 100, *window_size)  # ウィンドウサイズを画像サイズに合わせる
    mascot.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
    mascot.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)

    # マスコットの画像を読み込む
    mascot.label = QLabel(mascot)
    pixmap = QPixmap(image_path)
    mascot.label.setPixmap(pixmap)
    mascot.label.setGeometry(0, 0, pixmap.width(), pixmap.height())
    mascot.setFixedSize(pixmap.width(), pixmap.height())

    # 画面サイズを取得し、ウィンドウを右下に配置
    screen_geometry = mascot.screen().availableGeometry()
    mascot.screen_width = screen_geometry.width()
    mascot.screen_height = screen_geometry.height()
    mascot.move(mascot.screen_width - mascot.width(), mascot.screen_height - mascot.height())
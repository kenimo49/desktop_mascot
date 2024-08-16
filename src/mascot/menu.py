from PyQt6.QtWidgets import QMenu
from src.mascot.talk import auto_talk
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt
from src.mascot.profile.base import show_level


def init_menu(mascot):
    # 右クリックメニュー設定
    mascot.label.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
    mascot.label.customContextMenuRequested.connect(lambda position: show_context_menu(mascot, position))


def show_context_menu(mascot, position):
    menu = QMenu(mascot)

    # レベル表示用のアクションを作成
    level_action = QAction(f"レベル: {mascot.level}", mascot)
    level_action.triggered.connect(lambda: show_level(mascot))

    # 「話す」アクションを作成
    talk_action = QAction("話す", mascot)
    talk_action.triggered.connect(lambda: auto_talk(mascot))

    # 「終了」アクションを作成
    quit_action = QAction("終了", mascot)
    quit_action.triggered.connect(mascot.close)

    # メニューにアクションを追加
    menu.addAction(level_action)
    menu.addAction(talk_action)
    menu.addAction(quit_action)

    # メニューを表示
    menu.exec(mascot.mapToGlobal(position))
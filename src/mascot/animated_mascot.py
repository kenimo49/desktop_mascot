from PyQt6.QtWidgets import QMainWindow
from src.mascot.timers import setup_timers
from src.mascot.menu import init_menu
from src.mascot.interaction.drag import init_drag
from src.mascot.profile.base import init_profile
from src.mascot.display.base import setup_display
from src.database.controller.keylogger_setting import get_keylogger_status


class AnimatedMascot(QMainWindow):
    def __init__(self):
        super().__init__()
        setup_display(self)
        # 吹き出しウィジェットを初期化（非表示）
        self.speech_bubble = None
        self.is_keylogger_active = get_keylogger_status()
        # プロフィールの初期設定
        init_profile(self)
        # タイマーの設定
        setup_timers(self)
        # ドラッグ機能を追加
        init_drag(self)
        # メニューを初期化
        init_menu(self)


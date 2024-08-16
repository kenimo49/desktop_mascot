from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
import sys
from src.mascot.animated_mascot import AnimatedMascot
from src.database import initialize_database
from src.database.seed import run_all_seeds
from src.database.controller.system_status import is_initialized, set_initialized


if __name__ == "__main__":
    # データベースの初期化（テーブルの作成）
    initialize_database()
    # 初期化が必要か確認
    if not is_initialized():
        print("初期データの挿入が必要です。")
        # 初期データの挿入
        run_all_seeds()
        # 初期化済みフラグを設定
        set_initialized()

    app = QApplication(sys.argv)
    # アプリケーションのアイコンを設定
    app.setWindowIcon(QIcon("image/icon/icon.ico"))
    window = AnimatedMascot()
    window.show()
    sys.exit(app.exec())
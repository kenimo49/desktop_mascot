from src.mascot.talk import auto_talk, talk
from src.mascot.animation.moving_around import start_moving_around
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt
from src.mascot.profile.base import show_level
from src.database import session
from src.database.models.tweet_model import Tweet
from src.dialog.add_tweet_dialog import AddTweetDialog
from PyQt6.QtWidgets import QMenu, QWidgetAction, QLabel, QWidget, QVBoxLayout, QMessageBox
from src.dialog.setting_dialog import SettingsDialog
from src.database.controller.keylogger_setting import set_keylogger_status
from src.dialog.task_manager_dialog import TaskManagerDialog


MENU_STYLE = """
        QMenu {
            background-color: #1c1c1c; /* メニュー全体の背景色：ダークグレー */
            border: 1px solid #333;   /* ボーダーの色：やや明るめのグレー */
            color: #b0b0b0;           /* メニュー項目の文字色：淡いグレー */
        }
        QMenu::item {
            font-family: "Roboto", "Helvetica Neue", Arial, sans-serif; /* モダンなフォント */
            padding: 8px 24px; /* メニュー項目のパディング */
            background-color: transparent;
        }
        QMenu::item:selected {
            background-color: #004f80; /* 光沢感のあるダークブルー */
            color: white; /* 項目が選択された時の文字色 */
            border: 1px solid #007acc;  /* 微妙なエッジを付けるためのボーダー */
        }
        QMenu::separator {
            height: 1px;
            background: #444;         /* セパレータの色：暗めのグレー */
            margin-left: 15px;
            margin-right: 15px;
        }
    """

def init_menu(mascot):
    # 右クリックメニュー設定
    mascot.label.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
    mascot.label.customContextMenuRequested.connect(lambda position: show_context_menu(mascot, position))


def show_context_menu(mascot, position):
    menu = QMenu(mascot)

    # メニュー全体のスタイルシートを設定
    menu.setStyleSheet(MENU_STYLE)

    # レベル表示用のアクションを作成
    level_action = QAction(f"レベル: {mascot.level}", mascot)
    level_action.triggered.connect(lambda: show_level(mascot))

    # 「設定」アクションを作成
    settings_action = QAction("設定", mascot)
    settings_action.triggered.connect(lambda: show_settings_dialog(mascot))
    menu.addAction(settings_action)

    # 「話す」アクションを作成
    talk_action = QAction("話す", mascot)
    talk_action.triggered.connect(lambda: auto_talk(mascot))

    # 「アニメーション」アクションを作成
    animation_menu = menu.addMenu("アニメーション")
    animation_action = QAction("走る", mascot)
    animation_action.triggered.connect(lambda: start_moving_around(mascot))
    animation_menu.addAction(animation_action)

    # キーロガーON/OFFアクションを作成
    keylogger_action = QAction("キーロガーを有効にする", mascot)
    keylogger_action.setCheckable(True)
    keylogger_action.setChecked(mascot.is_keylogger_active)
    keylogger_action.triggered.connect(lambda: toggle_keylogger(mascot, keylogger_action))

    menu.addAction(keylogger_action)

    # 「つぶやき」サブメニューを作成
    tweet_menu = menu.addMenu("つぶやき")

    # 「つぶやきの追加」アクションを作成し、サブメニューの一番上に追加
    add_tweet_action = CustomMenuAction("つぶやきの追加", mascot)
    add_tweet_action.triggered.connect(lambda: add_tweet(mascot))
    add_tweet_action.setObjectName("add-tweet")  # カスタムオブジェクト名を設定
    tweet_menu.addAction(add_tweet_action)


    # 登録されているTweetデータのタイトルを取得し、サブメニューに追加
    tweets = session.query(Tweet).all()
    for tweet in tweets:
        tweet_sub_menu = QMenu(tweet.title, mascot)
        tweet_sub_menu.setStyleSheet(MENU_STYLE)

        # 「つぶやく」アクション
        tweet_action = QAction("つぶやく", mascot)
        tweet_action.triggered.connect(
            lambda checked, t=tweet: talk(mascot, t.content, t.get_images() if t.get_images() else None,
                                          close_timeout=5000))
        tweet_sub_menu.addAction(tweet_action)

        # 「削除」アクション
        delete_action = QAction("削除", mascot)
        delete_action.triggered.connect(lambda checked, t=tweet: delete_tweet(mascot, t))
        tweet_sub_menu.addAction(delete_action)

        tweet_menu.addMenu(tweet_sub_menu)

    # 「タスク管理」アクションを追加
    task_manager_action = QAction("タスク管理", mascot)
    task_manager_action.triggered.connect(lambda: open_task_manager(mascot))
    menu.addAction(task_manager_action)

    # 「終了」アクションを作成
    quit_action = QAction("終了", mascot)
    quit_action.triggered.connect(mascot.close)

    # メニューにアクションを追加
    menu.addAction(level_action)
    menu.addAction(talk_action)
    menu.addAction(quit_action)

    # メニューを表示
    menu.exec(mascot.mapToGlobal(position))

def open_task_manager(mascot):
    dialog = TaskManagerDialog(mascot)
    dialog.exec()

def toggle_keylogger(mascot, action):
    if action.isChecked():
        mascot.is_keylogger_active = True
        action.setText("キーロガーを無効にする")
        set_keylogger_status(True)  # データベースに状態を保存
    else:
        mascot.is_keylogger_active = False
        # リスナーを停止する場合はその処理を追加
        action.setText("キーロガーを有効にする")
        set_keylogger_status(False)  #


def add_tweet(mascot):
    dialog = AddTweetDialog(mascot)
    if dialog.exec():
        # ダイアログで追加された後の処理（必要なら）
        pass


def show_settings_dialog(mascot):
    dialog = SettingsDialog(mascot)
    dialog.exec()


def delete_tweet(mascot, tweet):
    # 確認ダイアログを表示して削除の確認
    reply = QMessageBox.question(mascot, "削除確認", f"本当に「{tweet.title}」を削除しますか？",
                                 QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                 QMessageBox.StandardButton.No)

    if reply == QMessageBox.StandardButton.Yes:
        # データベースから該当のTweetを削除
        session.delete(tweet)
        session.commit()
        QMessageBox.information(mascot, "削除完了", f"「{tweet.title}」を削除しました。")


class CustomMenuAction(QWidgetAction):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.widget = QWidget(parent)
        layout = QVBoxLayout(self.widget)
        label = QLabel(text, self.widget)
        label.setStyleSheet("""
            QLabel {
                color: white; 
                background-color: #1c1c1c; 
                padding: 5px; 
                border: 1px solid #333;
            }
            QLabel:hover {
                background-color: #004f80; /* 光沢感のあるダークブルー */
                color: white; /* 項目が選択された時の文字色 */
                border: 1px solid #007acc;  /* 微妙なエッジを付けるためのボーダー */
            }
            
        """)  # 常に色を変える
        layout.addWidget(label)
        self.setDefaultWidget(self.widget)
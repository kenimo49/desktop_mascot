from src.database.seed.tweet import seed_tweets
from src.database.seed.timer_setting import seed_timer_setting
from src.database.seed.keylogger_setting import seed_keylogger_setting
from src.database.seed.task import seed_tasks


def run_all_seeds():
    # 初期データとして追加したいデータを追加する関数を呼び出す
    seed_tweets()
    seed_timer_setting()
    seed_keylogger_setting()
    seed_tasks()

    print("すべての初期データの挿入が完了しました。")

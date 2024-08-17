from src.database.seed.tweet import seed_tweets
from src.database.seed.timer_setting import seed_timer_setting


def run_all_seeds():
    # 初期データとして追加したいデータを追加する関数を呼び出す
    seed_tweets()
    seed_timer_setting()

    print("すべての初期データの挿入が完了しました。")

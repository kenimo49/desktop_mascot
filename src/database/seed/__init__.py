from src.database.seed.seed_tweet import seed_tweets


def run_all_seeds():
    # 初期データとして追加したいデータを追加する関数を呼び出す
    seed_tweets()

    print("すべての初期データの挿入が完了しました。")
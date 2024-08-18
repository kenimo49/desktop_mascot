from src.database.models.task import Task
from src.database import session

def seed_tasks():
    initial_tasks = [
        Task(title="レポート作成", description="月次レポートを作成する"),
        Task(title="プレゼン資料の準備", description="次回会議のプレゼン資料を準備する"),
        Task(title="顧客フォローアップ", description="顧客へのフォローアップを行う"),
    ]

    session.bulk_save_objects(initial_tasks)
    session.commit()

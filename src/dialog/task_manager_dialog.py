from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QTreeWidget, QTreeWidgetItem, QInputDialog, QMessageBox, QComboBox
from src.database import session
from src.database.models.task import Task
from src.database.models.sub_task import SubTask

class TaskManagerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("タスク管理")
        self.setGeometry(100, 100, 600, 400)

        self.layout = QVBoxLayout(self)

        # タスク一覧表示ツリーテーブル
        self.tree = QTreeWidget(self)
        self.tree.setColumnCount(3)
        self.tree.setHeaderLabels(["タスク/サブタスク", "詳細", "状態"])

        # カラムの幅を指定の比率に基づいて設定
        total_width = self.width()
        self.tree.setColumnWidth(0, int(total_width * 0.35))  # タスク/サブタスク列の幅を40%
        self.tree.setColumnWidth(1, int(total_width * 0.35))  # 詳細列の幅を40%
        self.tree.setColumnWidth(2, int(total_width * 0.2))  # 状態列の幅を20%

        self.layout.addWidget(self.tree)

        # ボタンのレイアウト
        button_layout = QHBoxLayout()

        # タスク追加ボタン
        self.add_task_button = QPushButton("タスク追加")
        self.add_task_button.clicked.connect(self.add_task)
        button_layout.addWidget(self.add_task_button)

        # サブタスク追加ボタン
        self.add_subtask_button = QPushButton("サブタスク追加")
        self.add_subtask_button.clicked.connect(self.add_subtask)
        button_layout.addWidget(self.add_subtask_button)

        # 削除ボタン
        self.delete_button = QPushButton("選択したタスク/サブタスクを削除")
        self.delete_button.clicked.connect(self.delete_task_or_subtask)
        button_layout.addWidget(self.delete_button)

        self.layout.addLayout(button_layout)

        # タスクの読み込み
        self.load_tasks()

    def load_tasks(self):
        self.tree.clear()
        tasks = session.query(Task).all()

        for task in tasks:
            task_item = QTreeWidgetItem(self.tree, [task.title, task.description or ""])

            # 状態を表示するコンボボックス
            task_status_combo = QComboBox(self)
            task_status_combo.addItems(["未完了", "進行中", "完了"])
            task_status_combo.setCurrentText(task.status)
            task_status_combo.currentTextChanged.connect(lambda text, t=task: self.update_task_status(t, text))
            self.tree.setItemWidget(task_item, 2, task_status_combo)

            # サブタスクをツリーに追加
            subtasks = session.query(SubTask).filter_by(task_id=task.id).all()
            for subtask in subtasks:
                subtask_item = QTreeWidgetItem(task_item, [subtask.title, subtask.description or ""])

                # サブタスクの状態を表示するコンボボックス
                subtask_status_combo = QComboBox(self)
                subtask_status_combo.addItems(["未完了", "進行中", "完了"])
                subtask_status_combo.setCurrentText(subtask.status)
                subtask_status_combo.currentTextChanged.connect(lambda text, st=subtask: self.update_subtask_status(st, text))
                self.tree.setItemWidget(subtask_item, 2, subtask_status_combo)

            task_item.setExpanded(True)  # タスクを展開した状態で表示

    def add_task(self):
        title, ok = QInputDialog.getText(self, "タスク追加", "タスク名を入力してください:")
        if ok and title:
            description, ok = QInputDialog.getText(self, "タスク詳細", "タスクの詳細を入力してください（任意）:")
            if ok:
                new_task = Task(title=title, description=description or "", status="未完了")
                session.add(new_task)
                session.commit()
                self.load_tasks()

    def add_subtask(self):
        selected_item = self.tree.currentItem()
        if not selected_item or not selected_item.parent() is None:
            QMessageBox.warning(self, "警告", "サブタスクを追加するタスクを選択してください。")
            return

        task_title = selected_item.text(0)
        task = session.query(Task).filter_by(title=task_title).first()

        title, ok = QInputDialog.getText(self, "サブタスク追加", "サブタスク名を入力してください:")
        if ok and title:
            description, ok = QInputDialog.getText(self, "サブタスク詳細", "サブタスクの詳細を入力してください（任意）:")
            if ok:
                new_subtask = SubTask(task_id=task.id, title=title, description=description or "", status="未完了")
                session.add(new_subtask)
                session.commit()
                self.load_tasks()

    def delete_task_or_subtask(self):
        selected_item = self.tree.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "警告", "削除するタスク/サブタスクを選択してください。")
            return

        parent_item = selected_item.parent()

        if parent_item:  # サブタスクの場合
            subtask_title = selected_item.text(0)
            task_title = parent_item.text(0)
            task = session.query(Task).filter_by(title=task_title).first()
            subtask = session.query(SubTask).filter_by(task_id=task.id, title=subtask_title).first()
            if subtask:
                session.delete(subtask)
                session.commit()
                self.load_tasks()
        else:  # タスクの場合
            task_title = selected_item.text(0)
            task = session.query(Task).filter_by(title=task_title).first()
            if task:
                session.delete(task)
                session.commit()
                self.load_tasks()

    def update_task_status(self, task, status):
        if task:
            task.status = status
            session.commit()

    def update_subtask_status(self, subtask, status):
        if subtask:
            subtask.status = status
            session.commit()

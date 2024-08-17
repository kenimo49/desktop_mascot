from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton, QHBoxLayout
from src.database import session
from src.database.enums.timer_name import TimerName
from src.database.models.timer_setting import TimerSettings


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("タイマー設定")
        self.setFixedSize(300, 200)

        # レイアウトの初期化
        layout = QVBoxLayout(self)

        # タイマーの選択肢（ミリ秒単位）
        self.timer_options = {
            "30秒": 30000,
            "1分": 60000,
            "5分": 300000,
            "10分": 600000,
            "30分": 1800000,
            "1時間": 3600000,
            "3時間": 10800000,
            "6時間": 21600000,
            "12時間": 43200000,
            "なし": 0
        }

        # 各タイマー設定を表示するラベルとコンボボックス
        self.timer_combo_boxes = {}
        for timer_name in TimerName:
            if timer_name == TimerName.UPDATE_TIMER:
                continue
            timer_setting = session.query(TimerSettings).filter_by(name=timer_name).first()

            label = QLabel(f"{timer_name.display_name}:", self)
            combobox = QComboBox(self)

            # コンボボックスに選択肢を追加
            for text, ms in self.timer_options.items():
                combobox.addItem(text, ms)

            # 現在の設定を選択
            current_interval = timer_setting.interval if timer_setting else 30000
            index = combobox.findData(current_interval)
            if index != -1:
                combobox.setCurrentIndex(index)

            self.timer_combo_boxes[timer_name] = combobox

            # ラベルとコンボボックスをレイアウトに追加
            timer_layout = QHBoxLayout()
            timer_layout.addWidget(label)
            timer_layout.addWidget(combobox)
            layout.addLayout(timer_layout)

        # 保存ボタン
        save_button = QPushButton("保存", self)
        save_button.clicked.connect(self.save_settings)
        layout.addWidget(save_button)

    def save_settings(self):
        # コンボボックスの値を取得してデータベースに保存
        for timer_name, combo_box in self.timer_combo_boxes.items():
            interval = combo_box.currentData()
            timer_setting = session.query(TimerSettings).filter_by(name=timer_name).first()
            if timer_setting:
                timer_setting.interval = interval
            else:
                # 設定が存在しない場合は新たに作成
                new_setting = TimerSettings(name=timer_name, interval=interval)
                session.add(new_setting)

        session.commit()
        self.accept()  # ダイアログを閉じる

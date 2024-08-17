from enum import Enum


class TimerName(Enum):
    UPDATE_TIMER = ("アニメーション更新タイマー", "update_timer")
    AUTO_TALK_TIMER = ("自動会話タイマー", "auto_talk_timer")
    MOVE_TIMER = ("移動タイマー", "move_timer")

    def __init__(self, display_name, internal_name):
        self.display_name = display_name
        self.internal_name = internal_name

    def __str__(self):
        return self.display_name

    @classmethod
    def get_by_internal_name(cls, internal_name):
        for timer in cls:
            if timer.internal_name == internal_name:
                return timer
        raise ValueError(f"{internal_name} は TimerName に存在しません。")
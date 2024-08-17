from src.database.models.keylogger_setting import KeyloggerSetting
from src.database import session


def seed_keylogger_setting():
    # 初期値として False を設定
    initial_setting = KeyloggerSetting(is_enabled=False)

    # 既存の設定がない場合にのみ挿入
    existing_setting = session.query(KeyloggerSetting).first()
    if not existing_setting:
        session.add(initial_setting)
        session.commit()
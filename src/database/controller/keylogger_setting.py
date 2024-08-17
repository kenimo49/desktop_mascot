from src.database import session
from src.database.models.keylogger_setting import KeyloggerSetting


def get_keylogger_status():
    setting = session.query(KeyloggerSetting).first()
    if not setting:
        setting = KeyloggerSetting(is_enabled=False)
        session.add(setting)
        session.commit()
    return setting.is_enabled


def set_keylogger_status(is_enabled):
    setting = session.query(KeyloggerSetting).first()
    if setting:
        setting.is_enabled = is_enabled
        session.commit()

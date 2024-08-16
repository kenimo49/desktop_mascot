from src.database import session
from src.database.models.system_status import SystemStatus


def is_initialized():
    status = session.query(SystemStatus).filter_by(status_key="initialized").first()
    return status is not None and status.status_value


def set_initialized():
    status = session.query(SystemStatus).filter_by(status_key="initialized").first()
    if status is None:
        status = SystemStatus(status_key="initialized", status_value=True)
        session.add(status)
    else:
        status.status_value = True
    session.commit()
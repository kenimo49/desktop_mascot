from src.database import session
from src.database.models.task import Task

def add_task(title, description):
    new_task = Task(title=title, description=description)
    session.add(new_task)
    session.commit()

def get_all_tasks():
    return session.query(Task).all()

def update_task_status(task_id, new_status):
    task = session.query(Task).filter_by(id=task_id).first()
    if task:
        task.status = new_status
        session.commit()

def delete_task(task_id):
    task = session.query(Task).filter_by(id=task_id).first()
    if task:
        session.delete(task)
        session.commit()

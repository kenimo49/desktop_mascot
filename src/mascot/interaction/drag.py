# ドラッグアンドドロップに関する処理を記述する

def init_drag(mascot):
    mascot.label.mousePressEvent = lambda event: start_drag(mascot, event)
    mascot.label.mouseMoveEvent = lambda event: do_drag(mascot, event)


def start_drag(mascot, event):
    mascot.drag_start_x = event.position().x()
    mascot.drag_start_y = event.position().y()


def do_drag(mascot, event):
    x = mascot.x() + (event.position().x() - mascot.drag_start_x)
    y = mascot.y() + (event.position().y() - mascot.drag_start_y)
    mascot.move(x, y)
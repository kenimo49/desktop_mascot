from PyQt6.QtWidgets import QApplication
import sys
from src.mascot.animated_mascot import AnimatedMascot


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AnimatedMascot()
    window.show()
    sys.exit(app.exec())
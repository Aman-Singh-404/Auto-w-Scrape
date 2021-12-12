import sys

from PyQt5.QtWidgets import QApplication, QMessageBox

from src.structure.Window import Window
from Utils import excepthook

if __name__ == "__main__":
    main_app: QApplication = QApplication(sys.argv)
    # Starting window
    sys.excepthook = excepthook
    print("Application started...")

    window: Window = Window()
    window.show()
    main_app.exec_()

    # Stopping window
    print("Application stopped.")
    sys.exit()

import sys
import traceback

from PyQt5.QtWidgets import QApplication, QMessageBox

from Structure.Window import Window

if __name__ == "__main__":
    main_app: QApplication = QApplication(sys.argv);
    try:
        # Starting window
        window: Window = Window();
        window.show();
        main_app.exec_();
    except Exception as err:
        # Handling any error/exception occurrence
        QMessageBox.critical(None, "Error occurred", str(err));
        traceback.print_exc();

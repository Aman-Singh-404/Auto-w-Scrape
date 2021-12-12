import re
import traceback

from PyQt5.QtWidgets import QApplication, QMessageBox

from resource.constants import PROFILE

def validHTMLTag(htmlTag: str) -> bool:
    return re.match(r"^<(\"[^\"]*\"|'[^']*'|[^'\">])*>$", htmlTag.strip()) != None

def excepthook(error_type, error_message, error_traceback):
    # Handling any error/exception occurrence
    tracelog: str = "".join(traceback.format_exception(error_type, error_message, error_traceback))
    QMessageBox.critical(None, "Error occurred", tracelog.splitlines()[-1])

    # If software is under development, then log error
    if PROFILE == "dev":
        print(tracelog)
    QApplication.quit()


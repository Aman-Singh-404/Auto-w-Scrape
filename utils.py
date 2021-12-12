"""
Common functionalities
"""

import re
import traceback

from PyQt5.QtWidgets import QApplication, QMessageBox

from constants import PROFILE


def validHTMLTag(html_tag: str) -> bool:
    '''
    Handling any error/exception occurrence
    '''
    return re.match(r"^<(\"[^\"]*\"|'[^']*'|[^'\">])*>$", html_tag.strip()) is not None


def excepthook(error_type, error_message, error_traceback) -> None:
    '''
    Handling any error/exception occurrence
    '''
    # Creating trace log
    tracelog: str = "".join(traceback.format_exception(
        error_type, error_message, error_traceback))
    QMessageBox.critical(None, "Error occurred", tracelog.splitlines()[-1])

    # If software is under development, then log error
    if PROFILE == "dev":
        print(tracelog)
    QApplication.quit()

import re

from PyQt5.QtWidgets import QDialog, QMessageBox
from sqlalchemy import create_engine

from Interface.UI_saveDB import Ui_Dialog


class SaveDB(QDialog):
    def __init__(self, parent, str_engine="", table=""):
        QDialog.__init__(self, parent=parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setFixedSize(self.size())
        self.engine_url = str_engine

        self.ui.tableLE.setText(table)
        if str_engine != "":
            urlpart = re.findall(r"^(.+):\/\/(.+):(.+)@(.+)\/(.+)", str_engine)[0]
            self.ui.dialectCB.setCurrentText(urlpart[0])
            self.ui.userLE.setText(urlpart[1])
            self.ui.passwordLE.setText(urlpart[2])
            self.ui.hostportLE.setText(urlpart[3])
            self.ui.dbLE.setText(urlpart[4])

        self.ui.buttonBox.accepted.connect(self.verify)
        self.ui.buttonBox.rejected.connect(self.reject)

    def run(self):
        if self.exec_():
            table = self.ui.tableLE.text()
            return [self.engine_url, table]
        self.show()

    def verify(self):
        if self.ui.userLE.text() == "":
            QMessageBox.warning(self, "Alert", "Username can't be empty.")
        elif self.ui.hostportLE.text() == "":
            QMessageBox.warning(self, "Alert", "Host:port can't be empty.")
        elif self.ui.dbLE.text() == "":
            QMessageBox.warning(self, "Alert", "Database can't be empty.")
        elif self.ui.tableLE.text() == "":
            QMessageBox.warning(self, "Alert", "Table can't be empty.")
        else:
            try:
                str_engine = self.ui.dialectCB.currentText().strip() + "://"
                str_engine += self.ui.userLE.text().strip() + ":"
                str_engine += self.ui.passwordLE.text().strip() + "@"
                str_engine += self.ui.hostportLE.text().strip() + "/"
                str_engine += self.ui.dbLE.text().strip()

                engine = create_engine(str_engine)
                conn = engine.connect()
                conn.close()
                engine.dispose()
                self.engine_url = str_engine
                self.accept()
            except:
                QMessageBox.warning(self, "Alert", "Database URL not found.")

import platform
import sys
from threading import Thread

import pandas as pd
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from sqlalchemy import create_engine

from Interface.UI_progressView import Ui_Dialog
from Structure.Driver import Driver


class ProgressView(QDialog):
    def __init__(self, parent, pathlist, urllist, saveto, header, progress):
        QDialog.__init__(self, parent=parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setFixedSize(self.size())

        self.urllist = urllist
        self.saveto = saveto
        self.header = header
        self.index = 0
        self.stepsize = 1 / len(self.urllist) * 100
        index_dict = {}
        for node in header:
            index_dict[node] = 0
        self.driver = Driver(self, pathlist, self.urllist, index_dict)
        self.threads = []

        self.ui.closePB.clicked.connect(self.reject)
        self.ui.executePB.clicked.connect(self.execute)
        self.ui.pausePB.clicked.connect(self.pauseStatus)
        self.ui.cancelPB.clicked.connect(self.changeStatus)
        self.ui.savePB.clicked.connect(self.changeStatus)
        self.ui.stopPB.clicked.connect(self.changeStatus)

    def changeStatus(self):
        sender = self.sender().text()
        if sender == "Cancel URL":
            self.driver.status_code = 1
        elif sender == "Save and Stop":
            self.driver.status_code = 2
        else:
            self.driver.status_code = 3

    def checkBrowser(self):
        try:
            path = "Webdriver/Chrome/"
            operating = sys.platform
            if operating == "linux":
                path += "linux"
            elif operating == "win32":
                path += "win.exe"
            else:
                path += "mac"
            return "Chrome", path
        except:
            try:
                path = "Webdriver/Firefox/"
                operating = sys.platform
                bitsize = platform.architecture()[0][0]
                if operating == "linux":
                    if bitsize == "6":
                        path += "linux64"
                    else:
                        path += "linux32"
                elif operating == "win32":
                    if bitsize == "6":
                        path += "win64.exe"
                    else:
                        path += "win32.exe"
                else:
                    path += "mac"
                return "Firefox", path
            except:
                QMessageBox.warning(
                    self, "Alert", "System doesn't have firfox or chrome browser."
                )

    def closeEvent(self, event):
        if not self.ui.closePB.isEnabled():
            reply = QMessageBox.question(
                self,
                "Alert",
                "You will lost all scraped data.",
                QMessageBox.Cancel | QMessageBox.Ok,
                QMessageBox.Cancel,
            )
            if reply == QMessageBox.Ok:
                event.accept()
                for thread in self.threads:
                    thread.quit()
                    thread.wait()
            else:
                event.ignore()
        else:
            event.accept()

    @pyqtSlot()
    def decrementIndex(self):
        self.index -= 1

    def execute(self):
        browser, path = self.checkBrowser()
        if path != None:
            self.ui.label_1.setEnabled(False)
            self.ui.closePB.setEnabled(False)
            self.ui.executePB.setEnabled(False)

            self.ui.label_2.setEnabled(True)
            self.ui.label_2.setText(
                "Wait! Process is ongoing...\n"
                + str(self.index + 1)
                + ". "
                + self.urllist[self.index]
            )
            self.ui.progressPB.setEnabled(True)
            self.ui.pausePB.setEnabled(True)
            self.ui.cancelPB.setEnabled(True)
            self.ui.savePB.setEnabled(True)
            self.ui.stopPB.setEnabled(True)
            QApplication.processEvents()

            self.driver.get(browser, path)
            thread = QThread()
            self.threads.append(thread)
            self.driver.moveToThread(thread)
            thread.started.connect(self.driver.execute)
            thread.start()
        else:
            self.reject()

    @pyqtSlot()
    def notify(self):
        if self.index + 1 == len(self.urllist):
            self.ui.progressPB.setValue(100)
        else:
            self.index += 1
            self.ui.label_2.setText(
                "Wait! Process is ongoing...\n"
                + str(self.index + 1)
                + ". "
                + self.urllist[self.index]
            )
            self.ui.progressPB.setValue(int(self.index * self.stepsize))

    def pauseStatus(self):
        if self.ui.pausePB.text() == "Pause":
            self.ui.pausePB.setText("Resume")
            self.driver.pause_code = True
        else:
            self.ui.pausePB.setText("Pause")
            self.driver.pause_code = False

    def run(self):
        if self.exec_():
            return self.ui.progressPB.value()
        self.show()

    @pyqtSlot(list)
    def saveResult(self, datamatrix):
        for i in range(len(datamatrix)):
            if type(datamatrix[i][1]) == str:
                data_dict = {}
                for key in self.header:
                    data_dict[key] = [datamatrix[i][1]]
                datamatrix[i][1] = data_dict
        if len(datamatrix):
            df_total = pd.DataFrame(datamatrix[0][1])
            df_total.insert(0, "URL", datamatrix[0][0])

            for i in range(1, len(datamatrix)):
                df = pd.DataFrame(datamatrix[i][1])
                df.insert(0, "URL", datamatrix[i][0])
                df_total = df_total.append(df, ignore_index=True)

            if self.saveto[0]:
                engine = create_engine(self.saveto[1])
                conn = engine.connect()
                df_total.to_sql(self.saveto[2], conn)
                conn.close()
                db.dispose()
            else:
                df_total.to_excel(self.saveto[1], index=False)
        QMessageBox.about(self, "Information", "Process is completed.")
        for thread in self.threads:
            thread.quit()
            thread.wait()
        self.accept()

    @pyqtSlot(str)
    def showError(self, msg):
        QMessageBox.warning(self, "Alert", msg)
        for thread in self.threads:
            thread.quit()
            thread.wait()
        self.reject()

import platform
import sys

import pandas as pd
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from selenium.common.exceptions import NoSuchWindowException
from sqlalchemy import create_engine

from Interface.UI_progressView import Ui_Dialog
from Structure.Driver import Driver


class ProgressView(QDialog):
    def __init__(self, parent, pathlist, urllist, saveto):
        QDialog.__init__(self, parent=parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setFixedSize(self.size())

        self.pathlist = pathlist
        self.urllist = urllist
        self.saveto = saveto
        
        self.ui.closePB.clicked.connect(self.reject)
        self.ui.executePB.clicked.connect(self.execute)
    
    def checkBrowser(self):
        try:
            path = "Webdriver/Firefox/"
            operating = sys.platform
            bitsize = platform.architecture()[0][0]
            if operating == "linux":
                if bitsize == '6':
                    path += "linux64"
                else:
                    path += "linux32"
            elif operating == "win32":
                if bitsize == '6':
                    path += "win64.exe"
                else:
                    path += "win32.exe"
            else:
                path += "mac"
            return "Firefox", path
        except:
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
                QMessageBox.warning(self, "Alert", "System doesn't have firfox or chrome browser.")
    
    def closeEvent(self, event):
        if not self.ui.closePB.isEnabled():
            reply = QMessageBox.question(self, 'Alert', 'You will lost all scraped data.',QMessageBox.Cancel | QMessageBox.Ok, QMessageBox.Cancel)
            if reply == QMessageBox.Ok:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()
    
    def execute(self):
        browser, path = self.checkBrowser()
        if path != None:
            self.ui.label.setText("Wait...Process is on work!\nTake a seat since process will take some time.\nPlease don't interfere in the browser process.")
            self.ui.closePB.setEnabled(False)
            self.ui.executePB.setEnabled(False)
            QApplication.processEvents()
            try:
                driver = Driver(browser, path, self.pathlist, self.urllist)
                datamatrix = driver.execute()
                
                df_total = pd.DataFrame(datamatrix[0][1])
                df_total.insert(0, 'URL', datamatrix[0][0])
                for i in range(1, len(datamatrix)):
                    df = pd.DataFrame(datamatrix[i][1])
                    df.insert(0, 'URL', datamatrix[i][0])
                    df_total.append(df, ignore_index=True)
                if self.saveto[0]:
                    engine = create_engine(self.saveto[1])
                    df_total.to_sql(self.saveto[2], engine.connect())
                else:
                    df_total.to_excel(self.saveto[1], index=False)
                QMessageBox.about(self, "Information", "Process is completed.")
                self.accept()
            except NoSuchWindowException:
                QMessageBox.warning(self, "Alert", "Browser has beeen stop working.")
                self.reject()
            except:
                QMessageBox.warning(self, "Alert", "File can't be placed due to incorrect path or url.")
                self.reject()
        else:
            self.reject()

import json
import sys

from PyQt5.QtWidgets import QApplication, QMessageBox

from Structure.Window import Window
import traceback


class Controller:
    def __init__(self):
        self.main_app = QApplication(["No Configuration"])
        self.log = "log"
        self.main_window_count = 0
        self.main_window = []
        controller_count = self.read("controller_count")
        self.write("controller_count", controller_count + 1)

    def addWindow(self, open_file=""):
        reusable_titles = self.read("reusable_titles")
        index = self.read("index")
        window = None
        if reusable_titles != []:
            window = Window(self, reusable_titles[0])
            self.setValue("reusable_titles", reusable_titles[0], False)
        else:
            window = Window(self, "Untitled " + str(index))
            self.write("index", index + 1)
        self.main_window_count += 1
        window.show()
        self.main_window.append(window)
        if open_file != "":
            self.setValue("defaulter_files", open_file)
            window.setStat(open_file)

    def check(self, label, value):
        dataFile = self.read(label)
        if value in dataFile:
            return True
        else:
            return False

    def closeWindow(self, window):
        if self.check("defaulter_files", window):
            self.setValue("defaulter_files", window.saveto, False)
        self.setValue("reusable_titles", window.title)
        self.main_window_count -= 1
        self.main_window.remove(window)
        for window in self.main_window:
            window.show()
        if not self.main_window_count:
            controller_count = self.read("controller_count") - 1
            self.write("controller_count", controller_count)
            if not controller_count:
                self.setDefault_to_Log()
            del ()

    def read(self, label):
        with open(self.log, "r", encoding="utf-8") as fle:
            stat = json.load(fle)
            return stat[label]

    def setDefault_to_Log(self):
        stat = {
            "controller_count": 0,
            "defaulter_files": [],
            "index": 1,
            "reusable_titles": [],
        }
        with open(self.log, "w", encoding="utf-8") as fle:
            json.dump(stat, fle, ensure_ascii=False, indent=4)

    def setValue(self, label, value, insert_flag=True):
        dataFile = self.read(label)
        if insert_flag:
            dataFile.append(value)
        else:
            dataFile.remove(value)
        self.write(label, dataFile)

    def write(self, label, value):
        stat = {}
        with open(self.log, "r", encoding="utf-8") as fle:
            stat = json.load(fle)
        stat[label] = value
        with open(self.log, "w", encoding="utf-8") as fle:
            json.dump(stat, fle, ensure_ascii=False, indent=4)

controller = Controller()

def excepthook(error_type, error_message, error_traceback):
    tracelog: str = "".join(
        traceback.format_exception(error_type, error_message, error_traceback)
    )
    QMessageBox.critical(None, "Error occurred", tracelog.splitlines()[-1])
    print(tracelog)
    QApplication.quit()
    controller.setDefault_to_Log()


if __name__ == "__main__":
    sys.excepthook = excepthook
    controller.addWindow()
    controller.main_app.exec_()

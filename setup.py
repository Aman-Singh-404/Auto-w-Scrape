import sys

from PyQt5 import QtWidgets

from Structure_Window import Window


class Controller:
    def __init__(self):
        self.main_app = QtWidgets.QApplication(['No Configuration'])
        self.index = 1
        self.main_window = []
        self.reusable_titles = []
        self.defaulter_files = []

    def addWindow(self, open_file=''):
        if open_file in self.defaulter_files:
            QtWidgets.QMessageBox.warning(None, 'Alert', "File is already open.")
            return None
        if self.reusable_titles != []:
            self.main_window.append(Window(self, self.reusable_titles[0]))
            self.reusable_titles.pop(0)
        else:
            self.main_window.append(Window(self, 'Untitled ' + str(self.index)))
            self.index += 1
        self.main_window[-1].show()
        if open_file != '':
            self.defaulter_files.append(open_file)
            self.main_window[-1].setStat(open_file)
    
    def closeWindow(self, window):
        if window.saveto in self.defaulter_files:
            self.defaulter_files.remove(window.saveto)
        self.main_window.remove(window)
        if self.main_window == []:
            del()


if __name__ == "__main__":
    controller = Controller()
    controller.addWindow()
    controller.main_app.exec_()

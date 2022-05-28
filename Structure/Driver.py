import os
import re
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup
from PyQt5.QtCore import QObject, pyqtSignal
from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    WebDriverException,
)
from selenium.webdriver.support.ui import Select


class Driver(QObject):
    signalIndex = pyqtSignal()
    signalProgress = pyqtSignal()
    signalReject = pyqtSignal(str)
    signalSave = pyqtSignal(list)

    def __init__(self, parent, path_list, url_list, index_dict):
        super(Driver, self).__init__(parent=None)
        self.driver = None
        self.pathList = path_list
        self.urlList = url_list
        self.state = []
        self.tab = 1
        self.pause_code = False
        self.status_code = 0
        self.file_Data = []
        self.index_dict = index_dict

        self.signalIndex.connect(parent.decrementIndex)
        self.signalProgress.connect(parent.notify)
        self.signalReject.connect(parent.showError)
        self.signalSave.connect(parent.saveResult)

    def checkStatus(self):
        while self.pause_code:
            self.driver.minimize_window()
        if self.status_code:
            raise Exception

    def converttoXPATH(self, tag):
        self.driver.minimize_window()
        element = BeautifulSoup(tag, "lxml").find("body").findChild()
        xpath = "//" + element.name + "[@"
        if element.attrs == {}:
            return xpath[:-2]
        for key, value in element.attrs.items():
            if type(value) == list:
                xpath += key + "='" + " ".join(value) + "' and @"
            else:
                xpath += key + "='" + value + "' and @"
        return xpath[:-6] + "]"

    def evaluateAction(self, node, path):
        self.checkStatus()
        self.driver.minimize_window()
        dataList = {}
        if node.attribute[0] == "Click":
            xpath = self.converttoXPATH(node.attribute[1])
            if not self.wait(xpath):
                raise NoSuchElementException("ELEMENT_NOT_FOUND_" + node.text())
            elements = self.driver.find_elements_by_xpath(xpath)

            index = path.index(node)
            pre_path = path[:index]
            post_path = path[index + 1 :]

            elements[0].click()
            time.sleep(5)
            for label, value in self.executePath(post_path).items():
                if dataList.get(label) == None:
                    dataList[label] = []
                dataList[label] += value
            for i in range(1, len(elements)):
                self.executePath(pre_path)
                element = self.driver.find_elements_by_xpath(xpath)[i]
                element.click()
                time.sleep(5)
                for label, value in self.executePath(post_path).items():
                    if dataList.get(label) == None:
                        dataList[label] = []
                    dataList[label] += value
        else:
            time.sleep(int(node.attribute[1]))
        return dataList

    def evaluateData(self, node):
        self.checkStatus()
        self.driver.minimize_window()
        xpath = self.converttoXPATH(node.attribute[1])
        if not self.wait(xpath):
            return ["ELEMENT_NOT_FOUND_" + node.text()]
        elements = self.driver.find_elements_by_xpath(xpath)
        if node.attribute[0] == "Text":
            if node.attribute[3]:
                [elements[node.attribute[3] - 1].text]
            else:
                return [element.text for element in elements]
        elif node.attribute[0] == "Media":
            if node.attribute[3]:
                return [
                    self.saveFile(
                        elements[node.attribute[3] - 1], node.attribute[2], node.text()
                    )
                ]
            else:
                return [
                    self.saveFile(element, node.attribute[2], node.text())
                    for element in elements
                ]
        else:
            if node.attribute[3]:
                return [
                    self.saveSheet(
                        elements[node.attribute[3] - 1], node.attribute[2], node.text()
                    )
                ]
            else:
                return [
                    self.saveSheet(element, node.attribute[2], node.text())
                    for element in elements
                ]

    def evaluateInput(self, node):
        self.checkStatus()
        self.driver.minimize_window()
        xpath = self.converttoXPATH(node.attribute[1])
        if not self.wait(xpath):
            raise NoSuchElementException("ELEMENT_NOT_FOUND_" + node.text())
        elements = self.driver.find_elements_by_xpath(xpath)
        if node.attribute[0] == "Text/Combo Box":
            for element in elements:
                if element.tag_name == "select":
                    select = Select(element)
                    if node.attribute[2] in [opt.text for opt in select.options]:
                        select.select_by_value(node.attribute[2])
                else:
                    element.send_keys(node.attribute[2])
        else:
            if elements[0].get_attribute("type") == "radio":
                if not elements[0].is_selected():
                    elements[0].click()
            else:
                for element in elements:
                    if not element.is_selected():
                        element.click()

    def execute(self):
        try:
            dataMatrix = []
            self.driver.minimize_window()
            for i in range(len(self.urlList)):
                try:
                    dataList = {}
                    for path in self.pathList:
                        try:
                            self.state.append(("Same", self.urlList[i]))
                            self.driver.get(self.urlList[i])
                            dataList = self.executePath(path)
                            dataMatrix.append([self.urlList[i], dataList])
                            self.state.pop()
                        except NoSuchElementException as err:
                            dataMatrix.append([self.urlList[i], err.msg])
                            continue
                except WebDriverException:
                    dataMatrix.append([self.urlList[i], "URL_NOT_FOUND"])
                except:
                    if self.status_code == 3:
                        self.driver.quit()
                        for path in self.file_Data:
                            os.remove(path)
                        self.signalReject.emit("All URLs cancelled.")
                        return None
                    else:
                        defaulter = [
                            index
                            for index in range(len(dataMatrix))
                            if dataMatrix[index][0] == self.urlList[i]
                        ]
                        defaulter.reverse()
                        for index in defaulter:
                            dataMatrix.pop(index)
                        if self.status_code == 1:
                            dataMatrix.append([self.urlList[i], "URL_CANCELED"])
                        else:
                            self.signalIndex.emit()
                            break
                finally:
                    self.signalProgress.emit()
            self.driver.quit()
            self.signalSave.emit(dataMatrix)
        except:
            self.signalReject.emit("Browser has been stop working.")

    def executePath(self, path):
        self.checkStatus()
        self.driver.minimize_window()
        flag = False
        dataList = {}
        if self.state[-1][1] != self.driver.current_url:
            self.state.append(("Same", self.driver.current_url))
            flag = True
        elif self.tab != len(self.driver.window_handles):
            self.driver.switch_to.window(self.driver.window_handles[-1])
            self.state.append(("New", self.driver.current_url))
            flag = True
            self.tab += 1
        for node in path:
            if node.method == "Action":
                for label, value in self.evaluateAction(node, path).items():
                    if dataList.get(label) == None:
                        dataList[label] = []
                    dataList[label] += value
                break
            elif node.method == "Data":
                dataList[node.text()] = self.evaluateData(node)
            else:
                self.evaluateInput(node)
        if flag:
            value = self.state.pop()
            if value[0] == "Same":
                self.driver.back()
            else:
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[-1])
                self.tab -= 1
            self.driver.refresh()
        return dataList

    def get(self, browser, path):
        if browser == "Firefox":
            self.driver = webdriver.Firefox(executable_path=path)
        else:
            self.driver = webdriver.Chrome(executable_path=path)
        self.driver.minimize_window()
        self.driver.set_window_position(0, 0)
        self.driver.set_window_size(600, 600)

    def saveFile(self, element, path, prefix):
        src = ""
        if element.get_attribute("src") != None:
            src = element.get_attribute("src")
        elif element.get_attribute("href") != None:
            src = element.get_attribute("href")
        else:
            tag = element.get_attribute("outerHTML")
            sre = re.search("(?P<url>https?://[^\s]+)", tag)
            raw_url = sre.group("url")
            src = raw_url[: raw_url.find(tag[sre.span()[0] - 1])]
        req = requests.get(src, stream=True)
        path, base = os.path.split(path)
        base = prefix + "_" + str(self.index_dict[prefix]) + "_" + base
        self.index_dict[prefix] += 1
        fname = os.path.join(path, base)
        with open(fname, "wb") as fle:
            fle.write(req.content)
        self.file_Data.append(fname)
        return fname

    def saveSheet(self, element, path, prefix):
        try:
            path, base = os.path.split(path)
            base = prefix + "_" + str(self.index_dict[prefix]) + "_" + base
            self.index_dict[prefix] += 1
            fname = os.path.join(path, base)
            df = pd.read_html(element.get_attribute("outerHTML"))[0]
            df.to_excel(fname, index=False)
            self.file_Data.append(fname)
            return fname
        except:
            return " NO_TABLE_FOUND_" + prefix

    def wait(self, xpath, delay=10):
        self.driver.minimize_window()
        elements = self.driver.find_elements_by_xpath(xpath)
        while elements == [] and delay > 0:
            time.sleep(1)
            self.driver.minimize_window()
            delay -= 1
            elements = self.driver.find_elements_by_xpath(xpath)
        if elements == [] and delay == 0:
            return False
        else:
            return True

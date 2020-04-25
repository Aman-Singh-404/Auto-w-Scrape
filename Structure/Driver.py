import os
import re
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.support.ui import Select


class Driver:
    def __init__(self, browser, path, path_list, url_list):
        self.driver = None
        if browser == "Firefox":
            self.driver = webdriver.Firefox(executable_path=path)
        else:
            self.driver = webdriver.Chrome(executable_path=path)
        self.driver.minimize_window()
        self.driver.set_window_position(0,0)
        self.driver.set_window_size(600,600)
        self.pathList = path_list
        self.urlList = url_list
        self.dataMatrix = []
        self.state = []
        self.tab = 1
    
    def converttoXPATH(self, tag):
        self.driver.minimize_window()
        element = BeautifulSoup(tag, "lxml").find('body').findChild()
        xpath = "//" + element.name + "[@"
        if element.attrs == {}:
            return xpath[:-2]
        for key, value in element.attrs.items():
            if type(value) == list:
                xpath += key + "='" + " ".join(value) + "' and @"
            else:
                xpath += key + "='" + value + "' and @"
        return xpath[:-6] + ']'
    
    def evaluateAction(self, node, path):
        self.driver.minimize_window()
        dataList = {}
        if node.attribute[0] == "Click":
            xpath = self.converttoXPATH(node.attribute[1])
            if not self.wait(xpath):
                raise NoSuchElementException("ELEMENT_NOT_FOUND_" + node.text())
            elements = self.driver.find_elements_by_xpath(xpath)

            index = path.index(node)
            pre_path = path[:index]
            post_path = path[index + 1:]

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

    def evaluateData(self, node, prefix):
        self.driver.minimize_window()
        xpath = self.converttoXPATH(node.attribute[1])
        if not self.wait(xpath):
            return ["ELEMENT_NOT_FOUND_" + node.text()]
        element = self.driver.find_element_by_xpath(xpath)
        if node.attribute[0] == "Text":
            return [element.text]
        else:
            src = ""
            if elements[i].get_attribute("src") != None:
                src = elements[i].get_attribute("src")
            elif elements[i].get_attribute("href") != None:
                src = elements[i].get_attribute("href")
            else:
                tag = elements[i].get_attribute('outerHTML')
                sre = re.search("(?P<url>https?://[^\s]+)", tag)
                raw_url = sre.group("url")
                src = raw_url[:raw_url.find(tag[sre.span()[0]-1])]
            req = requests.get(src, stream = True)
            path, base = os.path.split(node.attribute[2])
            base = prefix + "_" + "_" + base
            fname = os.path.join(path, base)
            with open(fname,'wb') as fle:
                fle.write(req.content)
            return [fname]
    
    def evaluateInput(self, node):
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
        self.driver.minimize_window()
        for i in range(len(self.urlList)):
            try:
                dataList = {}
                for path in self.pathList:
                    try:
                        self.state.append(("Same", self.urlList[i]))
                        self.driver.get(self.urlList[i])
                        dataList = self.executePath(path).items()
                        self.dataMatrix.append([self.urlList[i], dataList])
                        self.state.pop()
                    except NoSuchElementException as err:
                        self.dataMatrix.append([self.urlList[i], err.msg])
                        continue
            except WebDriverException:
                self.dataMatrix.append([self.urlList[i], "URL_NOT_FOUND"])
        self.driver.close()
        return self.dataMatrix

    def executePath(self, path):
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
                dataList[node.text()] = self.evaluateData(node, node.text())
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

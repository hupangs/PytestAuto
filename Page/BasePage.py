import time
import os
import config.conf
import win32gui
import win32con
from util.mylog import MyLog
from time import sleep
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait as WD
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    TimeoutException,
    NoAlertPresentException,
)

from util.clipboard import ClipBoard
from util.keyboard import KeyBoard
from util.parseConFile import ParseConFile
from util.parseExcelFile import ParseExcel


class BasePage(object):
    """结合显示等待封装一些selenium内置方法"""
    cf = ParseConFile()
    excel = ParseExcel()

    def __init__(self, driver, timeout=10):
        self.byDic = {
            'id': By.ID,
            'name': By.NAME,
            'class_name': By.CLASS_NAME,
            'xpath': By.XPATH,
            'link_text': By.LINK_TEXT
        }
        self.driver = driver
        self.outTime = timeout
        self.logger = MyLog().get_log()

    # 查找元素
    def find_element(self, by, locator, model=None):
        """
        find alone element
        :param by: eg: id, name, xpath, css.....
        :param locator: id, name, xpath for str
        :return: element object
        """
        try:
            element = WD(self.driver, self.outTime).until(lambda x: x.find_element(by, locator))
        except TimeoutException as t:
            self.logger.exception(f'查找"{model}"元素失败,定位方式:{locator}')
            print('error: found "{}" timeout!'.format(locator), t)
            # 截图
            self.save_webImgs(f"查找元素[{model}]异常")
        else:
            return element

    # 查找元素集
    def find_elements(self, by, locator, model=None):
        """
        find group elements
        :param by: eg: id, name, xpath, css.....
        :param locator: eg: id, name, xpath for str
        :return: elements object
        """
        self.logger.info(f'查找"{model}"元素集，元素定位:{locator}')
        try:
            elements = WD(self.driver, self.outTime).until(lambda x: x.find_elements(by, locator))
        except TimeoutException:
            self.logger.exception(f'查找"{model}"元素集失败,定位方式:{locator}')
            # 截图
            self.save_webImgs(f"查找元素集[{model}]异常")
        else:
            return elements

    # 断言元素是否存在
    def is_element_exist(self, by, locator, model=None):
        """
        assert element if exist
        :param by: eg: id, name, xpath, css.....
        :param locator: eg: id, name, xpath for str
        :return: if element return True else return false
        """
        self.logger.info(f'断言"{model}"元素存在，元素定位:{locator}')
        if by.lower() in self.byDic:
            try:
                WD(self.driver, self.outTime). \
                    until(ec.visibility_of_element_located((self.byDic[by], locator)))
            except TimeoutException:
                self.logger.exception(f'断言"{model}"元素不存在,定位方式:{locator}')
                # 截图
                self.save_webImgs(f"断言元素[{model}]异常")
                return False
            return True
        else:
            print('the "{}" error!'.format(by))

    # 点击操作
    def is_click(self, by, locator, model=None):
        if by.lower() in self.byDic:
            try:
                element = WD(self.driver, self.outTime). \
                    until(ec.element_to_be_clickable((self.byDic[by], locator)))
            except TimeoutException:
                self.logger.exception(f'"{model}"点击失败')
                # 截图
                self.save_webImgs(f"[{model}]点击异常")
            else:
                return element
        else:
            print('the "{}" error!'.format(by))

    # 断言警告
    def is_alert(self):
        """
        assert alert if exsit
        :return: alert obj
        """
        try:
            re = WD(self.driver, self.outTime).until(ec.alert_is_present())
        except (TimeoutException, NoAlertPresentException):
            print("error:no found alert")
        else:
            return re

    #  切换 iframe
    def switch_to_frame(self, by, locator):
        """判断frame是否存在，存在就跳到frame"""
        self.logger.info('iframe 切换操作:')
        if by.lower() in self.byDic:
            try:
                WD(self.driver, self.outTime). \
                    until(ec.frame_to_be_available_and_switch_to_it((self.byDic[by], locator)))
                sleep(0.5)
                self.logger.info('切换成功')
            except TimeoutException:
                self.logger.exception('iframe 切换失败!!!')
                # 截图
                self.save_webImgs(f"iframe切换异常")
        else:
            print('the "{}" error!'.format(by))

    # 返回默认iframe
    def switch_to_default_frame(self):
        """返回默认的frame"""
        self.logger.info('切换到默认页面')
        try:
            self.driver.switch_to.default_content()
            self.logger.info('返回默认frame成功')
        except Exception:
            self.logger.exception('返回默认窗口失败!!!')
            # 截图
            self.save_webImgs("切换失败_没有要切换窗口的信息")
            # print(e)

    # 获取断言的提示信息
    def get_alert_text(self):
        """获取alert的提示信息"""
        alert = self.is_alert()
        if alert:
            return alert.text
        else:
            return None

    # 获取某一个元素的text信息
    def get_element_text(self, by, locator, name=None, model=None):
        """获取某一个元素的text信息"""
        self.logger.info(f'获取"{model}"元素文本内容，元素定位:{locator}')
        try:
            element = self.find_element(by, locator)
            if name:
                return element.get_attribute(name)
            else:
                self.logger.info(f'获取"{model}"元素文本内容为"{element.text}",元素定位:{locator}')
                return element.text
        except AttributeError:
            self.logger.exception(f'获取"{model}"元素文本内容失败,元素定位:{locator}')
            # 截图
            self.save_webImgs(f"获取[{model}]文本内容异常")

    # 获取多个元素的text信息
    def get_elements_text(self, by, locator, model=None):
        """获取多个元素的text信息"""
        try:
            element = self.find_elements(by, locator)
            text_list = []
            for i in element:
                text = i.text
                text_list.append(text)
            return text_list
        except AttributeError:
            self.logger.exception(f'获取多个"{model}"元素文本内容失败,元素定位:{locator}')
            # 截图
            self.save_webImgs(f"获取多个[{model}]文本内容异常")
            return None

    # 加载url
    def load_url(self, url):
        """加载url"""
        self.driver.get(url)

    # 获取页面源码
    def get_source(self):
        """获取页面源码"""
        return self.driver.page_source

    # 写数据
    def send_keys(self, by, locator, value='', model=None):
        """写数据"""
        self.logger.info(f'在"{model}"输入"{value}",元素定位:{locator}')
        try:
            element = self.find_element(by, locator)
            element.send_keys(value)
        except AttributeError:
            self.logger.exception(f'"{model}"输入操作失败!')
            # 截图
            self.save_webImgs(f"[{model}]输入异常")
            # print(e)

    # 清理数据
    def clear(self, by, locator, model=None):
        """清理数据"""
        self.logger.info(f'清除"{model}",元素定位:{locator}')
        try:
            element = self.find_element(by, locator)
            element.clear()
        except AttributeError:
            self.logger.exception(f'"{model}"清除操作失败')
            # 截图
            self.save_webImgs(f"[{model}]清除异常")

    # 点击某个元素
    def click(self, by, locator, model=None):
        """点击某个元素"""
        element = self.is_click(by, locator)
        self.logger.info(f'点击"{model}",元素定位:{locator}')
        if element:
            element.click()
        else:
            self.logger.exception(f'"{model}"点击失败')
            # 截图
            self.save_webImgs(f"[{model}]点击异常")

    # 双击元素
    def double_click(self, by, locator, model=None):
        """点击某个元素两次"""
        element = self.is_click(by, locator)
        xpath = self.find_element(by, locator)
        self.logger.info(f'双击"{model}",元素定位:{locator}')
        if element:
            ActionChains(self.driver).double_click(xpath).perform()
        else:
            self.logger.exception(f'"{model}"双击失败')
            # 截图
            self.save_webImgs(f"[{model}]双击异常")

    @staticmethod
    def sleep(num=0):
        """强制等待"""
        time.sleep(num)

    def ctrl_v(self, value):
        """ctrl + V 粘贴"""
        ClipBoard.set_text(value)
        self.sleep(2)
        KeyBoard.two_keys('ctrl', 'v')

    @staticmethod
    def enter_key():
        """enter 回车键"""
        KeyBoard.one_key('enter')

    def send_emoji(self, by, locator, value=''):
        JS_ADD_TEXT_TO_INPUT = """
          var elm = arguments[0], txt = arguments[1];
          elm.value += txt;
          elm.dispatchEvent(new Event('change'));
          """
        try:
            element = self.find_element(by, locator)
            self.driver.execute_script(JS_ADD_TEXT_TO_INPUT, element, value)
        except AttributeError as e:
            print(e)

    # 等待元素可见
    def wait_element_to_be_located(self, by, locator, model=None):
        """显示等待某个元素出现，且可见"""
        self.logger.info(f'等待"{model}"元素,定位方式:{locator}')
        try:
            return WD(self.driver, self.outTime).until(ec.presence_of_element_located((self.byDic[by], locator)))
        except TimeoutException:
            self.logger.exception(f'等待"{model}"元素失败,定位方式:{locator}')
            # 截图
            self.save_webImgs(f"等待元素[{model}]出现异常")

    def get_page_source(self):
        return self.get_source()

    def save_webImgs(self, model=None):
        # filepath = 指图片保存目录/model(页面功能名称)_当前时间到秒.png
        # 截图保存目录
        # 拼接截图文件夹，如果不存在则自动创建
        cur_path = config.conf.cur_path
        now_date = config.conf.CURRENT_TIME
        screenshots_path = os.path.join(os.path.dirname(cur_path), f'Screenshots\\{now_date}')
        if not os.path.exists(screenshots_path):
            os.makedirs(screenshots_path)
        # 当前时间
        dateNow = time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time()))
        # 路径
        filePath = '{}\\{}_{}.png'.format(screenshots_path, model, dateNow)
        try:
            self.driver.save_screenshot(filePath)
            self.logger.info(f"截屏成功,图片路径为{filePath}")
        except:
            self.logger.exception('截屏失败!')

    @staticmethod
    def upload(filePath, browser_type="chrome"):
        """
        通过pywin32模块实现文件上传的操作
        :param filePath: 文件的绝对路径
        :param browser_type: 浏览器类型（默认值为chrome）
        :return:
        """
        if browser_type.lower() == "chrome":
            title = "打开"
        elif browser_type.lower() == "firefox":
            title = "文件上传"
        elif browser_type.lower() == "ie":
            title = "选择要加载的文件"
        else:
            title = ""  # 这里根据其它不同浏览器类型来修改

        # 找元素
        # 一级窗口"#32770","打开"
        dialog = win32gui.FindWindow("#32770", title)
        # 向下传递
        ComboBoxEx32 = win32gui.FindWindowEx(dialog, 0, "ComboBoxEx32", None)  # 二级
        comboBox = win32gui.FindWindowEx(ComboBoxEx32, 0, "ComboBox", None)  # 三级
        # 编辑按钮
        edit = win32gui.FindWindowEx(comboBox, 0, 'Edit', None)  # 四级
        # 打开按钮
        button = win32gui.FindWindowEx(dialog, 0, 'Button', "打开(&O)")  # 二级
        # 输入文件的绝对路径，点击“打开”按钮
        win32gui.SendMessage(edit, win32con.WM_SETTEXT, None, filePath)  # 发送文件路径
        win32gui.SendMessage(dialog, win32con.WM_COMMAND, 1, button)  # 点击打开按钮


if __name__ == "__main__":
    pass

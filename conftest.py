import allure
import pytest
from selenium import webdriver

driver = None


# 测试失败时添加截图和测试用例描述(用例的注释信息)

@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    """
    当测试失败的时候，自动截图，展示到html报告中
    :param item:
    """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            file_name = report.nodeid.replace("::", "_") + ".png"
            screen_img = _capture_screenshot()
            if file_name:
                html = '<div><img src="data:image/png;base64,%s" alt="screenshot" style="width:600px;height:400px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % screen_img
                extra.append(pytest_html.extras.html(html))
            # 添加allure失败截图
            allure.attach(driver.get_screenshot_as_png(), "失败截图", allure.attachment_type.PNG)

        report.extra = extra
    extra.append(pytest_html.extras.text('some string', name='Different title'))
    report.description = str(item.function.__doc__)
    report.nodeid = report.nodeid.encode("utf-8").decode("unicode_escape")  # 解决乱码

def _capture_screenshot():
    """
    截图保存为base64
    :return:
    """
    return driver.get_screenshot_as_base64()


# 设置为session，全部用例执行一次
@pytest.fixture(scope='session')
def driver():
    global driver
    print('------------open browser------------')
    chromeOptions = webdriver.ChromeOptions()
    # 设定下载文件的保存目录，
    # 如果该目录不存在，将会自动创建
    prefs = {"download.default_directory": "E:\\testDownload"}
    # 将自定义设置添加到Chrome配置对象实例中
    chromeOptions.add_experimental_option("prefs", prefs)
    chromeOptions.add_argument("--ignore-certificate-errors")
    # chromeOptions.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=chromeOptions)
    # driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(10)

    yield driver
    print('------------close browser------------')
    driver.quit()

from Page.BasePage import BasePage
from util.parseConFile import ParseConFile

# 网盘IP地址
Net_disk_ip = ParseConFile().get_locators_or_account('LoginAccount', 'NetDisk_IP')


class LoginPage(BasePage):
    # 配置文件读取元素
    do_conf = ParseConFile()

    # 用户名输入框
    username = do_conf.get_locators_or_account('LoginPageElements', 'username')
    # 密码输入框
    password = do_conf.get_locators_or_account('LoginPageElements', 'password')
    # 登录按钮
    loginBtn = do_conf.get_locators_or_account('LoginPageElements', 'loginBtn')
    # 登录失败的提示信息
    error_Text = do_conf.get_locators_or_account('LoginPageElements', 'errorText')
    # 登录成功后的显示信息
    my_library = do_conf.get_locators_or_account('HomePageElements', 'my_library')

    def login(self, username, password):
        """登录流程"""
        self.logger.info("【===登录操作===】")
        self.open_url()
        self.input_username(username)
        self.input_password(password)
        self.click_login_btn()

    def open_url(self):
        """加载URL"""
        self.logger.info("【===打开URL===】")
        return self.load_url(url=Net_disk_ip)

    def input_username(self, username):
        """输入用户名"""
        self.wait_element_to_be_located(*LoginPage.username, model='用户名编辑框')
        return self.send_keys(*LoginPage.username, username, model='用户名编辑框')

    def input_password(self, password):
        """输入密码"""
        self.wait_element_to_be_located(*LoginPage.password, model='密码编辑框')
        return self.send_keys(*LoginPage.password, password, model='密码编辑框')

    def click_login_btn(self):
        """点击登录按钮"""
        self.wait_element_to_be_located(*LoginPage.loginBtn, model='登录按钮')
        return self.click(*LoginPage.loginBtn, model='登录按钮')

    def get_login_error_text(self):
        """用户登录失败提示信息"""
        self.logger.info("【===获取登录失败报错信息===】")
        return self.get_element_text(*LoginPage.error_Text, model='登录失败的验证信息')

    def get_login_success_text(self):
        """用户登录成功验证信息"""
        self.logger.info("【===获取登录成功验证信息===】")
        return self.get_element_text(*LoginPage.my_library, model="登录成功的验证信息")


if __name__ == "__main__":
    pass

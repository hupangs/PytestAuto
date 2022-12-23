import allure
import pytest
from data.Login.login_data import LoginData


@allure.feature("登录功能")
class TestLogin(object):
    """登录测试"""

    # 测试数据
    login_data = LoginData

    @pytest.mark.Login
    @allure.story("登录成功场景")
    @allure.title("正确的用户名密码")
    @pytest.mark.parametrize("data", login_data.login_success_data)
    def test_login_success(self, open_url, data):
        """登录成功测试"""
        login_page = open_url
        login_page.login(data["username"], data["password"])
        actual = login_page.get_login_success_text()
        assert actual == data["expected"]

    @allure.story("登录失败场景")
    @allure.title("不输入用户名")
    @pytest.mark.parametrize('data', login_data.login_username_none_data)
    def test_login_username_none(self, open_url, data):
        """用户名为空测试"""
        login_page = open_url
        login_page.login(data["username"], data["password"])
        actual = login_page.get_login_error_text()
        assert actual == data["expected"]

    @allure.story("登录失败场景")
    @allure.title("不输入密码")
    @pytest.mark.parametrize('data', login_data.login_passwd_none_data)
    def test_login_pwd_none(self, open_url, data):
        """密码为空测试"""
        login_page = open_url
        login_page.login(data["username"], data["password"])
        actual = login_page.get_login_error_text()
        assert actual == data["expected"]

    @allure.story("登录失败场景")
    @allure.title("用户名和密码都不输入")
    @pytest.mark.parametrize('data', login_data.login_user_pwd_none_data)
    def test_login_none(self, open_url, data):
        """用户名、密码为空测试"""
        login_page = open_url
        login_page.login(data["username"], data["password"])
        actual = login_page.get_login_error_text()
        assert actual == data["expected"]

    @allure.story("登录失败场景")
    @allure.title("用户名正确，密码错误")
    @pytest.mark.parametrize('data', login_data.login_password_fail_data)
    def test_login_password_fail(self, open_url, data):
        """登录密码错误测试"""
        login_page = open_url
        login_page.login(data["username"], data["password"])
        actual = login_page.get_login_error_text()
        assert actual == data["expected"]

    @allure.story("登录失败场景")
    @allure.title("用户名错误，密码正确")
    @pytest.mark.parametrize('data', login_data.login_username_fail_data)
    def test_login_username_fail(self, open_url, data):
        """登录密码错误测试"""
        login_page = open_url
        login_page.login(data["username"], data["password"])
        actual = login_page.get_login_error_text()
        assert actual == data["expected"]

    @allure.story("登录失败场景")
    @allure.title("用户名错误，密码错误")
    @pytest.mark.parametrize('data', login_data.login_fail_data)
    def test_all_fail(self, open_url, data):
        """登录密码错误测试"""
        login_page = open_url
        login_page.login(data["username"], data["password"])
        actual = login_page.get_login_error_text()
        assert actual == data["expected"]


if __name__ == "__main__":
    pytest.main()

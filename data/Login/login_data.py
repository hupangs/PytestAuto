class LoginData(object):
    """用户登录测试数据"""

    #   登录成功

    login_success_data = [
        {
            "case": "用户名正确, 密码正确",
            "username": "13671707573@163.com",
            "password": "admin2003",
            "expected": "我的资料库"
        }
    ]

    #   用户名不输入
    login_username_none_data = [
        {
            "case": "用户名不输入",
            "username": "",
            "password": "admin2003",
            "expected": "邮箱或用户名不能为空"
        }
    ]

    #   密码不输入
    login_passwd_none_data = [
        {
            "case": "用户名正确, 密码不输入",
            "username": "admin",
            "password": "",
            "expected": "密码不能为空"
        }
    ]

    #   用户名、密码都为空
    login_user_pwd_none_data = [
        {
            "case": "用户名为空, 密码为空",
            "username": "",
            "password": "",
            "expected": "邮箱或用户名不能为空"
        }
    ]

    #   用户名正确, 密码错误
    login_password_fail_data = [
        {
            "case": "用户名正确, 密码错误",
            "username": "admin",
            "password": "admin",
            "expected": "你输入的邮箱或密码不正确"
        }
    ]

    #   用户名错误，密码正确
    login_username_fail_data = [
        {
            "case": "用户名错误, 密码正确",
            "username": "qwer123",
            "password": "admin2003",
            "expected": "你输入的邮箱或密码不正确"
        }
    ]

    #   用户名错误、密码错误
    login_fail_data = [
        {
            "case": "用户名错误, 密码错误",
            "username": "admin123",
            "password": "admin",
            "expected": "你输入的邮箱或密码不正确"
        }
    ]


if __name__ == '__main__':
    pass

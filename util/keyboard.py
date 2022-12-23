import win32api
import win32con
import time


class KeyBoard(object):
    """模拟按键"""
    # 键盘码
    vk_code = {
        'enter': 0x0D,
        'tab': 0x09,
        'ctrl': 0x11,
        'v': 0x56,
        'a': 0x41,
        'x': 0x58,
        'c': 67,
        "r": 82,
        'down': 40,
        'esc': 27,
        'del': 46,
        'left': 37,
        'right': 39,
        'Up': 38,
        'space': 32,
        'F5': 116,

    }

    @staticmethod
    def multiple_go_down(num, name):
        # 多次按下同一个键
        t = 1
        while True:
            if t <= num:
                KeyBoard().keydown(name)
                t += 1
                time.sleep(0.5)
            else:
                break

    @staticmethod
    def keydown(key_name):
        """按下键"""
        key_name = key_name.lower()
        try:
            win32api.keybd_event(KeyBoard.vk_code[key_name], 0, 0, 0)
        except Exception as e:
            print('未按下enter键')
            print(e)

    @staticmethod
    def keyup(key_name):
        """抬起键"""
        key_name = key_name.lower()
        win32api.keybd_event(KeyBoard.vk_code[key_name], 0, win32con.KEYEVENTF_KEYUP, 0)

    @staticmethod
    def one_key(key):
        """模拟单个键"""
        key = key.lower()
        KeyBoard.keydown(key)
        time.sleep(0.1)
        KeyBoard.keyup(key)

    @staticmethod
    def two_keys(key1, key2):
        """模拟组合键"""
        key1 = key1.lower()
        key2 = key2.lower()
        KeyBoard.keydown(key1)
        KeyBoard.keydown(key2)
        KeyBoard.keyup(key1)
        KeyBoard.keyup(key2)


if __name__ == '__main__':
    pass

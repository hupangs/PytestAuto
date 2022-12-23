import win32con
import win32clipboard as wc


class ClipBoard(object):
    """设置剪切板内容和获取剪切板内容"""

    @staticmethod
    def get_text():
        """获取剪切板内容"""
        wc.OpenClipboard()
        value = wc.GetClipboardData(win32con.CF_TEXT)
        wc.CloseClipboard()
        return value

    @staticmethod
    def set_text(value):
        """设置剪切板内容"""
        wc.OpenClipboard()
        wc.EmptyClipboard()
        wc.SetClipboardData(win32con.CF_UNICODETEXT, value)
        wc.CloseClipboard()


if __name__ == '__main__':
    pass

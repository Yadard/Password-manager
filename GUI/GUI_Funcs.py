from API import Core
from MainUI import Entry
from PyQt5.QtCore import pyqtSlot, QEvent
from win32clipboard import SetClipboardText, CloseClipboard, OpenClipboard, EmptyClipboard


@pyqtSlot(QEvent)
def authenticating(username: Entry, senha: Entry):
    print(username.text())
    print(senha.text())


def set_clipboard(str_target: str):
    OpenClipboard()
    EmptyClipboard()
    SetClipboardText(str_target)
    CloseClipboard()

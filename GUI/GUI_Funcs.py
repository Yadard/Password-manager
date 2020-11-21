import sys

from PyQt5.QtCore import pyqtSlot, QEvent

from MainUI import Entry

sys.path.insert(1, 'C:\\Dev\\Password-manager\\API')
import Core


@pyqtSlot(QEvent)
def authenticating(username: Entry, senha: Entry):
    print(username.text())
    print(senha.text())

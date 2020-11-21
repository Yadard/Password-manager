from MainUI import Main_UI
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from mouseinfo import _winPosition as mouse_position
from GUI_Funcs import *


class MainApp(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.MainUI = Main_UI()
        self.MainUI.setupUi(self)
        self.MainUI.PF_password_submit.pressed.connect(lambda: authenticating(self.MainUI.PF_username, self.MainUI.PF_password))
        self.show()


class QuickApp(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.Quick_UI = QuickUI(self)
        self.Quick_UI.setupUi(self, mouse_position())
        self.Quick_UI.tray_icon.activated.connect(self.hello)
        self.show()

    @pyqtSlot(QKeyEvent)
    def keyPressEvent(self, e: QKeyEvent) -> None:
        if e.key() == Qt.Key_Escape:
            self.setHidden(True)
        super().keyPressEvent(e)

    @pyqtSlot(QSystemTrayIcon.ActivationReason)
    def hello(self, event):
        print(event)
        if event == self.UI.tray_icon.DoubleClick:
            self.setHidden(False)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = MainApp()
    sys.exit(app.exec_())

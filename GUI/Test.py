from PyQt5 import QtWidgets, QtGui, QtCore


class Entry(QtWidgets.QLineEdit):
    def __init__(self, Frame: QtWidgets.QFrame):
        super(Entry, self).__init__(Frame)
        self.default_text = ''

    @QtCore.pyqtSlot(QtGui.QFocusEvent)
    def focusInEvent(self, a0: QtGui.QFocusEvent) -> None:
        if self.text() == self.default_text:
            self.clear()
            if 'PASSWORD' in self.default_text:
                self.setEchoMode(self.Password)

    @QtCore.pyqtSlot(QtGui.QFocusEvent)
    def focusOutEvent(self, a0: QtGui.QFocusEvent) -> None:
        if self.text() == "":
            self.setText(self.default_text)
            if 'PASSWORD' in self.default_text:
                self.setEchoMode(self.Normal)


def print_value(entry: Entry, entry2: Entry):
    print(entry.text())
    print(entry2.text())

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    root = QtWidgets.QMainWindow()
    root.resize(500,500)
    frame = QtWidgets.QWidget(root)
    frame.resize(500,500)
    entry = Entry(frame)
    entry.setGeometry(QtCore.QRect(0, 0, 100, 50))
    entry.setText('PASSWORD')
    entry.default_text = 'PASSWORD'
    entry2 = Entry(frame)
    entry2.setGeometry(QtCore.QRect(0, 100, 100, 50))
    entry2.setText('USERNAME')
    entry2.default_text = 'USERNAME'
    button = QtWidgets.QPushButton(frame)
    button.setGeometry(QtCore.QRect(0, 200, 50,50))
    button.pressed.connect(lambda: print_value(entry, entry2))
    root.show()

    sys.exit(app.exec_())

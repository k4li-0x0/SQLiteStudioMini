import sys
from PyQt5.QtWidgets import QApplication
from hellownd import HelloWindow
from mainwindow import MainWindow

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.hide()
    hello = HelloWindow(window)
    hello.show()
    sys.exit(app.exec_())

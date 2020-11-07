import sqlite3, os
from PyQt5 import uic, QtGui
from PyQt5.Qt import QFont
from PyQt5.QtWidgets import QWidget, QPushButton, QListWidgetItem

class HelloWindow(QWidget): # Welcome window
    def __init__(self, mainWindow):
        super().__init__()
        uic.loadUi("ui/hell.ui", self)
        self.setWindowIcon(QtGui.QIcon("images/ID_ICON.png"))
        self.mainWindow = mainWindow # Instance of main window to activation
        self.prefs = self.mainWindow.prefs
        self.visualize()
        self.initUi()
    
    def visualize(self):
        if self.prefs[2] == "1":
            self.currentWndFont = QFont(self.prefs[0], int(self.prefs[1]), QFont.Bold)
        else:
            self.currentWndFont = QFont(self.prefs[0], int(self.prefs[1]))
        self.setFont(self.currentWndFont)

    def initUi(self):
        self.open.clicked.connect(self.opens)
        self.create.clicked.connect(self.creates)
        c = sqlite3.connect(os.path.abspath("data/recent.sqlite"))
        cr = c.cursor()
        results = c.execute("SELECT path FROM files ORDER BY id DESC").fetchall()
        c.close()
        for i in results:
            self.createRecentList(i[0])
        self.recent.itemClicked.connect(self.recentOpen)

    def recentOpen(self, item):
        self.mainWindow.currentFileName = item.text()
        self.mainWindow.reopen()
        self.close()

    def createRecentList(self, path):
        self.recent.addItem(QListWidgetItem(path))

    def opens(self):
        self.mainWindow.open()
        self.close()
    
    def creates(self):
        self.mainWindow.new()
        self.close()

    def closeEvent(self, e):
        self.mainWindow.show()


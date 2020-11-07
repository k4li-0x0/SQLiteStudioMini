from PyQt5 import uic, QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.Qt import QKeySequence
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QMessageBox


class PreferenceWidget(QWidget):
    def __init__(self, wnd):
        super().__init__()
        self.createUi()
        self.wnd = wnd
        self.loadPreferences()
        self.setFont(wnd.currentWndFont)
        print(self.font)

    def createUi(self):
        uic.loadUi("ui/prefs.ui", self)
        self.savePrefs.clicked.connect(self.ok)
        self.applyPrefs.clicked.connect(self.apply)
        self.cancel.clicked.connect(self.close)
        self.shorts = {self.clearShort: self.clearKey, self.closeShort: self.closeKey,
                self.createShort: self.createKey, self.exeShort: self.exeKey, 
                self.openShort: self.openKey, self.reopenShort: self.reopenKey,
                self.saveShort: self.saveKey}
        for i in self.shorts.keys():
            i.stateChanged.connect(self.sstateChanged)
    
    def ok(self):
        self.savePreferences()
        self.showMsg()
        self.close()
    
    def apply(self):
        self.savePreferences()
        self.showMsg()
    
    def sstateChanged(self, state):
        snd = self.sender()
        checked = bool([0, Qt.Checked].index(state))
        self.shorts[snd].setEnabled(checked)

    def showMsg(self):
        msg = QMessageBox()
        msg.setWindowTitle("SQLiteStudioMini")
        msg.setText("OK. You must to restart the application to apply shortcut preferences")
        msg = msg.exec()

    def loadPreferences(self):
        with open("data/prefs.txt") as f:
            data = f.read()
            f.close()
        data = data.split("\n")
        self.font.setCurrentFont(QFont(data[0]))
        self.fontSize.setValue(int(data[1]))
        self.isBoldBox.setChecked(bool(int(data[2])))
        self.color.setCurrentIndex(int(data[3]))
        for i in range(4, 18, 2):
            a = list(self.shorts.keys())[(i - 4) // 2]
            a.setChecked(bool(int(data[i])))
            self.shorts[a].setKeySequence(QKeySequence(data[i + 1]))
            
    
    def savePreferences(self):
        font = self.font.currentFont().family()
        size = str(self.fontSize.value())
        isBold = str(int(self.isBoldBox.isChecked()))
        color = str(self.color.currentIndex())
        shortcuts = list()
        for i in self.shorts.keys():
            shortcuts.append(str(int(i.isChecked())))
            shortcuts.append(self.shorts[i].keySequence().toString())
        data = font + "\n" + size + "\n" + isBold + "\n" + color + "\n" \
            + "\n".join(shortcuts)
        with open("data/prefs.txt", "w") as f:
            f.write(data)
            f.close()

    def closeEvent(self, e):
        self.wnd.show()
        self.wnd.loadPrefs()
        self.wnd.visualize()
        e.accept()

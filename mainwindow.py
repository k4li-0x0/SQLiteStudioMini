import sys, webbrowser, os, sqlite3
from PyQt5 import uic, QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QPalette, QColor
from PyQt5.Qt import QKeySequence,  QSyntaxHighlighter, QRegularExpression, QTextCharFormat, QFont, QTextCursor, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QShortcut, QCompleter, QMessageBox, QFileDialog, QTableWidgetItem, QTableWidget, QListWidgetItem
from hellownd import HelloWindow
from SQLHighlighter import SQLHighlighter
from preferences import PreferenceWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__() # Initialize superclass
        uic.loadUi("ui/root.ui", self) # Load UI
        self.loadPrefs()
        self.setWindowIcon(QtGui.QIcon("images/ID_ICON.png")) # Setting up icon
        self.connections() # Connect signals
        self.setVariables() # Setup variables values
        
    def setVariables(self):
        self.currentFileName = "" # Current file name
        self.fileExtension = "Database (*.db *.sqlite)" # Database file extension 

    def loadPrefs(self):
        with open("data/prefs.txt") as f:
            data = f.read()
            f.close()
        self.prefs = data.split("\n")
        self.visualize()
        self.colorize()
        print(self.prefs)
    
    def colorize(self):
        if self.prefs[3] == "1":
            app = QApplication.instance()
            palette = QPalette()
            palette.setColor(QPalette.Window, QColor(53, 53, 53))
            palette.setColor(QPalette.WindowText, Qt.white)
            palette.setColor(QPalette.Base, QColor(25, 25, 25))
            palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
            palette.setColor(QPalette.ToolTipBase, Qt.black)
            palette.setColor(QPalette.ToolTipText, Qt.white)
            palette.setColor(QPalette.Text, Qt.white)
            palette.setColor(QPalette.Button, QColor(53, 53, 53))
            palette.setColor(QPalette.ButtonText, Qt.white)
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Link, QColor(42, 130, 218))
            palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
            palette.setColor(QPalette.HighlightedText, Qt.black)
            app.setPalette(palette)
        else:
            app = QApplication.instance()
            palette = QPalette()
            palette.setColor(QPalette.Window, QColor(245, 245, 245))
            palette.setColor(QPalette.WindowText, Qt.black)
            palette.setColor(QPalette.Base, QColor(240, 240, 240))
            palette.setColor(QPalette.AlternateBase, QColor(245, 245, 245))
            palette.setColor(QPalette.ToolTipBase, Qt.white)
            palette.setColor(QPalette.ToolTipText, Qt.black)
            palette.setColor(QPalette.Text, Qt.black)
            palette.setColor(QPalette.Button, QColor(245, 245, 245))
            palette.setColor(QPalette.ButtonText, Qt.black)
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Link, QColor(0, 0, 255))
            palette.setColor(QPalette.Highlight, QColor(200, 200, 250))
            palette.setColor(QPalette.HighlightedText, Qt.white)
            app.setPalette(palette)

    def visualize(self):
        if self.prefs[2] == "1":
            self.currentWndFont = QFont(self.prefs[0], int(self.prefs[1]), QFont.Bold)
        else:
            self.currentWndFont = QFont(self.prefs[0], int(self.prefs[1]))
        self.setFont(self.currentWndFont)

    def connections(self):
        self.newAction.triggered.connect(self.new) # File Actions -> New database
        self.openAction.triggered.connect(self.open) # File Actions -> Open database
        self.reopenAction.triggered.connect(self.reopen) # File Actions -> Reopen database
        self.saveAction.triggered.connect(self.save) # File Actions -> Save database
        self.exitAction.triggered.connect(self.exit) # File Actions -> Exit Studio
        self.prefAction.triggered.connect(self.pref) # File Actions -> Preferences
        self.aboutAction.triggered.connect(self.about) # Help Actions -> About Studio
        self.howToAction.triggered.connect(self.howTo) # Help Actions -> How to use Studio
        self.sqlitedocAction.triggered.connect(self.sqliteDocs) # Help Actions -> open SQLite Docs
        self.SELECT.triggered.connect(self.cqSelection) # Action Actions -> Create SELECT query
        self.UPDATE.triggered.connect(self.cqUpdate) # Action Actions -> Create UPDATE query
        self.DELETE.triggered.connect(self.cqDelete) # Action Actions -> Create DELETE query
        self.DROP.triggered.connect(self.dropDb) # Action Actions -> Create DROP query
        self.clearBtn.clicked.connect(self.clear) # Button Actions -> Clear query
        self.executeBtn.clicked.connect(self.execute) # Button Actions -> Execute query
        self.connect.clicked.connect(self.connection)
        self.bindKeys()
        self.highlighter = SQLHighlighter(self.queryEdit.document()) # Syntax highlighter

    def bindKeys(self):
        if self.prefs[10] == "1":
            self.execShortcut = QShortcut(QKeySequence(self.prefs[11]), self) # Execute shortcut
            self.execShortcut.activated.connect(self.execute)
        if self.prefs[4] == "1":
            self.clearShortcut = QShortcut(QKeySequence(self.prefs[5]), self) # Clear shortcut
            self.clearShortcut.activated.connect(self.clear)
        if self.prefs[8] == "1":
            self.newShortcut = QShortcut(QKeySequence(self.prefs[9]), self) # Create new file shortcut
            self.newShortcut.activated.connect(self.new)
        if self.prefs[12] == "1":
            self.openShortcut = QShortcut(QKeySequence(self.prefs[13]), self) # Open file shortcut
            self.openShortcut.activated.connect(self.open)
        if self.prefs[6] == "1":
            self.closeShortcut = QShortcut(QKeySequence(self.prefs[7]), self) # Close shortcut
            self.closeShortcut.activated.connect(self.exit)
        if self.prefs[14] == "1":
            self.reopenShortcut = QShortcut(QKeySequence(self.prefs[15]), self) # Reopen shortcut
            self.reopenShortcut.activated.connect(self.reopen)
        if self.prefs[16] == "1":
            self.saveShortcut = QShortcut(QKeySequence(self.prefs[17]), self) # Save shortcut
            self.saveShortcut.activated.connect(self.save)

    def connection(self):
        self.con = sqlite3.connect(self.currentFileName)
        self.cur = self.con.cursor()

    def pref(self):
        self.hide()
        self.prefs = PreferenceWidget(self)
        self.prefs.show()

    def open(self): # Open database
        self.currentFileName = QFileDialog.getOpenFileName(self, "Open database", "", self.fileExtension)[0]
        self.connection()

    def new(self): # Create database
        name = QFileDialog.getSaveFileName(self, "Create file", "untitled", self.fileExtension)[0]
        with open(name,'w') as f:
            f.write('')
            f.close()
        self.currentFileName = name
        self.connection()
    
    def reopen(self): # Reopen database
        if os.path.exists(self.currentFileName):
            self.connection()
    
    def save(self): # Save database
        if os.path.exists(self.currentFileName):
            self.con.commit()
    
    def exit(self): # Exit application
        self.con.commit()
        self.close()
    
    def cqSelection(self): # Create SELECT query
        if self.queryEdit.toPlainText() == "":
            self.queryEdit.setText("SELECT * FROM tablename WHERE condition")
        else:
            self.queryEdit.moveCursor(QTextCursor.End)
            self.queryEdit.insertPlainText(";\nSELECT * FROM tablename WHERE condition")
    
    def cqUpdate(self): # Crete UPDATE query
        if self.queryEdit.toPlainText() == "":
            self.queryEdit.setText("UPDATE tablename SET values WHERE condition")
        else:
            self.queryEdit.moveCursor(QTextCursor.End)
            self.queryEdit.insertPlainText(";\nUPDATE tablename SET values WHERE condition")
    
    def cqDelete(self): # Create DELETE query
        if self.queryEdit.toPlainText() == "":
            self.queryEdit.setText("DELETE FROM tablename WHERE condition")
        else:
            self.queryEdit.moveCursor(QTextCursor.End)
            self.queryEdit.insertPlainText(";\nDELETE FROM tablename WHERE condition")
    
    def dropDb(self): # DROP database
        msg = QMessageBox()
        msg.setText("Are you sure you want to drop the table?")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg = msg.exec()
        if msg == QMessageBox.Ok:
            if self.queryEdit.toPlainText() == "":
                self.queryEdit.setText("DROP TABLE tablename")
            else:
                self.queryEdit.moveCursor(QTextCursor.End)
                self.queryEdit.insertPlainText(";\nDROP TABLE tablename")
    
    def about(self): # About application
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("About")
        msg.setText("SQLiteStudioMini v0.1")
        msg.setDetailedText(f"System info: \n{sys.version};\n\nPyQt version: \n{QtCore.QT_VERSION_STR}")
        msg.exec()
    
    def howTo(self): # Help
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Help")
        msg.setText("SQLiteStudioMini v0.1")
        with open("data/help.txt") as f:
            help = f.read()
            f.close()
        msg.setDetailedText(help)
        msg.exec()
    
    def sqliteDocs(self): # Docs
        webbrowser.open("file:\\\\" + os.path.abspath("sqlitedoc/index.html"))
    
    def clear(self): # Clear queryEdit
        self.queryEdit.setText("")
        self.input.setText("")
    
    def execute(self): # Execute query
        try:
            inputs = self.input.toPlainText()
            if self.inputBox.isChecked():
                self.lastResult = self.cur.execute(self.queryEdit.toPlainText(), tuple(inputs.split("\n"))).fetchall()
            else:
                self.lastResult = self.cur.execute(self.queryEdit.toPlainText()).fetchall()
            self.updateTable()
            self.statusBar().showMessage("Success")
        except Exception as e:
            self.statusBar().showMessage("Error: " + str(e))
    
    def updateTable(self):
        columns = max(map(len, self.lastResult))
        self.tableResult.setColumnCount(columns)
        self.tableResult.setRowCount(len(self.lastResult))
        for row in range(len(self.lastResult)):
            for column in range(len(self.lastResult[row])):
                self.tableResult.setItem(row, column, QTableWidgetItem(str(self.lastResult[row][column])))
        self.con.commit()

    def recents(self):
        if os.path.exists(self.currentFileName):
            c = sqlite3.connect(os.path.abspath("data/recent.sqlite"))
            cr = c.cursor()
            c.execute("""INSERT INTO files (
                        path
                    )
                    VALUES (
                        ?
                    )""", (self.currentFileName, ))
            c.commit()
            c.close()

    def closeEvent(self, e):
        msg = QMessageBox()
        msg.setWindowTitle("Close SQLiteStudioMini")
        msg.setText("Are you sure?")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg = msg.exec()
        if msg == QMessageBox.Ok:
            self.con.close()
            self.recents()
            e.accept()
        else:
            e.ignore()

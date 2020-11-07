from PyQt5.Qt import QSyntaxHighlighter, QRegularExpression, QTextCharFormat, QFont, Qt

class SQLHighlighter(QSyntaxHighlighter):
    def highlightBlock(self, block):
        self.str_format = QTextCharFormat() # String format
        self.str_format.setForeground(Qt.green)
        self.int_format = QTextCharFormat() # Int format
        self.int_format.setForeground(Qt.red)
        self.sql_format = QTextCharFormat() # SQL text format
        self.sql_format.setFontWeight(QFont.Bold)
        self.sql_format.setForeground(Qt.blue)
        self.highlightInt(block) # Highlight
        self.highlightStr(block)
        self.highlightSQL(block)
    
    def highlightStr(self, word):
        expression = QRegularExpression(r"(?:(\"|'))([^(\"|')]*)(?:(\"|'))") # String search expression
        it = expression.globalMatch(word)
        while it.hasNext():
            match = it.next()
            self.setFormat(match.capturedStart(), match.capturedLength(), self.str_format)
    
    def highlightInt(self, word):
        expression = QRegularExpression(r"\s*(\d*\.?\d*)") # Integer search expression
        it = expression.globalMatch(word)
        while it.hasNext():
            match = it.next()
            self.setFormat(match.capturedStart(), match.capturedLength(), self.int_format)
    
    def highlightSQL(self, word):
        expression = QRegularExpression(r"\b(?i:(SELECT|UPDATE|DELETE|JOIN|FROM|WHERE|AND|LIKE|ORDER|BY|BETWEEN|DISTINCT|SET|ALTER|TABLE|ORDER BY|OR|NOT|DROP))\b") # SQL keywords search expression
        it = expression.globalMatch(word)
        while it.hasNext():
            match = it.next()
            self.setFormat(match.capturedStart(), match.capturedLength(), self.sql_format)

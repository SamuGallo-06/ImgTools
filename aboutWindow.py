from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QWidget

class AboutWindow(QWidget):
    
    def __init__(self):
        super().__init__()
        loadUi("ui/about.ui", self)
        self.closeButton.clicked.connect(self.close)
from PyQt5.QtWidgets import (
QWidget, QPushButton, QLabel, QFileDialog, QLineEdit,
QMessageBox)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

import os
from PyQt5.uic import loadUi
from bgremove import *

class BackgroundRemoverWindow(QWidget):
    
    def __init__(self, originalImagePath=""):
        super().__init__()
        loadUi("ui/bgremover.ui", self)
        #constants
        self.HOME = os.path.expanduser("~")
        self.FILE_DIALOG_OPTIONS = "All Files(*);;PNG Files(*.png);;JPEG Files(*.jpg)"
        #variables
        self.inputImagePath = originalImagePath
        #setup ui
        self.SetupUi()
        
    def SetupUi(self):
        self.browseButton.clicked.connect(self.UpdateOutputPath)
        self.browseImageButton.clicked.connect(self.BrowseInputImage)
        self.updatePreviewButton.clicked.connect(self.UpdatePreview)
        self.saveButton.clicked.connect(self.SaveImage)
        
        
    def UpdateOutputPath(self):
        self.outputPath = QFileDialog.getSaveFileName(self, "Select output file path", self.HOME, self.FILE_DIALOG_OPTIONS, "All Files(*)")[0]
        self.outputFilePathInput.setText(self.outputPath)
    
    def BrowseInputImage(self):
        self.inputImagePath = QFileDialog.getOpenFileName(self, "Select output file path", self.HOME, self.FILE_DIALOG_OPTIONS, "All Files(*)")[0]
        self.UpdateOriginal()
        
    def UpdateOriginal(self):
        pixmap = QPixmap(self.inputImagePath)
        pixmap = pixmap.scaled(self.originalImgViewer.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.originalImgViewer.setPixmap(pixmap) 
        
    def UpdatePreview(self):
        RemoveBgFromImage(self.inputImagePath, "temp.png")
        pixmap = QPixmap("temp.png")
        pixmap = pixmap.scaled(self.newImgViewer.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.newImgViewer.setPixmap(pixmap)
        
    def SaveImage(self):
        RemoveBgFromImage(self.inputImagePath, self.outputFilePathInput.text())
        os.remove("temp.png")
        self.close()
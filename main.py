from PyQt5.QtWidgets import (
QMainWindow, QPushButton, QLabel, QFileDialog, QComboBox, 
QApplication, QLineEdit, QStatusBar, QCheckBox, QSpinBox,
QMessageBox, QDoubleSpinBox, QAction)
from PyQt5.QtCore import QTranslator
from PyQt5.QtGui import QPixmap, QTransform
import os, sys
from PIL import Image
from PyQt5.uic import loadUi
import configparser

from converters import *
from progressWindow import ProgressWindow
from preferencesWindow import PreferencesWindow
from aboutWindow import *


class ImgTools(QMainWindow):
    
    def __init__(self):
        super(ImgTools, self).__init__()
        loadUi("ui/converter.ui", self)
        self.HOME = os.path.expanduser("~")
        self.imagesList = []
        self.isFolderLoaded = False
        self.config = configparser.ConfigParser()
        self.config.read("configuration.ini")
        self.customOutputPath = self.config.get("ImgTools", "custom-output-path")
        self.SetupUi()
        self.show()
        
    def SetupUi(self):
        #Buttons
        #image loading
        self.loadImageButton = self.findChild(QPushButton, "loadImageButton")
        self.loadImageButton.clicked.connect(self.LoadImage)
        self.loadSaveFilePathButton = self.findChild(QPushButton, "browseOutputPathButton")
        self.loadSaveFilePathButton.clicked.connect(self.OpenSaveFilePathDialog)
        self.convertButton = self.findChild(QPushButton, "convertButton")
        self.convertButton.clicked.connect(self.StartConversion)
        #Size
        self.resetSizeButton = self.findChild(QPushButton, "resetSizeButton")
        self.resetSizeButton.clicked.connect(self.ResetSizeSpinBoxes)
        #Rotation
        self.rotate90degButton = self.findChild(QPushButton, "rotate90degButton")
        self.rotate90degButton.clicked.connect(self.RotateImage90Deg)
        self.rotate90NegDegButton = self.findChild(QPushButton, "rotate90NegDegButton")
        self.rotate90NegDegButton.clicked.connect(self.RotateImage90DegNeg)
        self.rotate180degButton = self.findChild(QPushButton, "rotate180degButton")
        self.rotate180degButton.clicked.connect(self.RotateImage180Deg)
        self.resetRotationButton = self.findChild(QPushButton, "resetRotationButton")
        self.resetRotationButton.clicked.connect(self.ResetRotation)
        
        #Labels
        self.imgViewerLabel = self.findChild(QLabel, "imgViewerLabel")
        #label pixmap with program logo
        self.imgViewerLabel.setPixmap(QPixmap("resources/logo.png"))
        self.imgPathLabel = self.findChild(QLabel, "imgPathLabel")
        
        #Combo boxes
        self.outputFormatComboBox = self.findChild(QComboBox, "outputFormatComboBox")
        self.outputFormatComboBox.currentIndexChanged.connect(self.UpdateOutputPath)
        self.imagesComboBox = self.findChild(QComboBox, "imagesComboBox")
        self.imagesComboBox.currentIndexChanged.connect(self.ChangeImage)
        
        #Line Edit
        self.outputFilePathInput = self.findChild(QLineEdit, "outputFilePathInput")
        self.useCustomOutputPath = self.config.get("ImgTools", "use-custom-output-path")
        if(self.useCustomOutputPath == "True"):
            self.outputFilePathInput.setText(self.customOutputPath)
            
        #Statusbar
        self.statusbar = self.findChild(QStatusBar, "statusbar")
        self.statusbar.showMessage("Ready!")
        
        #Spin boxes
        self.sizeXSpinBox = self.findChild(QSpinBox, "sizeXSpinBox")
        self.sizeYSpinBox = self.findChild(QSpinBox, "sizeYSpinBox")
        self.imageRotationSpinBox = self.findChild(QDoubleSpinBox, "imageRotationSpinBox")
        self.imageRotationSpinBox.valueChanged.connect(self.RotateImage)
        self.resizeCheckBox = self.findChild(QCheckBox, "resizeCheckBox")
        
        #QActions
        self.actionOpen = self.findChild(QAction, "actionOpen")
        self.actionOpen.triggered.connect(self.LoadImage)
        self.actionOpenFolder = self.findChild(QAction, "actionOpenFolder")
        self.actionOpenFolder.triggered.connect(self.LoadImageFolder)
        self.actionQuit = self.findChild(QAction, "actionQuit")
        self.actionQuit.triggered.connect(self.Quit)
        self.actionPreferences.triggered.connect(self.OpenPreferences)
        self.actionInfo.triggered.connect(self.ShowAboutWindow)
        
    def UpdateOutputPath(self):
        if(not self.useCustomOutputPath):
            self.outputFilePathInput.setText(os.path.splitext(self.loadedImageFileName)[0] + "." + self.outputFormatComboBox.currentText().lower())
        else:
            self.outputFilePathInput.setText(self.customOutputPath + "/" + os.path.basename(os.path.splitext(self.loadedImageFileName)[0]) + "." + self.outputFormatComboBox.currentText().lower())
        
    def ResetSizeSpinBoxes(self):
        self.sizeXSpinBox.setValue(self.originalSize[0])
        self.sizeYSpinBox.setValue(self.originalSize[1])
        
    def LoadImage(self):
        self.isFolderLoaded = False
        self.imagesList.clear()
        self.imagesComboBox.clear()
        self.loadedImageFileName = QFileDialog.getOpenFileName(self, "Select an image to convert", self.HOME, "All Files(*);;PNG Files(*.png);;JPEG Files(*.jpg)", "All Files(*)")[0]
        if(self.loadedImageFileName != ""):
            self.pixmap = QPixmap(self.loadedImageFileName)
            self.imgViewerLabel.setPixmap(self.pixmap)
            self.imgPathLabel.setText(self.loadedImageFileName)
            self.loadedImage = Image.open(self.loadedImageFileName, mode="r")
            self.originalSize = self.loadedImage.size
            self.sizeXSpinBox.setValue(self.originalSize[0])
            self.sizeYSpinBox.setValue(self.originalSize[1])
            self.currentRotation = 0
            self.UpdateOutputPath()
            self.statusbar.showMessage("Image loaded: " + self.loadedImageFileName)
        
    def ChangeImage(self):
        self.loadedImageFileName = self.imagesComboBox.currentText()
        self.pixmap = QPixmap(self.loadedImageFileName)
        self.imgViewerLabel.setPixmap(self.pixmap)
        self.imgPathLabel.setText(self.loadedImageFileName)
        self.loadedImage = Image.open(self.loadedImageFileName, mode="r")
        self.originalSize = self.loadedImage.size
        self.sizeXSpinBox.setValue(self.originalSize[0])
        self.sizeYSpinBox.setValue(self.originalSize[1])
        self.currentRotation = 0
        
    def LoadImageFolder(self):
        self.isFolderLoaded = True
        self.imagesList = []
        self.imagesList.clear()
        count = 0
        sourceDir = QFileDialog.getExistingDirectory(self, "Select source folder", self.HOME, QFileDialog.ShowDirsOnly)
        print("[INFO]: searching files in " + sourceDir)
        for filename in os.listdir(sourceDir):
            print(sourceDir + "/" + filename)
            ext = os.path.splitext(filename)[1]
            if(ext == ".png" or ext == ".jpeg" or ext==".gif" or ext ==".webp" or ext==".ico" or ext==".jfif" or ext == ".bmp" or ext==".svg" or ext==".jpg"):
                self.imagesList.append(sourceDir + "/" + filename)
                count += 1
        self.imagesComboBox.addItems(self.imagesList)
        
        self.outputFilePathInput.setText               
                
        print("Found " + str(count) + " valid files")
        
    def OpenSaveFilePathDialog(self):
        if(self.isFolderLoaded):
            outputPath = QFileDialog.getExistingDirectory(self, "Select output folder", self.HOME, QFileDialog.ShowDirsOnly)
            self.outputFilePathInput.setText(outputPath)
        else:
            outputPath = QFileDialog.getSaveFileName(self, "Select output file path", self.HOME, "All Files(*);;PNG Files(*.png);;JPEG Files(*.jpg)", "All Files(*)")[0]
            self.outputFilePathInput.setText(outputPath)
        
    def RotateImage90Deg(self):
        self.pixmap = self.pixmap.transformed(QTransform().rotate(90))
        self.imgViewerLabel.setPixmap(self.pixmap)
        self.currentRotation += 90.0
        self.imageRotationSpinBox.setValue(self.currentRotation)
    
    def RotateImage90DegNeg(self):
        self.pixmap = self.pixmap.transformed(QTransform().rotate(-90))
        self.imgViewerLabel.setPixmap(self.pixmap)
        self.currentRotation -= 90.0
        self.imageRotationSpinBox.setValue(self.currentRotation)
    
    def RotateImage180Deg(self):
        self.currentRotation += 180.0
        self.pixmap = self.pixmap.transformed(QTransform().rotate(180))
        self.imgViewerLabel.setPixmap(self.pixmap)
        self.imageRotationSpinBox.setValue(self.currentRotation)
    
    def RotateImage(self):
        self.currentRotation = self.imageRotationSpinBox.value()
        self.pixmap = self.pixmap.transformed(QTransform().rotate(self.currentRotation))
        self.imgViewerLabel.setPixmap(self.pixmap)
        self.imageRotationSpinBox.setValue(self.currentRotation)
        
    def ResetRotation(self):
        self.pixmap = QPixmap(self.loadedImageFileName)
        self.imgViewerLabel.setPixmap(self.pixmap)
        self.currentRotation = 0
        self.imageRotationSpinBox.setValue(0.0)
    
    def StartConversion(self):
        
        self.statusbar.showMessage("Initializing...")
        
        self.reisizeImage = self.resizeCheckBox.isChecked()
        self.outputFilePath = self.outputFilePathInput.text()  
        self.sizeX = self.sizeXSpinBox.value()
        self.sizeY = self.sizeYSpinBox.value()
        outputFormat = self.outputFormatComboBox.currentText()
        
        if(self.isFolderLoaded): 
            self.progressWindow = ProgressWindow(self.imagesList, self.outputFilePath, outputFormat, self.reisizeImage, self.sizeX, self.sizeY)
            self.progressWindow.show()
            self.statusbar.showMessage("Done")
        else:        
            self.statusbar.showMessage("Converting image...")
            
            if(outputFormat == "ICO"):
                result = ConvertToIco(self.loadedImageFileName, self.outputFilePath, self.reisizeImage, self.sizeX, self.sizeY, self.currentRotation)
            elif(outputFormat == "JPEG"):
                result = ConvertToJpeg(self.loadedImageFileName, self.outputFilePath, self.reisizeImage, self.sizeX, self.sizeY, self.currentRotation)
            elif(outputFormat == "PNG"):
                result = ConvertToPng(self.loadedImageFileName, self.outputFilePath, self.reisizeImage, self.sizeX, self.sizeY, self.currentRotation)
            elif(outputFormat == "BMP"):
                result = ConvertToBmp(self.loadedImageFileName, self.outputFilePath, self.reisizeImage, self.sizeX, self.sizeY, self.currentRotation)
            elif(outputFormat == "WEBP"):
                result = ConvertToWebp(self.loadedImageFileName, self.outputFilePath, self.reisizeImage, self.sizeX, self.sizeY, self.currentRotation)
            elif(outputFormat == "SVG"):
                result = ConvertToSvg(self.loadedImageFileName, self.outputFilePath, self.reisizeImage, self.sizeX, self.sizeY, self.currentRotation)
                
            if(result == "ERR_FILE_NOT_FOUND"):
                self.ShowErrorMessage("Cannot open file: no such file ore directory")
                self.statusbar.showMessage("Cannot open file: no such file ore directory")
            elif(result == "ERR_OUTPUT_NOT_GIVEN"):
                self.ShowErrorMessage("No output file was given")
                self.statusbar.showMessage("No output file was given")
            elif(result == "ERR_INPUT_NOT_GIVEN"):
                self.ShowErrorMessage("No Input file was given")
                self.statusbar.showMessage("No Input file was given")
            else:
                self.statusbar.showMessage("Done")
                
    def OpenPreferences(self):
        self.preferencesWindow = PreferencesWindow()
        self.preferencesWindow.show()
        
    def ShowAboutWindow(self):
        self.aboutWindow = AboutWindow()
        self.aboutWindow.show()
                
            
    def ShowErrorMessage(self, info):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("ImgTools: Error")
        msg.setText("Error")
        msg.setInformativeText(info)
        msg.exec_()
        
    def Quit(self):
        self.imagesList.clear()
        exit(0)
        
if __name__ == "__main__":
    #Inizializzazione
    app = QApplication(sys.argv)
    # File di traduzione
    translator = QTranslator()
    if(not os.path.exists("configuration.ini")):
        file = open("configuration.ini", "w")
        file.write("[ImgTools]\nlanguage = English\nuse-custom-output-path = False\ncustom-output-path =")
        file.close()
    config = configparser.ConfigParser()
    config.read("configuration.ini")
    if(config.get("ImgTools", "language") == "Italiano"):
        translator.load("translations/it.qm")
        app.installTranslator(translator)
    #elif(config.get("ImgTools", "language") == "Español"):
    #    translator.load("translations/es.qm")
    #    app.installTranslator(translator)
    #elif(config.get("ImgTools", "language") == "Français"):
    #    translator.load("translations/fr.qm")
    #    app.installTranslator(translator)
    
    #Esecuzione Applicazione
    window = ImgTools()
    app.exec_()

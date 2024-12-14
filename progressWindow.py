from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QMessageBox
import os
from converters import *
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QProgressBar, QDialogButtonBox
from PyQt5.uic import loadUi
import time

class ConversionThread(QThread):
    
    def __init__(self, statusLabel, progressBar, imagesList, outputPath, outputFormat, resizeImage, sizeX, sizeY):
        
        super().__init__()
        
        self.statusLabel = statusLabel
        self.progressBar = progressBar
        self.imagesList = imagesList
        self.outputPath = outputPath
        self.outputFormat = outputFormat
        self.resizeImage = resizeImage
        self.sizeX = sizeX
        self.sizeY = sizeY
        
    
    def run(self):
        
        totalImages = len(self.imagesList)
        convertedImages =0
        
        for file in self.imagesList:
                
            fileBaseName = os.path.splitext(os.path.basename(file))[0]
            outputFilePath = self.outputPath + "/" + fileBaseName + "." + self.outputFormat.lower()
            self.statusLabel.setText("Converting " + file + "...")
                
            if(self.outputFormat == "ICO"):
                result = ConvertToIco(file, outputFilePath, self.resizeImage, self.sizeX, self.sizeY)
            elif(self.outputFormat == "JPEG"):
                result = ConvertToJpeg(file, outputFilePath, self.resizeImage, self.sizeX, self.sizeY)
            elif(self.outputFormat == "PNG"):
                result = ConvertToPng(file, outputFilePath, self.resizeImage, self.sizeX, self.sizeY)
            elif(self.outputFormat == "BMP"):
                result = ConvertToBmp(file, outputFilePath, self.resizeImage, self.sizeX, self.sizeY)
            elif(self.outputFormat == "WEBP"):
                result = ConvertToWebp(file, outputFilePath, self.resizeImage, self.sizeX, self.sizeY)
            elif(self.outputFormat == "SVG"):
                result = ConvertToSvg(file, outputFilePath, self.resizeImage, self.sizeX, self.sizeY)
                
            if(result == "ERR_FILE_NOT_FOUND"):
                self.ShowErrorMessage("Cannot open file: no such file ore directory")
                break
            elif(result == "ERR_OUTPUT_NOT_GIVEN"):
                self.ShowErrorMessage("No output file was given")
                break
            elif(result == "ERR_INPUT_NOT_GIVEN"):
                self.ShowErrorMessage("No Input file was given")
                break
            
            convertedImages += 1
            
            self.progressBar.setValue(int((convertedImages / totalImages) * 100))
            
        return
        
    def ShowErrorMessage(self, info):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("ImgTools: Error")
        msg.setText("Error")
        msg.setInformativeText(info)
        msg.exec_()
        
        
class ProgressWindow(QWidget):
    
    def __init__(self, imagesList, outputPath, outputFormat, resizeImage, sizeX, sizeY):
        super().__init__()
        loadUi("ui/progress.ui", self)
        
        self.progressLabel = self.findChild(QLabel, "progressLabel")
        self.progressBar = self.findChild(QProgressBar, "progressBar")
        self.abortButton = self.findChild(QPushButton, "abortButton")
        self.abortButton.clicked.connect(self.Abort)
        
        self.progressBar.setValue(0)

        self.worker = ConversionThread(self.progressLabel, self.progressBar, imagesList, outputPath, outputFormat, resizeImage, sizeX, sizeY)
        self.worker.finished.connect(self.OnOperationComplete)
        self.worker.start()

    def OnOperationComplete(self):
        self.worker.quit()
        time.sleep(1.5)
        self.close()
        
    def Abort(self):
        self.worker.quit()
        self.close()
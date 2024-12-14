from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QWidget, QMessageBox
import configparser

class PreferencesWindow(QWidget):
    
    def __init__(self):
        super().__init__()
        self.config = configparser.ConfigParser()
        self.config.read("configuration.ini")
        loadUi("ui/preferences.ui", self)
        self.closeButton.clicked.connect(self.close)
        
        #Language
        self.currentLanguage = self.config.get("ImgTools", "language")
        print(self.currentLanguage)
        self.languagesComboBox.setCurrentText(self.currentLanguage)
        self.languagesComboBox.currentIndexChanged.connect(self.ChangeLanguage)
        
        #CustomOutput
        if(self.config.get("ImgTools", "use-custom-output-path") == "True"):
            self.useCustomOutputPath = True
        else:
            self.useCustomOutputPath = False
        
        self.useCustomPathCheckbox.setChecked(self.useCustomOutputPath)
        self.useCustomPathCheckbox.stateChanged.connect(self.OnCheckBoxChange)
        self.defaultOutputPathInput.setText(self.config.get("ImgTools", "custom-output-path"))
        
        #buttons
        self.applyButton.clicked.connect(self.ApplySettings)
        
    def ChangeLanguage(self):
        self.currentLanguage = self.languagesComboBox.currentText()
        print(self.currentLanguage)
        self.config.set("ImgTools", "language", self.currentLanguage)
        
    def OnCheckBoxChange(self):
        self.useCustomOutputPath = self.useCustomPathCheckbox.isChecked()
        if(self.useCustomOutputPath):
            self.config.set("ImgTools", "use-custom-output-path", "True")
        else:
            self.config.set("ImgTools", "use-custom-output-path", "False")
        
    def ApplySettings(self):
        self.config.set("ImgTools", "custom-output-path", self.defaultOutputPathInput.text())
        
        with open('configuration.ini', 'w') as configfile:
            self.config.write(configfile)
        print("Settings Written on file")
        self.ShowRestartInfo()
        
    def ShowRestartInfo(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        if(self.currentLanguage == "Italiano"):
            msg.setText("Per applicare le impostazioni, riavviare il programma")
        else:
            msg.setText("In order to apply settings you must restart ImgTools")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setDefaultButton(QMessageBox.Ok)
        msg.exec_()
        
        
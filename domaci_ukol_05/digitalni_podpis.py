import sys
import hashlib
from PyQt5.QtWidgets import(QApplication, QMainWindow, QMessageBox,
QFileDialog)
from PyQt5 import QtGui, uic
from PyQt5 import QtWidgets


qtCreatorFile = "gui.ui" # Enter file here.
 
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
 
class MyApp(QMainWindow, Ui_MainWindow):
    
    def get_hash(self, file):
        BLOCK_SIZE = 65536 # The size of each read from the file
        file_hash = hashlib.sha3_512() # Create the hash object, can use something other than `.sha256()` if you wish
        with open(file, 'rb') as f: # Open the file to read it's bytes
            fb = f.read(BLOCK_SIZE) # Read from the file. Take in the amount declared above
            while len(fb) > 0: # While there is still data being read from the file
                file_hash.update(fb) # Update the hash
                fb = f.read(BLOCK_SIZE) # Read the next block from the file
        return (file_hash.hexdigest()) # Get the hexadecimal digest of the hash
    
    def openFileNameDialog(self):
        fileName = QFileDialog.getOpenFileName()
        if fileName:
            return fileName[0]
        
    def openDirectoryNameDialog(self):
        fileName = QFileDialog.getExistingDirectory(self, caption='Select a folder')
        if fileName:
            return fileName
        
    def error_message(self, message):
        error_message = QMessageBox()
        error_message.setText(message)
        error_message.setWindowTitle('Chyba!')
        error_message.exec()
        
    def chooseFileButton_clicked(self):
        file = self.openFileNameDialog()
        self.filePath.setText(file)

        
    def chooseDirectoryButton_clicked(self):
        file = self.openDirectoryNameDialog()
        self.DirectoryPath.setText(file)
        
    
    def generate_hash(self):
        #zkontrolovat cesty
        
        return 0    
    
    
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.chooseFileButton.clicked.connect(self.chooseFileButton_clicked)
        self.chooseDirectoryButton.clicked.connect(self.chooseDirectoryButton_clicked)
        self.generateHashButton.clicked.connect(self.generate_hash)
        
     
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtGui, uic
 
qtCreatorFile = "MojePrvniGUI - sablona.ui" # Enter file here.
 
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
 
class MyApp(QMainWindow, Ui_MainWindow):
    
    #funkce zde
                              
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.buttonSpocitejSoucetDvou.clicked.connect(self.SoucetDvouHodnot)
        self.buttonSpocitejSoucetTri.clicked.connect(self.SoucetTriHodnot)
     
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())

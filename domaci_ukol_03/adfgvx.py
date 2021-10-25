import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtGui, uic
 
qtCreatorFile = "gui.ui"
 
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
 
def func():
    return 0


class MyApp(QMainWindow, Ui_MainWindow):
    
    defaultniTextTri = "Součet hodnot A + B + C = "
    defaultniTextDvou = "Součet hodnot A + B = "
    nevalidniVstupHlaska = "Nebylo zadané číslo !!!"
    
    def SoucetDvouHodnot(self):

        try:
            hodnotaA = int(self.lineEditHodnotaA.text())
            hodnotaB = int(self.lineEditHodnotaB.text())
            soucet = hodnotaA + hodnotaB
            self.labelSoucetDvou.setText(self.defaultniTextDvou + str(soucet))
        except:
            self.labelSoucetDvou.setText(self.nevalidniVstupHlaska)
        
    def SoucetTriHodnot(self):

        try:
            hodnotaA = int(self.lineEditHodnotaA.text())
            hodnotaB = int(self.lineEditHodnotaB.text())
            hodnotaC = int(self.lineEditHodnotaC.text())
            soucet = hodnotaA + hodnotaB + hodnotaC
            self.labelSoucetTri.setText(self.defaultniTextTri + str(soucet))
        except:
            self.labelSoucetTri.setText(self.nevalidniVstupHlaska)
                              
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

     
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())

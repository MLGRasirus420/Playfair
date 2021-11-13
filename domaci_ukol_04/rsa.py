import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtGui, uic
from sympy import randprime, totient
import timeit
from math import gcd
from random import randint
 
qtCreatorFile = "gui.ui" # Enter file here.
 
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
 
class MyApp(QMainWindow, Ui_MainWindow):
    
    def generate_key(self):
        #1
        p = randprime(10**17,10**18-1)
        q = randprime(10**17,10**18-1)
        while q == p:
            q = randprime(10**17,10**18-1)
        #2
        n = p*q
        #3
        fi_n = (p-1)*(q-1)
        #4
        e = randint(1, fi_n)
        while gcd(e, fi_n) != 1:
            e = randint(1, fi_n)
        #5
        d = pow(e, -1, fi_n)
        self.nLine.setText(str(n))
        self.dLine.setText(str(d))
        self.eLine.setText(str(e))

    def encrypt(self, my_text, n, e):
        my_text = self.split_into_list(my_text)
        i = 0
        for item in my_text:
            my_text[i] = pow(item, int(e), int(n))
            i += 1
        return my_text
            
            
    def split_into_list(self, my_text):
        temp = []
        encrypted_list = []
        encrypted_segment = ''
        i = 0
        for character in my_text:
            if i == 5:
                for item in temp:
                    encrypted_segment += item
                encrypted_list.append(int(encrypted_segment, 2))
                encrypted_segment = ''
                temp = []
                i = 0
            temp.append(bin(ord(character))[2:].zfill(10))
            i += 1
        if temp:
            for item in temp:
                encrypted_segment += item
            encrypted_list.append(int(encrypted_segment, 2))
            
        return encrypted_list
            
        
    def encodeButton_clicked(self):
        my_text = self.inputText.toPlainText()
        n = self.nLine.text()
        e = self.eLine.text()
        my_text = self.encrypt(my_text, n, e)
        finished_text = ''
        for item in my_text:
            finished_text += str(item) + ' '
        finished_text = finished_text.rstrip()
        self.outputText.setPlainText(finished_text)
        
        
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.randGenButton.clicked.connect(self.generate_key)
        self.encodeButton.clicked.connect(self.encodeButton_clicked)
     
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())

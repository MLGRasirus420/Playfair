import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
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


    def check_for_empty_input(self, my_text, msg):
        if my_text == [''] or my_text == '':
            self.error_message(msg)
            return -1
        
        
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
        try:
            my_text = self.inputText.toPlainText()
            if self.check_for_empty_input(my_text, 'Pr??zdn?? vstup!') == -1: return -1
            n = self.nLine.text()
            if self.check_for_empty_input(n, 'Pr??zdn?? kl???? N! Pro ??ifrov??n?? je '
                                       'pot??eba zadat N a E.') == -1: return -1
            e = self.eLine.text()
            if self.check_for_empty_input(e, 'Pr??zdn?? kl???? E! Pro ??ifrov??n?? je '
                                       'pot??eba zadat N a E.') == -1: return -1
            my_text = self.encrypt(my_text, n, e)
            finished_text = ''
            for item in my_text:
                finished_text += str(item) + ' '
            finished_text = finished_text.rstrip()
            self.outputText.setPlainText(finished_text)
        except ValueError:
            self.error_message('N??co se pokazilo!')
        
        
    def decrypt(self, my_text, n, d):
        i = 0
        for item in my_text:
            my_text[i] = pow(int(item), int(d), int(n))
            i += 1
        return my_text
    
    
    def decode_transformation(self, my_text):
        decoded_text = ''
        i = 0
        for item in my_text:
            my_text[i] = bin(int(item))[2:].zfill(50)
            i += 1
        temp = []
        for item in my_text:
            temp = [item[i:i+10] for i in range(0, len(item), 10)]
            i = 0
            for item in temp:
                temp[i] = chr(int(item, 2))
                i += 1
            for item in temp:
                decoded_text += str(item)
        return decoded_text
    
    
    def decodeButton_clicked(self):
        try:
            my_text = self.inputText.toPlainText().split(' ')
            if self.check_for_empty_input(my_text, 'Pr??zdn?? vstup!') == -1: return -1
            n = self.nLine.text()
            if self.check_for_empty_input(n, 'Pr??zdn?? kl???? N! Pro de??ifrov??n?? je '
                                          'pot??eba zadat N a D.') == -1: return -1
            e = self.eLine.text()
            if self.check_for_empty_input(e, 'Pr??zdn?? kl???? D! Pro ??ifrov??n?? je '
                                          'pot??eba zadat N a D.') == -1: return -1
            my_text = self.decrypt(my_text, n, e)
            my_text = self.decode_transformation(my_text)
            self.outputText.setPlainText(my_text)
        except ValueError:
            self.error_message('P??i de??ifrov??n?? mus?? b??t vstup INT!')
        
    def error_message(self, message):
        error_message = QMessageBox()
        error_message.setText(message)
        error_message.setWindowTitle('Chyba!')
        error_message.exec()
    
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.randGenButton.clicked.connect(self.generate_key)
        self.encodeButton.clicked.connect(self.encodeButton_clicked)
        self.decodeButton.clicked.connect(self.decodeButton_clicked)
     
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())

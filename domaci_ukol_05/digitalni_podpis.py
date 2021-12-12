import sys
import hashlib
from PyQt5.QtWidgets import(QApplication, QMainWindow, QMessageBox,
QFileDialog)
from PyQt5 import QtGui, uic
from PyQt5 import QtWidgets
from sympy import randprime, totient
from math import gcd
from random import randint


qtCreatorFile = "gui.ui" # Enter file here.
 
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
 
class MyApp(QMainWindow, Ui_MainWindow):
    
    #rsa
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
        #list
        n_d_e = []
        n_d_e.append(str(n))
        n_d_e.append(str(d))
        n_d_e.append(str(e))
        return n_d_e


    def check_for_empty_input(self, my_text, msg):
        if my_text == [''] or my_text == '':
            self.error_message(msg)
            return -1
        
        
    def encrypt(self, my_text, n, d):
        my_text = self.split_into_list(my_text)
        i = 0
        for item in my_text:
            my_text[i] = pow(item, int(d), int(n))
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
            
        
    def encodeButton_clicked(self, my_text, n, d):
        try:
            my_text = self.inputText.toPlainText()
            if self.check_for_empty_input(my_text, 'Prázdný vstup!') == -1: return -1
            n = self.nLine.text()
            if self.check_for_empty_input(n, 'Prázdný klíč N! Pro šifrování je '
                                       'potřeba zadat N a D.') == -1: return -1
            d = self.dLine.text()
            if self.check_for_empty_input(d, 'Prázdný klíč D! Pro šifrování je '
                                       'potřeba zadat N a D.') == -1: return -1
            my_text = self.encrypt(my_text, n, d)
            finished_text = ''
            for item in my_text:
                finished_text += str(item) + ' '
            finished_text = finished_text.rstrip()
            self.outputText.setPlainText(finished_text)
        except ValueError:
            self.error_message('Něco se pokazilo!')
        
        
    def decrypt(self, my_text, n, e):
        i = 0
        for item in my_text:
            my_text[i] = pow(int(item), int(e), int(n))
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
            if self.check_for_empty_input(my_text, 'Prázdný vstup!') == -1: return -1
            n = self.nLine.text()
            if self.check_for_empty_input(n, 'Prázdný klíč N! Pro dešifrování je '
                                          'potřeba zadat N a E.') == -1: return -1
            e = self.eLine.text()
            if self.check_for_empty_input(e, 'Prázdný klíč E! Pro šifrování je '
                                          'potřeba zadat N a E.') == -1: return -1
            my_text = self.decrypt(my_text, n, e)
            my_text = self.decode_transformation(my_text)
            self.outputText.setPlainText(my_text)
        except ValueError:
            self.error_message('Při dešifrování musí být vstup INT!')
    
    
    #digitalni_podpis
    def get_hash(self, file):
        BLOCK_SIZE = 65536 # The size of each read from the file
        file_hash = hashlib.sha3_512() # Create the hash object, can use something other than `.sha256()` if you wish
        with open(file, 'rb') as f: # Open the file to read it's bytes
            fb = f.read(BLOCK_SIZE) # Read from the file. Take in the amount declared above
            while len(fb) > 0: # While there is still data being read from the file
                file_hash.update(fb) # Update the hash
                fb = f.read(BLOCK_SIZE) # Read the next block from the file
        return (file_hash.hexdigest()) # Get the hexadecimal digest of the hash
    
    
    #vyber souboru
    def openFileNameDialog(self):
        fileName = QFileDialog.getOpenFileName()
        if fileName:
            return fileName[0]
        
    #vyber slozky
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
        
    def chooseKeyFileButton_clicked(self):
        file = self.openFileNameDialog()
        self.keyPath.setText(file)
        
        
    def generateKeyFilesButton_clicked(self):
        try:
            n_d_e = self.generate_key()
            n = n_d_e[0]
            d = n_d_e[1]
            e = n_d_e[2]
            
            with open('private_key.priv', 'x') as f:
                f.write(n + '\n')
                f.write(d)
            with open('public_key.pub', 'x') as f:
                f.write(n + '\n')
                f.write(e)
                
            self.message('Hotovo!', 'Vytvořeny soubory private_key.priv a public_key.pub ve složce s programem.')
        except FileExistsError:
            self.message('Chyba!', 'Soubory už existují.')
        
    
    def sign_file(self):
        #zkontrolovat cesty
        file = self.filePath.text()
        hashcode = self.get_hash(file)
        key_file = self.keyPath.text()
        n_d = []
        with open(key_file) as f:
            for line in f:
                n_d.append(line)
        n = n_d[0].rstrip()
        d = n_d[1]
        hashcode = self.encodeButton_clicked(hashcode, n, d)
        print(hashcode)
  
    
    def message(self, title, message):
        error_message = QMessageBox()
        error_message.setText(message)
        error_message.setWindowTitle(title)
        error_message.exec()
        
        
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.chooseFileButton.clicked.connect(self.chooseFileButton_clicked)
        self.chooseDirectoryButton.clicked.connect(self.chooseDirectoryButton_clicked)
        self.chooseKeyFileButton.clicked.connect(self.chooseKeyFileButton_clicked)
        self.generateKeyFilesButton.clicked.connect(self.generateKeyFilesButton_clicked)
        self.signButton.clicked.connect(self.sign_file)
        
     
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())

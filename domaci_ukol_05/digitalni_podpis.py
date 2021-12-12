import sys
import hashlib
from PyQt5.QtWidgets import(QApplication, QMainWindow, QMessageBox,
QFileDialog)
from PyQt5 import QtGui, uic
from PyQt5 import QtWidgets
from sympy import randprime, totient
from math import gcd
from random import randint
import base64
from zipfile import ZipFile
import os
from shutil import copy2, SameFileError

class TooManyFiles(Exception):
        pass

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
            my_text = self.encrypt(my_text, n, d)
            finished_text = ''
            for item in my_text:
                finished_text += str(item) + ' '
            finished_text = finished_text.rstrip()
            return finished_text
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
    
    
    def decodeButton_clicked(self, my_text, n, e):
        try:
            my_text = my_text.split(' ')
            my_text = self.decrypt(my_text, n, e)
            my_text = self.decode_transformation(my_text)
            return my_text
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
        
        
    #filedialog soubor pro podpis
    def chooseFileButton_clicked(self):
        file = self.openFileNameDialog()
        self.filePath.setText(file)

    
    #filedialog slozka pro zip    
    def chooseDirectoryButton_clicked(self):
        file = self.openDirectoryNameDialog()
        self.DirectoryPath.setText(file)
     
        
    #file dialog pro klic
    def chooseKeyFileButton_clicked(self):
        file = self.openFileNameDialog()
        self.keyPath.setText(file)
        
        
    def generateKeyFilesButton_clicked(self):
        try:
            n_d_e = self.generate_key()
            n = n_d_e[0]
            d = n_d_e[1]
            e = n_d_e[2]
            
            with open('private_key.priv', 'w') as f:
                f.write(n + '\n')
                f.write(d)
            with open('public_key.pub', 'w') as f:
                f.write(n + '\n')
                f.write(e)         
            self.message('Hotovo!', 'Vytvořeny soubory private_key.priv a public_key.pub ve složce s programem.')
        except:
            self.message('Chyba!', 'Něco se pokazilo.')
        
    
    def sign_file(self):
        try:
            file = self.filePath.text()
            hashcode = self.get_hash(file)
            key_file = self.keyPath.text()
            n_d = []
            with open(key_file) as f:#brani klicu ze souboru
                for line in f:
                    n_d.append(line)
            n = n_d[0].rstrip()
            d = n_d[1]
            #encode hashe pomoci RSA
            hashcode = self.encodeButton_clicked(hashcode, n, d)
            hashcode = base64.b64encode (bytes(hashcode, "utf-8"))
            head, tail = os.path.split(file)
            with open('digital_signature.sign', 'wb') as f:
                f.write(hashcode)
            #kopie souboru pro ulozeni do zipu
            self.copy_file(file)
            #vytvoreni zipu
            zip_obj = ZipFile('digital_signature.zip', 'w')
            zip_obj.write('digital_signature.sign')
            zip_obj.write(tail)
            zip_obj.close()
            #smazani kopii
            os.remove('digital_signature.sign')
            os.remove(tail)
            
            self.message('Hotovo!', tail + ' a elektronický podpis: '
                         'digital_signature.sign byly uloženy do archivu: '
                         'digital_signature.zip.')  
        except FileNotFoundError:
            self.message('Chyba!', 'Soubor neexistuje!')
        except (IndexError, UnicodeDecodeError):
            self.message('Chyba!', 'Problém s klíčem! Doporučuji vytvořit nové'
                         ' klíče pomocí tlačítka: Vygenerovat soubory s klíči.')
        except:
           self.message('Chyba!', 'Něco se pokazilo.')
    
    
    def verify_file(self):
        try:
            zip_file = self.filePath.text()
            key_file = self.keyPath.text()
            n_e = []
            with open(key_file) as f:#brani klicu ze souboru
                for line in f:
                    n_e.append(line)
            n = n_e[0].rstrip()
            e = n_e[1]
            #zjisti co je co v zipu
            with ZipFile(zip_file, 'r') as my_zip:
                zip_files = my_zip.namelist()
            
            #kontrola zipu
            if len(zip_files) > 2:
                raise TooManyFiles
            
            #pokracovani patrani co je co
            signature = zip_files.index('digital_signature.sign')
            signature = zip_files.pop(signature)
            file = zip_files.pop(0)
            with ZipFile(zip_file, 'r') as my_zip:
                hashcode = my_zip.read(signature)#zasifrovany hash co prisel se souborem
                my_zip.extract(file)#nachvilku si ho vytahnu, neprisel jsem na to jak se podivat do zipu
            new_hashcode = self.get_hash(file)
            os.remove(file)#extrahovanou kopii mazu
            hashcode = base64.b64decode(hashcode).decode("utf-8")#z5 na string
            hashcode = self.decodeButton_clicked(hashcode, n, e)#desifrovani RSA
            hashcode = hashcode.replace('\x00', '')#fantom
            if hashcode == new_hashcode:
                self.message('Oznamení!', 'Hash je stejný. Soubor nebyl pozměněn.')
            else:
                self.message('Oznamení!', 'Hash se liší! Se souborem bylo '
                             'manipulováno.')
        except FileNotFoundError:
            self.message('Chyba!', 'Soubor neexistuje!')
        except (IndexError, UnicodeDecodeError):
            self.message('Chyba!', 'Problém s klíčem! Doporučuji vytvořit nové'
                         ' klíče pomocí tlačítka: Vygenerovat soubory s klíči.')
        except ValueError:
            self.message('Chyba!', 'V zipu chybí digitální podpis!')
        except TooManyFiles:
            self.message('Chyba!', 'V zipu je moc souborů. V zipu by měly být'
                          ' dva soubory. Soubor .sign a podepsaný soubor.')
        except:
           self.message('Chyba!', 'Něco se pokazilo.')
            
            
    def message(self, title, message):
        error_message = QMessageBox()
        error_message.setText(message)
        error_message.setWindowTitle(title)
        error_message.exec()
        
        
    def signRadio_clicked(self):
        print('moje hovno')
        
        
    def verificationRadio_clicked(self):
        print('tvoje hovno')    
        
        
    def get_program_path(self):
        head, tail = os.path.split(sys.argv[0])
        return head
    
    
    def copy_file(self, file):
        #pokud je soubor nakopirovany ve slozce s programem tak se kopie nedela
        try:
            program_path = self.get_program_path()
            copy2(file, program_path)
        except SameFileError:
            pass
    
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.chooseFileButton.clicked.connect(self.chooseFileButton_clicked)
        self.chooseKeyFileButton.clicked.connect(self.chooseKeyFileButton_clicked)
        self.generateKeyFilesButton.clicked.connect(self.generateKeyFilesButton_clicked)
        self.signButton.clicked.connect(self.sign_file)
        self.signRadio.clicked.connect(self.signRadio_clicked)
        self.verificationRadio.clicked.connect(self.verificationRadio_clicked)
        self.verifyButton.clicked.connect(self.verify_file)
        
     
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
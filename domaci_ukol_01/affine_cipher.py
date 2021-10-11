import string, sys
from math import gcd
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5 import uic


def encrypt(key_a, key_b, my_text):
    """ Encrypts a string. Affine cipher. """
    alphabet = list(form_alphabet())
    encrypted_text = ''
    my_text = format_text(my_text)
    for character in my_text:
        alphabet_index = (key_a * alphabet.index(character) + key_b) % 36
        encrypted_text += alphabet[alphabet_index]
    encrypted_text = split_by_x(encrypted_text, 5)
    return encrypted_text
        
        
def decrypt(key_a, key_b, my_text):
    """Decrypts a string. Affine cipher. """
    alphabet = list(form_alphabet())
    mmi = inverzni_prvek(key_a, 36)
    my_text = remove_spaces(my_text)
    decrypted_text = ''
    for character in my_text:
        alphabet_index = (alphabet.index(character) - key_b) * mmi % 36
        decrypted_text += alphabet[alphabet_index]
    decrypted_text = replace_xmezerax(decrypted_text)
    return decrypted_text
    
    
def format_text(my_text):
    """ Formats text for encryption. """
    my_text = my_text.upper()
    my_text = remove_accents(my_text)
    my_text = replace_spaces(my_text)
    my_text = remove_non_letters(my_text)
    return my_text


def remove_non_letters(my_text):
    """Removes letters that are not in alphabet."""
    for character in my_text[ : :-1]:
        if character not in form_alphabet():
            my_text = my_text.replace(character, '')
    return my_text


def remove_accents(my_text):
    """ Replaces accented letters. """
    dict_accents = {'Á': 'A', 'Č': 'C', 'Ď': 'D', 'Ě': 'E', 'É': 'E', 'Í': 'I',
                    'Ň': 'N', 'Ó': 'O', 'Ř': 'R', 'Š': 'S', 'Ť': 'T', 'Ú': 'U',
                    'Ů': 'U', 'Ý': 'Y', 'Ž': 'Z', }
    for character in my_text:
        if character in dict_accents:
            my_text = my_text.replace(character, dict_accents.get(character))
    return my_text

    
def form_alphabet():
    """ Forms an alphabet that's used for encryption/decryption. """
    alphabet = string.ascii_uppercase
    for i in range(10):
        alphabet+=str(i)
    return alphabet

def replace_spaces(my_text):
    """ Replaces spaces with XMEZERAX. """
    return my_text.replace(' ', 'XMEZERAX')

def remove_spaces(my_text):
    """ Removes spaces from a string. """
    return my_text.replace(' ', '')

def replace_xmezerax(my_text):
    """ Replaces XMEZERAX in a string with a space character. """
    return my_text.replace('XMEZERAX', ' ')


def split_by_x(my_text, x):
    """ Inserts a space character in a string after x characters. """
    return ' '.join(my_text[i:i + x] for i in range(0, len(my_text), x))


def inverzni_prvek(a, m):
    """ Calculates modular multiplicative inverse 
        Sprostě ukradeno z moodle pro mě spíše španělská vesnice."""
    if gcd(a, m) != 1:
        return -1
    else:
        for i in range(0, m):
            if (i * a % m) == 1:
                break
        return i


qtCreatorFile = "gui.ui"
 
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QMainWindow, Ui_MainWindow):
    def encryptButtonClicked(self):       
        try:    
            a = int(self.keyA.currentText())
            b = int(self.keyB.value())
            my_text = self.origText.toPlainText()
            my_text = encrypt(a, b, my_text)   
            self.encText.setText(str(my_text))
            alphabet = self.alphabet.toPlainText()
            alphabet = encrypt(a, b, alphabet)
            alphabet = remove_spaces(alphabet)
            self.encAlphabet.setText(str(alphabet))
        except:
            self.errorMessage('Něco se pokazilo.')

            
            
    def decryptButtonClicked(self):      
        try:
            a = int(self.keyA.currentText())
            b = int(self.keyB.value()) 
            my_text = self.origText.toPlainText()
            my_text = decrypt(a, b, my_text)   
            self.encText.setText(str(my_text))    
            alphabet = self.alphabet.toPlainText()
            alphabet = encrypt(a, b, alphabet)
            alphabet = remove_spaces(alphabet)
            self.encAlphabet.setText(str(alphabet))
        except:
            self.errorMessage('Vstup musí být složený ze znaků v abecedě.')
        
    
    def errorMessage(self, message):
        error_message = QMessageBox()
        error_message.setText(message)
        error_message.setWindowTitle('Chyba!')
        error_message.exec()
        
        
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.encryptButton.clicked.connect(self.encryptButtonClicked)
        self.decryptButton.clicked.connect(self.decryptButtonClicked)
     
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())

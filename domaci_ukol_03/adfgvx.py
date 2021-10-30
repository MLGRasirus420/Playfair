import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox
from PyQt5 import QtGui, uic
from random import randint
 
qtCreatorFile = "gui.ui"
 
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
 

def remove_accents(my_text):
    """ Replaces accented letters. """
    dict_accents = {'Á': 'A', 'Č': 'C', 'Ď': 'D', 'Ě': 'E', 'É': 'E', 'Í': 'I',
                    'Ň': 'N', 'Ó': 'O', 'Ř': 'R', 'Š': 'S', 'Ť': 'T', 'Ú': 'U',
                    'Ů': 'U', 'Ý': 'Y', 'Ž': 'Z', }
    for character in my_text:
        if character in dict_accents:
            my_text = my_text.replace(character, dict_accents.get(character))
    return my_text


def replace_extra_character(my_text, lang):
    """ Replaces one character with another depending on the language chosen. 
        0 = EN [J -> I], 1 = CZ [Q -> O] """
    if(lang == 0):    
        replaced = 'J'
        replacement = 'I'
    elif(lang == 1):
        replaced = 'Q'
        replacement = 'O'
    else:
        return -1    
    return my_text.replace(replaced, replacement)


def remove_non_letters(my_text, alphabetMatrix):
    """Removes letters that are not in alphabet."""
    for character in my_text[ : :-1]:
        if character not in alphabetMatrix:
            my_text = my_text.replace(character, '')
    return my_text


def format_key(key, lang, alphabet):
    key = key.upper()
    key = remove_accents(key)
    key = replace_extra_character(key, lang)
    key = remove_non_letters(key, alphabet)
    return key


def encode(my_text, key, lang, alphabet):
    key = format_key(key, lang, alphabet)
    return 0

def decode():
    return 0


class MyApp(QMainWindow, Ui_MainWindow):
    adfgx_index = ['A', 'D', 'F', 'G', 'X']
    adfgvx_index = ['A', 'D', 'F', 'G', 'V', 'X']
    alphabet_cz = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                  'M', 'N', 'O', 'P', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                  'Z']
    alphabet_en = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M',
                  'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                  'Z']
    
    
    def fill_tableWidget(self, alphabet):
        """ Fills tableWidget """
        line = 0
        row = 0
        for char in alphabet:
            self.tableWidget.setItem(line, row, QTableWidgetItem(char))
            row += 1
            if row == 5:
                row = 0
                line += 1


    def rand_alphabet(self, alphabet_original):
        alphabet = alphabet_original.copy()
        r_alphabet = []

        i = len(alphabet) - 1
        while alphabet:
            index = randint(0, i)
            r_alphabet.append(alphabet.pop(index))
            i -= 1
        return r_alphabet
            
        
    def errorMessage(self, message):
        error_message = QMessageBox()
        error_message.setText(message)
        error_message.setWindowTitle('Chyba!')
        error_message.exec()
    
    
    def checkLang(self):
        if self.czRadioButton.isChecked():
            return 1
        elif self.enRadioButton.isChecked():
            return 0
        
    def chooseAlphabet(self, lang):
        if lang == 1:
            return self.alphabet_cz
        else:
            return self.alphabet_en
        
        
    def encodeButtonClicked(self):
        try:
            lang = self.checkLang()
            alphabet = self.rand_alphabet(self.chooseAlphabet(lang))#temp untill table writing and reading finished
            my_text = self.inputText.toPlainText()
            key = self.inputKey.text()
            my_text = encode(my_text, key, lang, alphabet)
            self.outputText.setPlainText(my_text)
        except:
            self.errorMessage('Vstup nesmí být prázdný!')

        
    def decodeButtonClicked(self):
        try:
            lang = self.checkLang()
            my_text = self.inputText.toPlainText()
            key = self.inputKey.text()
            #my_text = decode(my_text, key, lang)
            self.outputText.setPlainText(my_text)
        except:
            self.errorMessage('Vstup nesmí být prázdný!')
            
    
    def randTableButtonClicked(self):
        alphabet = self.rand_alphabet(self.chooseAlphabet(self.checkLang()))
        self.fill_tableWidget(alphabet)
                

    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.encodeButton.clicked.connect(self.encodeButtonClicked)
        self.decodeButton.clicked.connect(self.decodeButtonClicked)
        self.randTableButton.clicked.connect(self.randTableButtonClicked)

     
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
    

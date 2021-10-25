import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtGui, uic
 
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


class MyApp(QMainWindow, Ui_MainWindow):
    adfgx_index = ['A', 'D', 'F', 'G', 'X']
    adfgvx_index = ['A', 'D', 'F', 'G', 'V', 'X']
    alphabet_cz = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                  'M', 'N', 'O', 'P', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                  'Z']
    alphabet_en = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M',
                  'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                  'Z']
    rand_alphabet = shuffle_alphabet()
    
    
    def checkLang(self):
        if self.czRadioButton.isChecked():
            return 1
        elif self.enRadioButton.isChecked():
            return 0
                

    def encodeButtonClicked
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

     
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())

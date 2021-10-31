import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox
from PyQt5 import QtGui, uic
from random import randint
from math import floor
 
qtCreatorFile = "gui.ui"
 
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
 
class MyApp(QMainWindow, Ui_MainWindow):
    adfgx_index = {'0':'A', '1':'D', '2':'F', '3':'G', '4':'X'}
    adfgvx_index = ['A', 'D', 'F', 'G', 'V', 'X']
    alphabet_cz = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                  'M', 'N', 'O', 'P', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                  'Z']
    alphabet_en = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M',
                  'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                  'Z']
    
    def encode(self, my_text, alphabet):
        encoded_text = ''
        for character in my_text:
            index = alphabet.index(character)
            row = floor(index / 5)
            column = index % 5
            encoded_text += str(row) + str(column)
        return encoded_text

    
    def switch_indexes(self, my_text, mode):
        #Encode: mode == True; Decode: mode == False
        if mode == True:
            for character in my_text:
                my_text = my_text.replace(character, self.adfgx_index.get(character))
        else:
            for key, value in self.adfgx_index.items():
                my_text = my_text.replace(value, key)
        return my_text
    
    
    def make_key_list(self, key):
        key_list = []
        key_char_index = 0
        for character in key:
            key_list.append(character + str(key_char_index))
            key_char_index += 1
        return sorted(key_list)
    
    
    def make_encode_trans_table(self, key, my_text):
        trans_table = []
        temp_list = []
        key_length = len(key)
        i = 0
        for character in my_text:
            temp_list.append(character)
            i += 1
            if i == key_length:
                trans_table.append(temp_list)
                temp_list = []
                i = 0 
        
        while i <= key_length - 1:
            temp_list.append('')
            i += 1
        trans_table.append(temp_list)
        
        return trans_table


    def encode_transposition(self, sorted_key_list, trans_table):
        my_text = ''
        for element in sorted_key_list:
            i = 0
            while i < len(trans_table):
                my_text += trans_table[i][int(element[1])]
                i += 1
            my_text += ' '
        return my_text

    
    def decode(self, my_text):
        #finds a character in the tableWidget based on index
        decoded_text = ''
        length = len(my_text)
        i = 1
        while i < length:
            column = int(my_text[i])
            row = int(my_text[i - 1])
            decoded_text += self.tableWidget.item(row, column).text()
            i += 2
        return decoded_text
       
    
    def make_decode_trans_table(self, my_text, key):
        #prepare empty trans table
        trans_table = []
        #inserting data into transtable
        row = 0
        column = 0
        for character in my_text:
            if character == ' ':
                row = 0
                column += 1
                continue
            if row == 0:
                trans_table.append([character])
                row += 1
            else:
                trans_table[column].append(character)
         
        return trans_table
        

    def decode_trans_list_order(self, sorted_key ,trans_table):
        #finding correct order
        order = ''
        key_length = len(sorted_key)
        i = 0
        while i < key_length:
            for element in sorted_key:
                if element[1] == str(i):
                    order += str(sorted_key.index(element))
                    i += 1
        #applying order
        ordered_list = []
        for character in order:
            ordered_list.append(trans_table[int(character)])
        return ordered_list


    def decode_trans(self, ordered_list):
        trans_string = ''
        while ordered_list:
            try:
                for element in ordered_list:
                    trans_string += element.pop(0)
            except IndexError:
                return trans_string 
        
        
    def remove_accents(self, my_text):
        """ Replaces accented letters. """
        dict_accents = {'Á': 'A', 'Č': 'C', 'Ď': 'D', 'Ě': 'E', 'É': 'E', 'Í': 'I',
                        'Ň': 'N', 'Ó': 'O', 'Ř': 'R', 'Š': 'S', 'Ť': 'T', 'Ú': 'U',
                        'Ů': 'U', 'Ý': 'Y', 'Ž': 'Z', }
        for character in my_text:
            if character in dict_accents:
                my_text = my_text.replace(character, dict_accents.get(character))
        return my_text
    
    
    def replace_extra_character(self, my_text, lang):
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
    
    
    def replace_numbers(self, my_text, mode):
        """Replaces numbers with abbreviations if true. """
        dict_numbers = {'1': 'XONX', '2': 'XTWX', '3': 'XTHX', '4': 'XFOX',
                        '5': 'XFIX', '6': 'XSIX',
                        '7': 'XSEX', '8': 'XEIX', '9': 'XNIX', '0': 'XZEX', }
        if mode == True:
            for character in my_text:
                    if character in dict_numbers:
                        my_text = my_text.replace(character, 
                                                  dict_numbers.get(character))
        else:
            for key, value in dict_numbers.items():
                my_text = my_text.replace(value, key)
        return my_text


    def replace_spaces(self, my_text, mode):
        """ Replaces spaces with XSPCX if True. Else replaces XSPC with a space. 
        """
        if mode == True:
            return my_text.replace(' ', 'XSPCX')
        else:
            return my_text.replace('XSPCX', ' ')
    
    
    def remove_non_letters(self, my_text, alphabet):
        """Removes letters that are not in alphabet."""
        for character in my_text[ : :-1]:
            if character not in alphabet:
                my_text = my_text.replace(character, '')
        return my_text


    def format_key(self, key, lang, alphabet):
        key = key.upper()
        key = self.remove_accents(key)
        key = self.replace_extra_character(key, lang)
        key = self.remove_non_letters(key, alphabet)
        return key
    
    
    def format_input_output(self, my_text, lang, mode, alphabet):
        """ Encode: Mode == True; Decode: Mode == False"""
        if mode == True:
            my_text = my_text.upper()
            my_text = self.remove_accents(my_text)
            my_text = self.replace_extra_character(my_text, lang)
        my_text = self.replace_spaces(my_text, mode)
        my_text = self.replace_numbers(my_text, mode)
        if mode == True:
            my_text = self.remove_non_letters(my_text, alphabet)  
        return my_text
        
        
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
    
    
    def check_Lang(self):
        if self.czRadioButton.isChecked():
            return 1
        elif self.enRadioButton.isChecked():
            return 0
        
        
    def choose_Alphabet(self, lang):
        if lang == 1:
            return self.alphabet_cz
        else:
            return self.alphabet_en
        
        
    def tableWidget_into_list(self):
        alphabet = []
        row = 0
        column = 0
        while row <= 4:
            alphabet.append((self.tableWidget.item(row, column).text()))
            column += 1
            if column == 5:
                column = 0
                row += 1
        return alphabet
    
    
    def encodeButtonClicked(self):
        try:
            lang = self.check_Lang()
            alphabet = self.tableWidget_into_list()#add remove numbers, remove duplicates
            my_text = self.inputText.toPlainText()
            key = self.inputKey.text()
            my_text = self.format_input_output(my_text, lang, True, alphabet)
            key = self.format_key(key, lang, alphabet)
            
            my_text = self.encode(my_text, alphabet)
            my_text = self.switch_indexes(my_text, True)
            key_list = self.make_key_list(key)
            trans_table = self.make_encode_trans_table(key, my_text)
            my_text = self.encode_transposition(key_list, trans_table)
            
            self.outputText.setPlainText(my_text)
        except:
            self.errorMessage('Vstup nesmí být prázdný!')

        
    def decodeButtonClicked(self):
        try:
            lang = self.check_Lang()
            alphabet = self.tableWidget_into_list()#add remove numbers, remove duplicates
            my_text = self.inputText.toPlainText()
            key = self.inputKey.text()
            key = self.format_key(key, lang, alphabet)
            sorted_key_list = self.make_key_list(key)
            
            #Decode
            trans_table = self.make_decode_trans_table(my_text, key)
            ordered_trans_list = self.decode_trans_list_order(sorted_key_list, trans_table)
            my_text = self.decode_trans(ordered_trans_list)
            my_text = self.switch_indexes(my_text, False)
            my_text = self.decode(my_text)
            my_text = self.format_input_output(my_text, lang, False, alphabet)
            self.outputText.setPlainText(my_text)
        except:
            self.errorMessage('Vstup nesmí být prázdný!')
            
            
    def randTableButtonClicked(self):            
        """On click generates random alphabet into tableWidget depending on
           language"""
        alphabet = self.rand_alphabet(self.choose_Alphabet(self.check_Lang()))
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
    

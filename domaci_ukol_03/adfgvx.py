import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox
from PyQt5 import QtGui, uic
from random import randint
from math import floor
 
qtCreatorFile = "gui.ui"
 
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
 
class MyApp(QMainWindow, Ui_MainWindow):
    adfgx_index = {'0':'A', '1':'D', '2':'F', '3':'G', '4':'X'}
    adfgvx_index = {'0':'A', '1':'D', '2':'F', '3':'G', '4':'V', '5':'X'}
    alphabet_cz = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                  'M', 'N', 'O', 'P', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                  'Z']
    alphabet_en = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M',
                  'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                  'Z']
    alphabet_six = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                  'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                  'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    #5x5: mode = True; 6x6: mode = False
    mode = True
    
    def encode(self, my_text, alphabet):
        encoded_text = ''
        if self.mode == True:
            size = 5
        else:
            size = 6
        for character in my_text:
            index = alphabet.index(character)
            row = floor(index / size)
            column = index % size
            encoded_text += str(row) + str(column)
        return encoded_text

    
    def switch_indexes(self, my_text, enc_or_dec):
        #Encode: enc_or_dec == True; Decode: enc_or_dec == False
        if self.mode == True:
            if enc_or_dec == True:
                for character in my_text:
                    my_text = my_text.replace(character, self.adfgx_index.get(character))
            else:
                for key, value in self.adfgx_index.items():
                    my_text = my_text.replace(value, key)
        else:
            if enc_or_dec == True:
                for character in my_text:
                    my_text = my_text.replace(character, self.adfgvx_index.get(character))
            else:
                for key, value in self.adfgvx_index.items():
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
            if self.mode == True:
                decoded_text += self.tableWidget.item(row, column).text()
            else:
                decoded_text += self.tableWidgetSix.item(row, column).text()
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
    
    
    def replace_numbers(self, my_text, enc_or_dec):
        """Replaces numbers with abbreviations if true. """
        dict_numbers = {'1': 'XONX', '2': 'XTWX', '3': 'XTHX', '4': 'XFOX',
                        '5': 'XFIX', '6': 'XSIX',
                        '7': 'XSEX', '8': 'XEIX', '9': 'XNIX', '0': 'XZEX', }
        if enc_or_dec == True:
            for character in my_text:
                    if character in dict_numbers:
                        my_text = my_text.replace(character, 
                                                  dict_numbers.get(character))
        else:
            for key, value in dict_numbers.items():
                my_text = my_text.replace(value, key)
        return my_text


    def replace_spaces(self, my_text, enc_or_dec):
        """ Replaces spaces with XSPCX if True. Else replaces XSPC with a space. 
        """
        if enc_or_dec == True:
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
        if self.mode == True:
             key = self.replace_extra_character(key, lang)
        key = self.remove_non_letters(key, alphabet)
        return key
    
    
    def format_input_output(self, my_text, lang, enc_or_dec, alphabet):
        """ Encode: enc_or_dec == True; Decode: enc_or_dec == False"""
        if self.mode == True:    
            if enc_or_dec == True:
                my_text = my_text.upper()
                my_text = self.remove_accents(my_text)
                my_text = self.replace_spaces(my_text, enc_or_dec)
                my_text = self.replace_extra_character(my_text, lang)
                my_text = self.replace_numbers(my_text, enc_or_dec)
                my_text = self.remove_non_letters(my_text, alphabet) 
            else:
                my_text = my_text.upper()
                my_text = self.replace_spaces(my_text, enc_or_dec)
                my_text = self.replace_numbers(my_text, enc_or_dec)
        else:
            if enc_or_dec == True:
                my_text = my_text.upper()
                my_text = self.remove_accents(my_text)
                my_text = self.replace_spaces(my_text, enc_or_dec)
                my_text = self.remove_non_letters(my_text, alphabet) 
            else:
                my_text = my_text.upper()
                my_text = self.replace_spaces(my_text, enc_or_dec)
                my_text = self.replace_numbers(my_text, enc_or_dec)
        return my_text
        
        
    def fill_tableWidget(self, alphabet):
        """ Fills tableWidget """
        line = 0
        row = 0
        if self.mode == True:
            for char in alphabet:
                self.tableWidget.setItem(line, row, QTableWidgetItem(char))
                row += 1
                if row == 5:
                    row = 0
                    line += 1
        else:
            for char in alphabet:
                self.tableWidgetSix.setItem(line, row, QTableWidgetItem(char))
                row += 1
                if row == 6:
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
            
        
    def error_message(self, message):
        error_message = QMessageBox()
        error_message.setText(message)
        error_message.setWindowTitle('Chyba!')
        error_message.exec()
    
    
    def check_lang(self):
        if self.czRadioButton.isChecked():
            return 1
        elif self.enRadioButton.isChecked():
            return 0
    
    
    def choose_mode_five(self):
        self.mode = True
        self.tableWidget.setHidden(False)
        self.tableWidgetSix.setHidden(True)
        self.czRadioButton.setHidden(False)
        self.enRadioButton.setHidden(False)
        self.randTableButton.move(520, 475)
        self.labelKey.move(595, 530)
        self.inputKey.move(520, 550)
        self.encodeButton.move(520, 570)
        self.decodeButton.move(615, 570)
        
        
    def choose_mode_six(self):
        self.mode = False
        self.tableWidget.setHidden(True)
        self.tableWidgetSix.setHidden(False)
        self.czRadioButton.setHidden(True)
        self.enRadioButton.setHidden(True)
        self.randTableButton.move(520, 483)
        self.labelKey.move(595, 530)
        self.inputKey.move(520, 550)
        self.encodeButton.move(520, 570)
        self.decodeButton.move(615, 570)
        
        
    def choose_Alphabet(self, lang):
        if self.mode == True:    
            if lang == 1:
                return self.alphabet_cz
            else:
                return self.alphabet_en
        else:
            return self.alphabet_six
        
        
    def tableWidget_into_list(self):
        alphabet = []
        row = 0
        column = 0
        if self.mode == True:
            while row <= 4:
                alphabet.append((self.tableWidget.item(row, column).text()))
                column += 1
                if column == 5:
                    column = 0
                    row += 1
        else:
            while row <= 5:
                alphabet.append((self.tableWidgetSix.item(row, column).text()))
                column += 1
                if column == 6:
                    column = 0
                    row += 1
        return alphabet
    
    
    def check_for_numbers(self, alphabet):
        if self.mode == True:
                for element in alphabet:
                    if ord(element) >= 48 and ord(element) <= 57:
                        self.error_message('V tabulce nesmí být čísla!')
                        return -1
        
        
    def check_for_numbers_decode_input(self, my_text):
        for character in my_text:
                    if ord(character) >= 48 and ord(character) <= 57:
                        self.error_message('Na vstupu nesmí být čísla!')
                        return -1
      
        
    def check_for_duplicates(self, alphabet):
        if self.mode == True:
            size = 25
        else:
            size = 36
        if len(list(dict.fromkeys(alphabet))) < size:
                self.error_message('V tabulce se nesmí nacházet duplicitní znaky!')
                return -1
    
    
    def check_for_unallowed_characters(self, lang, alphabet):
        for element in alphabet:
                if self.mode == True:
                    if lang == 1:
                        if element not in self.alphabet_cz:
                            self.error_message('V tabulce pro český jazyk musí' 
                                               ' být pouze znaky A-Z a nesmí '
                                               'obsahovat písmeno Q! To je '
                                               'nahrazeno za O. '
                                               'Vygenerujte si novou tabulku '
                                               'nebo si zkontroluje co jste ' 
                                               'vepsali dovnitř.')
                            return -1
                    if lang == 0:
                        if element not in self.alphabet_en:
                            self.error_message('V tabulce pro anglický jazyk '
                                               'musí být pouze znaky A-Z '
                                               'a nesmí obsahovat písmeno J! '
                                               'To je nahrazeno za I. '
                                               'Vygenerujte si novou tabulku '
                                               'nebo si zkontroluje co jste ' 
                                               'vepsali dovnitř.')
                            return -1
                else:
                    if element not in self.alphabet_six:
                        self.error_message('V tabulce o velikosti 6x6 musí být' 
                                           'pouze znaky A-Z a čísla 0-9! '
                                           'Vygenerujte si novou tabulku '
                                           'nebo si zkontroluje co jste ' 
                                           'vepsali dovnitř.')
                        return -1
      
        
    def check_table(self, lang, alphabet):
        result = self.check_for_numbers(alphabet)
        if result: return result
        result = self.check_for_duplicates(alphabet)
        if result: return result
        result = self.check_for_unallowed_characters(lang, alphabet)
        if result: return result
    
    
    def check_input_length(self, my_text, key):
        if len(my_text) * 2 < len(key):
                self.error_message('Délka vstupu * 2 musí být alespoň stejně ' 
                                   'dlouhá jak klíč!')
                return -1
    
    
    def check_for_unallowed_characters_decode_input(self, my_text, alphabet):
        result = 0
        for character in my_text:
            if character == ' ':
                continue
            if character not in alphabet:
                result = -1
        return result
    
    
    def check_decode_input(self, my_text, lang, alphabet):
        result = self.check_for_numbers_decode_input(my_text)
        if result: return result
        result = self.check_for_unallowed_characters_decode_input(my_text, alphabet)
        if result: return result
        
        
    def encodeButtonClicked(self):
        try:
            lang = self.check_lang()
            alphabet = self.tableWidget_into_list()
            if self.check_table(lang, alphabet) == -1: return -1
            my_text = self.inputText.toPlainText()
            key = self.inputKey.text()
            my_text = self.format_input_output(my_text, lang, True, alphabet)
            key = self.format_key(key, lang, alphabet)
            if not key:
                self.error_message('Klíč nesmí zůstat prázdný!')
                return -1
            if self.check_input_length(my_text, key) == -1: return -1
            #encode
            my_text = self.encode(my_text, alphabet)
            my_text = self.switch_indexes(my_text, True)
            key_list = self.make_key_list(key)
            trans_table = self.make_encode_trans_table(key, my_text)
            my_text = self.encode_transposition(key_list, trans_table)
            self.outputText.setPlainText(my_text)
        except:
            self.error_message('Ani klíč, vstup ani tabulka nesmí být prázdné!')

        
    def decodeButtonClicked(self):
        try:
            lang = self.check_lang()
            alphabet = self.tableWidget_into_list()
            if self.check_table(lang, alphabet) == -1: return -1
            my_text = self.inputText.toPlainText()
            my_text = my_text.upper()
            if self.check_decode_input(my_text, lang, alphabet) == -1: return -1
            key = self.inputKey.text()
            key = self.format_key(key, lang, alphabet)
            sorted_key_list = self.make_key_list(key)
            #decode
            trans_table = self.make_decode_trans_table(my_text, key)
            ordered_trans_list = self.decode_trans_list_order(sorted_key_list, trans_table)
            my_text = self.decode_trans(ordered_trans_list)
            my_text = self.switch_indexes(my_text, False)
            my_text = self.decode(my_text)
            my_text = self.format_input_output(my_text, lang, False, alphabet)
            self.outputText.setPlainText(my_text)
        except:
            self.error_message('Ani klíč, vstup ani tabulka nesmí být prázdné!')
            
            
    def randTableButtonClicked(self):            
        """On click generates random alphabet into tableWidget depending on
           language"""
        if self.mode == True:
            lang = self.check_lang()
            if lang == 1:
                alphabet = self.rand_alphabet(self.alphabet_cz)
                self.fill_tableWidget(alphabet)
            elif lang == 0:
               alphabet = self.rand_alphabet(self.alphabet_en)
               self.fill_tableWidget(alphabet) 
        else:
            alphabet = self.rand_alphabet(self.alphabet_six)
            self.fill_tableWidget(alphabet)


    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.tableWidgetSix.setHidden(True)
        self.encodeButton.clicked.connect(self.encodeButtonClicked)
        self.decodeButton.clicked.connect(self.decodeButtonClicked)
        self.randTableButton.clicked.connect(self.randTableButtonClicked)
        self.modeButtonFive.clicked.connect(self.choose_mode_five)
        self.modeButtonSix.clicked.connect(self.choose_mode_six)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
    

from string import ascii_uppercase


def format_key(key):
    key = key.upper()
    key = remove_accents(key)
    key = remove_non_letters(key)
    key = replace_extra_character(key, 1)#replace number with lang
    key = remove_duplicates(key)
    return key
    
    
def make_table(key):
    """ Creates a list and fills it with key + remaining alphabet strings size 5. """
    my_list = ['', '', '', '', '']
    key = format_key(key)
    alphabet = form_alphabet(key)
    i = 0
    for character in alphabet:
        if character == ' ':
            i += 1
            continue
        my_list[i] += character
    return my_list


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
    """ Replaces one character with another to fit inside 5x5 grid. 
        0 = EN [J -> I], 1 = CZ [Q -> O] """
    if(lang == 0):    
        replaced = 'J'
        replacement = 'I'
    elif(lang == 1):
        replaced = 'Q'
        replacement = 'O'
    else:
        return -1    
    my_text = my_text.replace(replaced, replacement)
    return my_text
    

def remove_duplicates(my_text):
    return ''.join(dict.fromkeys(my_text))


def form_alphabet(key):
    """ Forms an alphabet without characters in the key and appends the key at
     index 0 """
    alphabet = ascii_uppercase
    alphabet = replace_extra_character(alphabet, 1)#replace number with lang
    alphabet = remove_duplicates(alphabet)
    for character in key:
        alphabet = alphabet.replace(character, '')   
    return split_by_x(key + alphabet, 5)
           
                   
def split_by_x(my_text, x):
    """ Inserts a space character in a string after x characters. """
    return ' '.join(my_text[i:i + x] for i in range(0, len(my_text), x))


def replace_spaces(my_text, mode):
    """ Replaces spaces with XSPCX if True. Else replaces XSPC with a space. 
    """
    if mode == True:
        return my_text.replace(' ', 'XSPCX')
    else:
        return my_text.replace('XSPCX', ' ')


def replace_numbers(my_text, mode):
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


def remove_non_letters(my_text):
    """Removes letters that are not in alphabet."""
    for character in my_text[ : :-1]:
        if character not in form_alphabet(''):#empty input = unchanged alphabet
            my_text = my_text.replace(character, '')
    return my_text


def remove_same_pairs(my_text):
    i = 0
    for character in my_text:
        if i % 2 != 0:
            if my_text[i] == my_text[i - 1]:
                if my_text[i] == 'X':
                    substitute = 'W'
                else:
                    substitute = 'X'
                my_text = my_text[:i] + substitute + my_text[i:]
        i += 1
    return my_text


def add_end_character(my_text):
    if my_text[len(my_text) -  1] == 'X':
        substitute = 'W'
    else:
        substitute = 'X'
    return my_text + substitute
    
    
def format_input(my_text):
    my_text = my_text.upper()
    my_text = remove_accents(my_text)
    my_text = replace_spaces(my_text, True)
    my_text = replace_numbers(my_text, True)
    my_text = remove_non_letters(my_text)
    my_text = remove_same_pairs(my_text)
    if len(my_text) % 2 != 0:
        my_text = add_end_character(my_text)
    return split_by_x(my_text, 2)


def encode_decode_operation(my_text, key, mode):
    """ Encode - mode == 1, Decode - mode == -1"""
    my_text = format_input(my_text)
    table = make_table(key)
    encoded_decoded_text = ''
    i = 0
    while i <= len(my_text):
        if find_index(my_text[i], table)[0] == find_index(my_text[i + 1], table)[0]:
            encoded_decoded_text += line_rule(my_text[i], my_text[i + 1], table, mode)
            i += 3
        elif find_index(my_text[i], table)[1] == find_index(my_text[i + 1], table)[1]:
            encoded_decoded_text += column_rule(my_text[i], my_text[i + 1], table, mode)
            i+=3
        else:
            encoded_decoded_text += cross_rule(my_text[i], my_text[i + 1], table)
            i+=3
    return encoded_decoded_text


def cross_rule(character, next_character, table):
    """ Funguje i na decode. """
    encrypted_pair = ''
    first_char_index = find_index(character, table)
    second_char_index = find_index(next_character, table)
    encrypted_pair += table[int(first_char_index[0])][int(second_char_index[1])]
    encrypted_pair += table[int(second_char_index[0])][int(first_char_index[1])]
    return encrypted_pair


def line_rule(character, next_character, table, mode):
    encrypted_pair = ''
    first_char_index = find_index(character, table)
    second_char_index = find_index(next_character, table)
    encrypted_pair += table[int(first_char_index[0])][(int(first_char_index[1]) + mode) % 5]
    encrypted_pair += table[int(second_char_index[0])][(int(second_char_index[1]) + mode) % 5]
    return encrypted_pair


def column_rule(character, next_character, table, mode):
    encrypted_pair = ''
    first_char_index = find_index(character, table)
    second_char_index = find_index(next_character, table)
    encrypted_pair += table[(int(first_char_index[0]) + mode) % 5][int(first_char_index[1])]
    encrypted_pair += table[(int(second_char_index[0]) + mode) % 5][int(second_char_index[1])]
    return encrypted_pair


def find_index(character, table):
    row_index = -1
    line_index = 0
    for element in table:
        row_index = element.find(character)
        if row_index != -1:
            return str(line_index) + str(row_index)
        line_index += 1


def encode(my_text, key):
    my_text = encode_decode_operation(my_text, key, 1) 
    return split_by_x(my_text, 5)


def decode(my_text, key):
    my_text = my_text.replace(' ', '')
    my_text = encode_decode_operation(my_text, key, -1)
    my_text = replace_spaces(my_text, False) 
    return replace_numbers(my_text, False)


encoded_message = encode('123456789', 'Kolotoč')
print(encoded_message)
decoded_message = decode('WLRVY LXYYL IWZDL WZDRL YRRLY RDYYD RLVRR L', 'Kolotoč')
print(decoded_message)
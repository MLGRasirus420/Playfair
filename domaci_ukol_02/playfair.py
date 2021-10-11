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

def replace_spaces(my_text):
    """ Replaces spaces with XSPCX. """
    return my_text.replace(' ', 'XSPCX')

def replace_numbers(my_text):
    """Replaces numbers with abbreviations. """
    dict_numbers = {'1': 'XONX', '2': 'XTWX', '3': 'XTHX', '4': 'XFOX',
                    '5': 'XFIX', '6': 'XSIX',
                    '7': 'XSEX', '8': 'XEIX', '9': 'XNIX', '0': 'XZEX', }
    for character in my_text:
        if character in dict_numbers:
            my_text = my_text.replace(character, dict_numbers.get(character))
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
    my_text = replace_spaces(my_text)
    my_text = replace_numbers(my_text)
    my_text = remove_non_letters(my_text)
    my_text = remove_same_pairs(my_text)
    if len(my_text) % 2 != 0:
        my_text = add_end_character(my_text)
    return split_by_x(my_text, 2)

print(make_table('Kolotoč'))
print(format_input('LXXX'))


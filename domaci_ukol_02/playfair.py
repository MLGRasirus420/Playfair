from string import ascii_uppercase

def format_key(key):
    key = key.upper()
    key = remove_accents(key)
    key = replace_extra_character(key, 1)
    key = remove_duplicates(key)
    return key
    
    

def make_table(key):
    my_table = []
    


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
    alphabet = replace_extra_character(alphabet, 0)
    alphabet = remove_duplicates(alphabet)
    for character in key:
        alphabet = alphabet.replace(character, '')   
    return split_by_x(key + alphabet, 5)
           
                   
def split_by_x(my_text, x):
    """ Inserts a space character in a string after x characters. """
    return ' '.join(my_text[i:i + x] for i in range(0, len(my_text), x))


print(len(form_alphabet('AHOI')))
print(form_alphabet('AHOI'))

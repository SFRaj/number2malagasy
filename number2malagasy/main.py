"""
convert a number into Malagasy phrase
convertit un nombre en Malgache
mandika ny isa ho lasa soratra amin'ny teny Malagasy
TODO : - numbers above 9 999 999
       - write tests
       - isa misy faingo
"""
DIGIT_NAME = {'1':'iray', '2':'roa', '3':'telo', '4':'efatra', '5':'dimy',
              '6':'enina', '7':'fito', '8':'valo', '9':'sivy', '0':'aotra'}
POWER_OF_TEN = ['amby', 'folo', 'zato', 'arivo', 'alina', 'hetsy', 'tapitrisa']
DICT_COMBINATION = ({
    ('aotra', 'folo'):"", ('iray', 'folo'):'folo',
    ('roa', 'folo'):'roapolo', ('telo', 'folo'):'telopolo',
    ('efatra', 'folo'):'efapolo', ('dimy', 'folo'):'dimapolo',
    ('enina', 'folo'):'enimpolo', ('fito', 'folo'):'fitopolo',
    ('valo', 'folo'):'valopolo', ('sivy', 'folo'):'sivy folo'
})
DICT_COMBINATION.update({
    ('aotra', 'zato'):"", ('iray', 'zato'):'zato',
    ('roa', 'zato'):'roanjato', ('telo', 'zato'):'telonjato',
    ('efatra', 'zato'):'efajato', ('dimy', 'zato'):'dimanjato',
    ('enina', 'zato'):'eninjato', ('fito', 'zato'):'fitonjato',
    ('valo', 'zato'):'valonjato', ('sivy', 'zato'):'sivinjato'
})

def link(word1, word2):
    """
    manambatra ny isa sy ny tafolo miaraka aminy
    e.g link('telo', 'zato') --> 'telonjato'
    """
    if word1 == 'aotra':
        return ''
    elif word2 == 'amby':
        return word1
    elif (word1, word2) in DICT_COMBINATION:
        return DICT_COMBINATION[word1, word2]
    elif word1 == 'iray' and word2 in ['zato', 'arivo']:
        return word2
    else:
        return word1 + ' ' + word2

def digit_to_word(number):
    """
    convert each digit into the corresponding word
    e.g 291 --> ['roanjato', 'sivy folo', 'iray']
    """
    converted = []
    digits = list(str(number)) # oh: 291 --> ['2', '9', '1']
    digits.reverse()
    for i in range(len(digits)):
        digit = digits[i]
        converted += [link(DIGIT_NAME[digit], POWER_OF_TEN[i])]
    return converted

def combine(digit_words):
    """
    combines each digit word into a phrase (RECURSIVELY)
    examples:
    combine(['roa arivo', 'aotra', 'aotra', 'roa']) -> 'roa amby roa arivo' (not 'roa sy roa arivo')
    combine(['roanjato', 'aotra', 'roa']) -> 'roa amby roanjato' (not 'roa sy roa arivo')
    combine(['roanjato', 'roapolo', 'aotra']) -> 'roapolo sy roanjato' (not 'roapolo amby roanjato')
    exceptions:
    'sy zato' -> 'amby zato'
    'amby sy x arivo' -> 'amby x arivo' (e.g taona roa amby roa arivo) (when len(digit_words) == 4)
    """
    if len(digit_words) == 1:
        phrase = digit_words[0]
    elif len(digit_words) == 2:
        phrase = ''
        if digit_words[0] != '':
            phrase = digit_words[0] + ' amby ' + combine(digit_words[1:])
        else:
            phrase = combine(digit_words[1:])
        return phrase
    elif len(digit_words) > 2:
        if digit_words[-1] != '':
            if not all(p == '' for p in digit_words[1:-1]):
                phrase = combine(digit_words[:-1]) + ' sy ' + digit_words[-1]
            elif all(p == '' for p in digit_words[1:-1]):
                phrase = combine(digit_words[:-1]) + digit_words[-1]
            elif all(p == '' for p in digit_words[1:-1]) and len(digit_words) == 4:
                phrase = combine(digit_words[:-1]) + digit_words[-1]
            elif all(p == '' for p in digit_words[1:-1]) and len(digit_words) > 4:
                phrase = combine(digit_words[:-1]) + ' sy ' +  digit_words[-1]
        elif digit_words[-1] == '':
            phrase = combine(digit_words[:-1])
    phrase = phrase.replace('  ', ' ')
    phrase = phrase.replace('sy zato', 'amby zato')
    phrase = phrase.replace('iray amby', 'iraika amby')
    return phrase

def combine_reverse(digit_words):
    """
    combines each digit word into a phrase (RECURSIVELY) 
    examples:
    combine(['roa arivo', 'aotra', 'aotra', 'roa']) -> 'roa amby roa arivo' (not 'roa sy roa arivo')
    combine(['roanjato', 'aotra', 'roa']) -> 'roa amby roanjato' (not 'roa sy roa arivo')
    combine(['roanjato', 'roapolo', 'aotra']) -> 'roapolo sy roanjato' (not 'roapolo amby roanjato')
    exceptions:
    'sy zato' -> 'amby zato'
    'amby sy x arivo' -> 'amby x arivo' (e.g taona roa amby roa arivo) (when len(digit_words) == 4)
    """
    if len(digit_words) == 1:
        phrase = digit_words[0]
    elif len(digit_words) == 2:
        phrase = ''
        if digit_words[0] != '':
            phrase = combine_reverse(digit_words[1:]) + ' ' + digit_words[0] + ' amby'
        else:
            phrase = combine_reverse(digit_words[1:])
        return phrase
    elif len(digit_words) > 2:
        if digit_words[-1] != '':
            if not all(p == '' for p in digit_words[1:-1]):
                phrase = digit_words[-1] + ' sy ' + combine_reverse(digit_words[:-1])
            elif all(p == '' for p in digit_words[1:-1]):
                phrase = digit_words[-1] + ' ' + combine_reverse(digit_words[:-1])
            elif all(p == '' for p in digit_words[1:-1]) and len(digit_words) == 4:
                phrase = digit_words[-1] + ' ' + combine_reverse(digit_words[:-1])
            elif all(p == '' for p in digit_words[1:-1]) and len(digit_words) > 4:
                phrase = digit_words[-1] + ' sy ' + combine_reverse(digit_words[:-1])
        elif digit_words[-1] == '':
            phrase = combine_reverse(digit_words[:-1])
    phrase = phrase.replace('  ', ' ')
    phrase = phrase.replace('amby ', 'amby')
    phrase = phrase.replace('iray amby', 'iraika amby')
    return phrase

def write_in_malagasy(number):
    """ main function """
    return combine(digit_to_word(number)), combine_reverse(digit_to_word(number))

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        words1, words2 = write_in_malagasy(int(sys.argv[1]))
        print("Version 1: ", words1 + '\n' + "Version 2: ", words2)
        print(digit_to_word(int(sys.argv[1])))

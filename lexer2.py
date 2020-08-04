from ply import lex

keywords = (
	'T', 'F', 'PLEASE', 'EQ', 'PRINT', 'PRINTMAT', 'MO', 'NP', 'MF', 'MB', 'MR', 'ML', 'TP',
)

tokens = keywords + (
	'EQUALS', 'PLUS', 'MINUS', 'INTEGER', 'BOOLEAN', 'LPAREN', 'RPAREN',
    'COMMA', 'POINT', 'LSQPAREN', 'RSQPAREN', 'ID', 
    'NEWLINE', 'DOLLAR', 'BEGIN', 'END', 'ERROR', 'DOG', 'PIERCE',
    'WAVE', 'DOUB', 'DASH', 'PERC',
)

t_ignore = ' \t'

t_EQUALS = r'\<\-'
t_PLUS = r'\,\#'
t_MINUS = r'\,\*'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMMA = r'\,'
t_POINT = r'\.'
t_LSQPAREN = r'\['
t_RSQPAREN = r'\]'
t_DOLLAR = r'\$'
t_WAVE = r'~'
t_DOG = r'\@'
t_PERC = r'\%'
t_PIERCE = r'\.\#'
t_DOUB = r'\:'
t_DASH = r'\-'
t_BEGIN = r'\{'
t_END = r'\}'


def t_INTEGER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value is wrong %d", t.value)
        t.value = 0
    return t


def t_NEWLINE(t):
    r'\n'
    t.lexer.lineno += 1
    t.lexer.lexposition = t.lexer.lexpos
    return t

def t_ID(t):
    r'[a-zA-Z]+'
    if t.value in keywords:
        t.type = t.value
        if t.value == 'T' or t.value == 'F':
            t.type = 'BOOLEAN'
    return t

def t_ANY_error(t):
    t.type = 'ERROR'
    t.value = 4
    return t


lex.lex()

'''while True:
    lexer.input(input())

    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)'''
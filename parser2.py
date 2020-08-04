from ply import *
import lexer2

tokens = lexer2.tokens


def p_program(p):
    '''program : program statement
               | program statgroup
               | statement'''
    if len(p) == 2 and p[1]:
        p.counter = 0
        p[0] = {}
        p[0][p.counter] = p[1]
        p.counter += 1
        # print(p[0])
    elif len(p) == 3:
        p[0] = p[1]
        if not p[0]:
            p[0] = {}
        if p[2]:
            stat = p[2]
            p[0][p.counter] = stat
            p.counter += 1


def p_statgroup(p):
    'statgroup : statement'
    p[0] = ('STATGROUP', p[1])

def p_statgroup_cont(p):
    '''statgroup : statgroup statement
                 | statgroup command
                 | statgroup expression'''
    p[0] = ('STATGROUP', p[1], p[2])

def p_expression_integer(p):
    'expression : INTEGER'
    p[0] = ('INTEG', p[1])

def p_expression_boolean(p):
    'expression : BOOLEAN'
    p[0] = ('BOOL', p[1])

def p_expression_id1(p):
    'expression : COMMA INTEGER'
    p[0] = ('INT', p[2])

def p_expression_id2(p):
    'expression : POINT INTEGER'
    p[0] = ('BOOLE', p[2])

def p_expression_massiv1(p):
    'expression : COMMA INTEGER DOUB expression'
    p[0] = ('MASINT', p[2], p[4])

def p_expression_massiv2(p):
    'expression : POINT INTEGER DOUB expression'
    p[0] = ('MASBOOL', p[2], p[4])


def p_expression_binop(p):
    '''expression : PLUS expression
                  | MINUS expression'''
    p[0] = ('BINOP', p[1], p[2])

def p_expression_massiv3(p):
    'expression : COMMA INTEGER DOUB expression DASH dims'
    p[0] = ('MASINT', p[2], p[4], p[6])

def p_expression_massiv4(p):
    'expression : POINT INTEGER DOUB expression DASH dims'
    p[0] = ('MASBOOL', p[2], p[4], p[6])

def p_expression_id3(p):
    'expression : DOLLAR INTEGER'
    p[0] = ('PROC', p[2])

def p_expression_masproc(p):
    'expression : DOLLAR INTEGER DOUB expression'
    p[0] = ('MASPROC', p[2], p[4])

def p_expression_masproc1(p):
    'expression : DOLLAR INTEGER DOUB expression DASH dims'
    p[0] = ('MASPROC', p[2], p[4], p[6])

def p_command_id(p):
    'command : WAVE INTEGER'
    p[0] = ('LABEL', p[2])

def p_command_assign4(p):
    'command : COMMA INTEGER DOUB expression DASH dims EQUALS expression'
    p[0] = ('ASSINT', p[2], p[4], p[6], p[8])

def p_command_assign5(p):
    'command : POINT INTEGER DOUB expression DASH dims EQUALS expression'
    p[0] = ('ASSBOOL', p[2], p[4], p[6], p[8])

def p_relexpr(p):
    '''relexpr : expression EQ expression
               | expression MO expression
               | relexpr EQ expression
               | expression EQ NP'''
    p[0] = ('RELOP', p[1], p[2], p[3])

def p_command_print(p):
    '''command : PRINT COMMA INTEGER
               | PRINT POINT INTEGER '''
    p[0] = ('PRINT', p[3])

def p_command_printmatr(p):
    'command : PRINTMAT COMMA INTEGER'
    p[0] = ('PRINTM', p[3])
    
def p_command_proc(p):
    'command : DOLLAR INTEGER EQUALS BEGIN statgroup END'
    p[0] = ('ASSPROC', p[2], p[5])

def p_command_proc1(p):
    'command : DOLLAR INTEGER DOUB expression EQUALS BEGIN statgroup END'
    p[0] = ('ASSPROC', p[2], p[4], p[7])

def p_command_proc2(p):
    'command : DOLLAR INTEGER DOUB expression DASH dims EQUALS BEGIN statgroup END'
    p[0] = ('ASSPROC', p[2], p[4], p[6], p[9])

def p_command_proc3(p):
    'command : DOLLAR INTEGER EQUALS expression'
    p[0] = ('EQPROC', p[2], p[4])

def p_command_proc4(p):
    'command : DOLLAR INTEGER DOUB expression EQUALS expression'
    p[0] = ('EQPROC', p[2], p[4], p[6])

def p_command_proc5(p):
    'command : DOLLAR INTEGER DOUB expression DASH dims EQUALS expression'
    p[0] = ('EQPROC', p[2], p[4], p[6], p[8])

def p_dims_1(p):
    'dims : expression'
    p[0] = p[1]

def p_dims_2(p):
    '''dims : expression COMMA expression
            | dims COMMA expression'''
    p[0] = ('DIMS', p[1], p[3])

def p_dims1(p):
    '''dims : expression error expression
            | dims error expression'''
    p[0] = None
    #print('Error in ,')

def p_logic(p):
    '''logic : relexpr COMMA expression
             | expression COMMA expression
             | relexpr COMMA relexpr
             | expression COMMA relexpr
             | logic COMMA relexpr
             | logic COMMA expression'''
    p[0] = ('LOGIC', p[1], p[3])

def p_logic_error(p):
    '''logic : relexpr error expression
             | expression error expression
             | relexpr error relexpr
             | expression error relexpr
             | logic error relexpr
             | logic error expression'''
    p[0] = None
    #print('Error in ,')

def p_expression_pierce1(p):
    '''expression : PIERCE relexpr
                  | PIERCE expression'''
    p[0] = ('PIERCE', p[2])

def p_expression_pierce2(p):
    'expression : PIERCE BEGIN logic END'
    p[0] = ('PIERCES', p[3])

def p_expression_pierce2_error(p):
    'expression : PIERCE error logic END'
    p[0] = None
    #print ('Error in {')

def p_command_if1(p):
    '''command : LPAREN expression RPAREN statement
               | LPAREN relexpr RPAREN statement'''
    p[0] = ('IF', p[2], p[4])

def p_command_if2(p):
    '''command : LPAREN expression RPAREN BEGIN statgroup END
               | LPAREN relexpr RPAREN BEGIN statgroup END
               | LPAREN logic RPAREN BEGIN statgroup END'''
    p[0] = ('IF', p[2], p[5])

def p_command_if2_error(p):
    '''command : LPAREN expression error BEGIN statgroup END
               | LPAREN relexpr error BEGIN statgroup END'''
    p[0] = None
    #print('Error in )')

def p_command_np(p):
    'command : NP'
    p[0] = None

def p_command_assign(p):
    'command : COMMA INTEGER EQUALS expression'
    p[0] = ('ASSINT', p[2], p[4])

def p_command_assign1(p):
    'command : COMMA INTEGER DOUB expression EQUALS expression'
    p[0] = ('ASSINT', p[2], p[4], p[6])

def p_command_assign2(p):
    'command : POINT INTEGER EQUALS expression'
    p[0] = ('ASSBOOL', p[2], p[4])

def p_command_assign3(p):
    'command : POINT INTEGER DOUB expression EQUALS expression'
    p[0] = ('ASSBOOL', p[2], p[4], p[6])

def p_expression_ident1(p):
    '''expression : POINT INTEGER DOG expression
                  | POINT INTEGER PERC expression
                  | COMMA INTEGER DOG expression
                  | COMMA INTEGER PERC expression
                  | DOLLAR INTEGER DOG expression
                  | DOLLAR INTEGER PERC expression'''
    p[0] = ('IDENT', p[1], p[2], p[3], p[4])

def p_expression_ident2(p):
    '''expression : POINT INTEGER DOUB expression DOG expression
                  | POINT INTEGER DOUB expression PERC expression
                  | COMMA INTEGER DOUB expression DOG expression
                  | COMMA INTEGER DOUB expression PERC expression
                  | DOLLAR INTEGER DOUB expression DOG expression
                  | DOLLAR INTEGER DOUB expression PERC expression'''
    p[0] = ('IDENT', p[1], p[2], p[4], p[5], p[6])

def p_expression_ident3(p):
    '''expression : POINT INTEGER DOUB expression DASH dims DOG expression
                  | POINT INTEGER DOUB expression DASH dims PERC expression
                  | COMMA INTEGER DOUB expression DASH dims DOG expression
                  | COMMA INTEGER DOUB expression DASH dims PERC expression
                  | DOLLAR INTEGER DOUB expression DASH dims DOG expression
                  | DOLLAR INTEGER DOUB expression DASH dims PERC expression'''
    p[0] = ('IDENT', p[1], p[2], p[4], p[6], p[7], p[8])

def p_command_label(p):
    '''command : LSQPAREN LSQPAREN expression RSQPAREN RSQPAREN LSQPAREN PLEASE RSQPAREN WAVE INTEGER
               | LSQPAREN LSQPAREN relexpr RSQPAREN RSQPAREN LSQPAREN PLEASE RSQPAREN WAVE INTEGER'''
    p[0] = ('GOLABEL', p[3], p[10])

def p_command_ladel_error_1(p):
    '''command : LSQPAREN error expression RSQPAREN RSQPAREN LSQPAREN PLEASE RSQPAREN WAVE INTEGER
               | LSQPAREN error relexpr RSQPAREN RSQPAREN LSQPAREN PLEASE RSQPAREN WAVE INTEGER
               | LSQPAREN LSQPAREN expression RSQPAREN RSQPAREN error PLEASE RSQPAREN WAVE INTEGER
               | LSQPAREN LSQPAREN relexpr RSQPAREN RSQPAREN error PLEASE RSQPAREN WAVE INTEGER'''
    p[0] = None
    #print('Error in [')

def p_command_ladel_error_2(p):
    '''command : LSQPAREN LSQPAREN expression RSQPAREN error LSQPAREN PLEASE RSQPAREN WAVE INTEGER
               | LSQPAREN LSQPAREN relexpr RSQPAREN error LSQPAREN PLEASE RSQPAREN WAVE INTEGER
               | LSQPAREN LSQPAREN expression RSQPAREN RSQPAREN LSQPAREN PLEASE error WAVE INTEGER
               | LSQPAREN LSQPAREN relexpr RSQPAREN RSQPAREN LSQPAREN PLEASE error WAVE INTEGER'''
    p[0] = None
    #print('Error in ]')

def p_expression_move(p):
    '''expression : MF
                  | MB
                  | MR
                  | ML
                  | TP'''
    p[0] = ('MOVE', p[1])

def p_statement(p):
    '''statement : command NEWLINE
                 | command statement
                 | expression NEWLINE
                 | expression statement'''
    p[0] = p[1]


def p_error(t):
    # print("Syntax error at token", t.type)
    print("Syntax error at '%s' at line '%s' at pos '%s'" % (t.value, t.lexer.lineno, t.lexer.lexpos - t.lexer.lexposition))

parser = yacc.yacc()

def parse(data, debug=0):
    parser.error = 0
    p = parser.parse(data, debug=debug)
    if parser.error:
        return None
    return p
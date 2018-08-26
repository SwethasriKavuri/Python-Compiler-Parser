tokens = (
    'NAME', 'NUMBER',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS','TRUE','FALSE',
    'LPAREN', 'RPAREN','STRING','POWER','OR','AND','NOT','LESS_THAN','GREATER_THAN','LESS_EQUAL','GREATER_EQUAL','DOUBLE_EQUALS',
    'IN','FLOOR_DIVIDE','MODULUS','LSQUAREPAREN','RSQUAREPAREN','DELIMITER','NOT_EQUAL',
)
# Tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQUALS = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_POWER = r'\*\*'
t_MODULUS = r'\%'
t_GREATER_THAN = r'>'
t_GREATER_EQUAL = r'>='
t_DOUBLE_EQUALS = r'=='
t_LESS_EQUAL = r'<='
t_LESS_THAN = r'<'
t_IN = r'in'
t_NOT = r'not'
t_AND = r'and'
t_OR = r'or'
t_LSQUAREPAREN = r'\['
t_RSQUAREPAREN = r'\]'
t_DELIMITER = r','
t_TRUE = r'True'
t_FALSE = r'False'
t_NOT_EQUAL = r'<>'
t_FLOOR_DIVIDE = r'\/\/'

global error
error= False

global count
count = 0

def t_NUMBER(t):
    r'-?\d*(\d\.|\.\d)\d* | \d+'
    try:
       if '.' in t.value:
        t.value = float(t.value)
       else:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_STRING(t):
    r'([\'"](|[^\']|[^"]|"")*[\'"])'
    t.value = t.value[1:-1]
    return t

# Ignored characters
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    global error
    error = True
    global count
    count = count+1
    try:
        raise SyntaxError
    except:
            if count == 1:
                print("SYNTAX ERROR")

            else:
                count = count-1
    t.lexer.skip(1)

# Build the lexer
import ply.lex as lex

lex.lex()

# Parsing rules
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'NOT'),
    ('left', 'LESS_THAN','LESS_EQUAL','DOUBLE_EQUALS','GREATER_THAN','GREATER_EQUAL','NOT_EQUAL'),
    ('left', 'IN'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'FLOOR_DIVIDE'),
    ('left', 'MODULUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'POWER'),
    ('right', 'UMINUS'),
    ('left','LSQUAREPAREN'),
    ('left','LPAREN'),
)

# dictionary of names
names = {}

def p_statement_assign(t):
    'statement : NAME EQUALS expression'
    names[t[1]] = t[3]

def p_statement_expr(t):
    'statement : expression'
    global error
    if (not error):

        if type(t[1]) == str:
            print("'"+t[1]+"'")
        elif t[1] == None:
            pass
        else:
            print(t[1])
    else:
        error = False

def p_index_group(t):
    'expression : expression expression_index'
    try:
        t[0]=(t[1])[t[2]]
    except TypeError:
        print("%%SEMANTIC ERROR")
    except IndexError:
        print("!SEMANTIC ERROR")

def p_index_element(t):
    'expression_index : LSQUAREPAREN expression RSQUAREPAREN'
    t[0] = t[2]

def p_list(t):
    'expression : LSQUAREPAREN expression_head RSQUAREPAREN'
    t[0] = t[2]

def p_list_group_one(t):
    'expression_head : expression'
    t[0] = [t[1]]

def p_list_group_two(t):
    'expression_head : expression expression_tail'
    t[0] = t[2]
    t[0].insert(0, t[1])

def p_list_group_three(t):
    'expression_tail : DELIMITER expression expression_tail'
    t[0] = t[3]
    t[0].insert(0,t[2])

def p_list_group_four(t):
    'expression_tail :  '
    t[0] = []

def p_expression_binop(t):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression FLOOR_DIVIDE expression
                  | expression MODULUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression POWER expression
                  | expression LESS_THAN expression
                  | expression LESS_EQUAL expression
                  | expression GREATER_THAN expression
                  | expression GREATER_EQUAL expression
                  | expression DOUBLE_EQUALS expression
                  | expression IN expression
                  | NOT expression
                  | expression AND expression
                  | expression OR expression
                  | expression NOT_EQUAL expression
                  '''
    if t[2] == '+':
        try:
            t[0] = t[1] + t[3]
        except TypeError:
            print("SEMANTIC ERROR")

    elif t[2] == '-':
        try:
            t[0] = t[1] - t[3]
        except TypeError:
            print("SEMANTIC ERROR")

    elif t[2] == '*':
        try:
            t[0] = t[1] * t[3]
        except TypeError:
            print("SEMANTIC ERROR")

    elif t[2] == '/':

        try:
            t[0] = t[1] / t[3]
        except TypeError:
            print("SEMANTIC ERROR")
        except ZeroDivisionError:
            print("SEMANTIC ERROR")

    elif t[2] == '**':
        try:
            t[0] = t[1] ** t[3]
        except TypeError:
            print("SEMANTIC ERROR")

    elif t[2] == '//':
        try:
            t[0] = t[1] // t[3]
        except TypeError:
            print("SEMANTIC ERROR")
        except ZeroDivisionError:
            print("SEMANTIC ERROR")

    elif t[2] == '%':
        try:
            t[0] = t[1] % t[3]
        except TypeError:
            print("SEMANTIC ERROR")

    elif t[2] == '>':
        try:
            t[0] = t[1] > t[3]
        except TypeError:
            print("SEMANTIC ERROR")

    elif t[2] == '<':
        try:
            t[0] = t[1] < t[3]
        except TypeError:
            print("SEMANTIC ERROR")

    elif t[2] == '==':
        try:
            t[0] = t[1] == t[3]
        except TypeError:
            print("SEMANTIC ERROR")

    elif t[2] == 'in':
        try:
            t[0] = t[1] in t[3]
        except TypeError:
            print("SEMANTIC ERROR")

    elif t[1] == 'not':
        try:
            t[0] = not t[2]
        except TypeError:
            print("SEMANTIC ERROR")

    elif t[2] == 'and':
        try:
            t[0] = t[1] and t[3]
        except TypeError:
            print("SEMANTIC ERROR")

    elif t[2] == 'or':
        try:
            t[0] = t[1] or (t[3])
        except TypeError:
            print("SEMANTIC ERROR")

    elif t[2] == '>=':
        try:
            t[0] = t[1] >= t[3]
        except TypeError:
            print("SEMANTIC ERROR")

    elif t[2] == '<=':
        try:
            t[0] = t[1] <= t[3]
        except TypeError:
            print("@@SEMANTIC ERROR")

    elif t[2] == '<>':
        try:
            t[0] = t[1] != t[3]
        except TypeError:
            print("SEMANTIC ERROR")

def p_expression_uminus(t):
    'expression : MINUS expression %prec UMINUS'
    t[0] = -t[2]

def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    t[0] = t[2]

def p_expression_number(t):
    'expression : NUMBER'
    t[0] = t[1]

def p_expression_true(t):
    'expression : TRUE'
    t[0] = True

def p_expression_false(t):
    'expression : FALSE'
    t[0] = False

def p_expression_string(t):
    'expression : STRING'
    t[0] = t[1]

def p_expression_name(t):
    'expression : NAME'
    try:
        t[0] = names[t[1]]
    except LookupError:
        print("Undefined name '%s'" % t[1])
        t[0] = 0

def p_error(t):
    try:
        raise SyntaxError
    except:
        global count
        if count == 0:
            print("SYNTAX ERROR")
        else:
            pass
    global error
    error = True

import ply.yacc as yacc

yacc.yacc()

import sys
fd= open(sys.argv[1],"r")
for i in fd:
    if i.strip('\n'):
        count = 0
        lex.input(i)
        while True:
            tok = lex.token()
            if not tok:
                break
        yacc.parse(i)

names = { }

class Node:
    def __init__(self):
        print("init node")

    def evaluate(self):
        return 0

    def execute(self):
        return 0

class StringNode(Node):
    def __init__(self, v):
        self.value = str(v)
    def evaluate(self):
        return self.value

class BoolNode(Node):
    def __init__(self, v):
        self.value = bool(v)
    def evaluate(self):
        return self.value

class VariableNode(Node):
    def __init__(self, v):
        self.value = v
    def evaluate(self):
        return names[self.value]

class ListNode(Node):
    def __init__(self, v):
        self.value = v
    def evaluate(self):
        return self.value

class NumberNode(Node):

    def __init__(self, v):
        if ('.' in v):
            self.value = float(v)
        else:
            self.value = int(v)

    def evaluate(self):
        return self.value

class IndexNode(Node):

    def __init__(self,listone,index):
        self.listone = listone
        self.index =index

    def evaluate(self):
        try:
            self.value = (self.listone.evaluate())[(self.index.evaluate())]
            return self.value
        except TypeError:
            print("SEMANTIC ERROR")
        except IndexError:
            print("SEMANTIC ERROR")

    def returnList(self):
        return self.listone

    def returnIndex(self):
        return self.index


class NotNode(Node):
    def __init__(self, op, v1):
        self.v1 = v1
        self.op = op

    def evaluate(self):
        if (self.op == 'not'):
            return not self.v1.evaluate()

class BopNode(Node):
    def __init__(self, op, v1, v2):
        self.v1 = v1
        self.v2 = v2
        self.op = op

    def evaluate(self):
        if (self.op == '+'):
            try:
                return self.v1.evaluate() + self.v2.evaluate()
            except TypeError:
                    print("SEMANTIC ERROR")
        elif (self.op == '-'):
            try:
                return self.v1.evaluate() - self.v2.evaluate()
            except TypeError:
                print("SEMANTIC ERROR")
        elif (self.op == '*'):
            try:
                return self.v1.evaluate() * self.v2.evaluate()
            except TypeError:
                print("SEMANTIC ERROR")
        elif (self.op == '/'):
            try:
                return self.v1.evaluate() / self.v2.evaluate()
            except TypeError:
                print("SEMANTIC ERROR")
            except ZeroDivisionError:
                print("SEMANTIC ERROR")

        elif (self.op == '//'):
            try:
                return self.v1.evaluate() // self.v2.evaluate()
            except TypeError:
                print("SEMANTIC ERROR")
            except ZeroDivisionError:
                print("SEMANTIC ERROR")

        elif (self.op == '%'):
            try:
                return self.v1.evaluate() % self.v2.evaluate()
            except TypeError:
                print("SEMANTIC ERROR")
        elif (self.op == '>'):
            try:
                return self.v1.evaluate() > self.v2.evaluate()
            except TypeError:
                print("SEMANTIC ERROR")
        elif (self.op == '<'):
            try:
                return self.v1.evaluate() < self.v2.evaluate()
            except TypeError:
                print("SEMANTIC ERROR")
        elif (self.op == '>='):
            try:
                return self.v1.evaluate() >= self.v2.evaluate()
            except TypeError:
                print("SEMANTIC ERROR")
        elif (self.op == '<='):
            try:
                return self.v1.evaluate() <= self.v2.evaluate()
            except TypeError:
                print("SEMANTIC ERROR")
        elif (self.op == '=='):
            try:
                return self.v1.evaluate() == self.v2.evaluate()
            except TypeError:
                print("SEMANTIC ERROR")
        elif (self.op == '**'):
            try:
                return self.v1.evaluate() ** self.v2.evaluate()
            except TypeError:
                print("SEMANTIC ERROR")
        elif (self.op == '<>'):
            try:
                return self.v1.evaluate() != self.v2.evaluate()
            except TypeError:
                print("SEMANTIC ERROR")
        elif (self.op == 'and'):
            try:
                return self.v1.evaluate() and self.v2.evaluate()
            except TypeError:
                print("SEMANTIC ERROR")
        elif (self.op == 'or'):
            try:
                return self.v1.evaluate() or self.v2.evaluate()
            except TypeError:
                print("SEMANTIC ERROR")
        elif (self.op == 'in'):
            try:
                return self.v1.evaluate() in self.v2.evaluate()
            except TypeError:
                print("SEMANTIC ERROR")

class PrintNode(Node):
    def __init__(self, v):
        self.value = v

    def execute(self):
        if self.value.evaluate() == None:
            pass
        else:
         print(self.value.evaluate())
        return 0

class IfNode(Node):
    def __init__(self, v,block):
        self.condition = v
        self.block = block

    def execute(self):
        if (self.condition.evaluate()):
            self.block.execute()

class IfElseNode(Node):
    def __init__(self, v,if_block,else_block):
        self.condition = v
        self.if_block = if_block
        self.else_block = else_block

    def execute(self):
        if (self.condition.evaluate()):
            self.if_block.execute()
        else:
            self.else_block.execute()

class WhileNode(Node):
    def __init__(self, v,block):
        self.condition = v
        self.block = block

    def execute(self):
        while(self.condition.evaluate()):
            self.block.execute()


class AssignmentNode(Node):
    def __init__(self, v,e):
        self.name = v
        self.expression = e
    def execute(self):
        print(self.name,self.expression.evaluate())
        names[self.name] = self.expression.evaluate()
        return names[self.name]

class ExpressionAssignmentNode(Node):

    def __init__(self,variable,index,expression):
        self.name = variable
        self.index = index
        self.expression = expression

    def execute(self):
        names[self.name] = (self.name.evaluate())[self.index.evaluate()] = self.expression.evaluate()
        return names[self.name]


class BlockNode(Node):
    def __init__(self, s):
        if s is None:
            self.sl = []
        else:
            self.sl = [s]

    def execute(self):
        for statement in self.sl:
            statement.execute()

reserved = {
   'if' : 'IF',
   'then' : 'THEN',
   'else' : 'ELSE',
   'while' : 'WHILE',
   'for'   :  'FOR',
   'print' : 'PRINT',
   'and'   : 'AND',
   'in'   : 'IN',
   'or'   : 'OR',
   'not'  : 'NOT',
   'True' : 'TRUE',
   'False' : 'FALSE',
}

tokens = [
    'NAME', 'NUMBER','LBRACE', 'RBRACE', 'SEMI',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS',
    'LPAREN', 'RPAREN','STRING','POWER','LESS_THAN','GREATER_THAN','LESS_EQUAL','GREATER_EQUAL','DOUBLE_EQUALS',
    'FLOOR_DIVIDE','MODULUS','LSQUAREPAREN','RSQUAREPAREN','DELIMITER','NOT_EQUAL',
] + list(reserved.values())

# Tokens
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMI = r';'
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
t_LSQUAREPAREN = r'\['
t_RSQUAREPAREN = r'\]'
t_DELIMITER = r','
t_NOT_EQUAL = r'<>'
t_FLOOR_DIVIDE = r'\/\/'

def t_NUMBER(t):
    r'-?\d*(\d\.|\.\d)\d* | \d+'
    try:
        t.value = NumberNode(t.value)
        print("Hey")
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_STRING(t):
    r'([\'"](|[^\']|[^"]|"")*[\'"])'
    t.value = t.value[1:-1]
    t.value = StringNode(t.value)
    return t

# Ignored characters
t_ignore = " \t"

def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    if t.value in reserved:
        t.type = reserved[t.value]   # Check for reserved words
    return t

def t_error(t):
    print("Syntax error at '%s'" % t.value)


# Build the lexer
import ply.lex as lex

lex.lex()

# Parsing rules
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'NOT'),
    ('left', 'LESS_THAN', 'LESS_EQUAL', 'DOUBLE_EQUALS', 'GREATER_THAN', 'GREATER_EQUAL', 'NOT_EQUAL'),
    ('left', 'IN'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'FLOOR_DIVIDE'),
    ('left', 'MODULUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'POWER'),
    ('right', 'UMINUS'),
    ('left', 'LSQUAREPAREN'),
    ('left', 'LPAREN'),
    ('left', 'LBRACE'),
)


def p_block(t):
    """
    block : LBRACE inblock RBRACE
    """
    t[0] = t[2]

def p_inblock(t):
    """
    inblock : smt inblock
    """
    t[0] = t[2]
    t[0].sl.insert(0, t[1])

def p_inblock2(t):
    """
    inblock : smt
    """
    t[0] = BlockNode(t[1])

def p_stmt_main(t):
    """
    smt : block
    """
    t[0] = BlockNode(t[1])

def p_inblock3(t):
    """
    smt : LBRACE RBRACE
    """
    t[0] = BlockNode(None)

def p_inblock4(t):
    """
    block : LBRACE RBRACE
    """
    t[0] = BlockNode(None)

def p_statement_assign(t):
    'smt : NAME EQUALS expression SEMI'
    print("p_statement_assign(t)",t[3].value)
    t[0] = AssignmentNode(t[1],t[3])


def p_expression_assign(t):
    'smt : expression expression_index EQUALS expression SEMI'
    t[0] = ExpressionAssignmentNode(t[1],t[2],t[4])


def p_smt(t):
    """
    smt : print_smt
        | if_smt
        | while_smt
        | if_else_smt
    """
    t[0] = t[1]

def p_print_smt(t):
    """
    print_smt : PRINT LPAREN expression RPAREN SEMI
    """
    t[0] = PrintNode(t[3])

def p_if_smt(t):
    """
        if_smt : IF LPAREN expression RPAREN block
        """
    t[0] = IfNode(t[3],t[5])

def p_ifelse_smt(t):
    """
        if_else_smt : IF LPAREN expression RPAREN block ELSE block
        """
    t[0] = IfElseNode(t[3],t[5],t[7])

def p_while_smt(t):
    """
        while_smt : WHILE LPAREN expression RPAREN block
        """
    t[0] = WhileNode(t[3],t[5])


def p_index_group(t):
    'expression : expression expression_index'
    try:
        t[0]=IndexNode(t[1],t[2])
    except TypeError:
        print("SEMANTIC ERROR")
    except IndexError:
        print("SEMANTIC ERROR")

def p_index_element(t):
    'expression_index : LSQUAREPAREN expression RSQUAREPAREN'
    t[0] = t[2]

def p_list(t):
    'expression : LSQUAREPAREN expression_head RSQUAREPAREN'
    t[0] = ListNode(t[2])

def p_list_group_one(t):
    'expression_head : expression'
    t[0] = [t[1].evaluate()]

def p_list_group_two(t):
    'expression_head : expression expression_tail'
    t[0] = t[2]
    t[0].insert(0, t[1].evaluate())

def p_list_group_three(t):
    'expression_tail : DELIMITER expression expression_tail'
    t[0] = t[3]
    t[0].insert(0,t[2].evaluate())

def p_list_group_four(t):
    'expression_tail :  '
    t[0] = []

def p_list_group_five(t):
    'expression_head :  '
    t[0] = []

def p_expression_uminus(t):
    'expression : MINUS expression %prec UMINUS'
    t[0] = t[2]
    t[0].value = -t[0].value

def p_expression_binop(t):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression FLOOR_DIVIDE expression
                  | expression MODULUS expression
                  | expression POWER expression
                  | expression LESS_THAN expression
                  | expression LESS_EQUAL expression
                  | expression GREATER_THAN expression
                  | expression GREATER_EQUAL expression
                  | expression DOUBLE_EQUALS expression
                  | expression IN expression
                  | expression AND expression
                  | expression OR expression
                  | expression NOT_EQUAL expression
               '''
    t[0] = BopNode(t[2], t[1], t[3])

def p_NOTexpression_binop(t):
    '''expression : NOT expression'''
    t[0] = NotNode(t[1],t[2])

def p_expression_factor(t):
    '''expression : factor'''
    t[0] = t[1]

def p_factor_number(t):
    'factor : NUMBER'
    t[0] = t[1]

def p_expression_string(t):
    'expression : STRING'
    t[0] = t[1]

def p_expression_smt(t):
    'expression : smt'
    t[0] = t[1]


def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    t[0] = t[2]

def p_error(t):
    #print("SYNTAX ERROR")
    print("Syntax error at '%s'" % t.value)
def p_expression_name(t):
    'expression : NAME'
    try:
        t[0] = VariableNode(t[1])
    except LookupError:
        print("Undefined name '%s'" % t[1])
        t[0] = 0

def p_expression_true(t):
    'expression : TRUE'
    t[0] = BoolNode(True)

def p_expression_false(t):
    'expression : FALSE'
    t[0] = BoolNode(False)

import ply.yacc as yacc

yacc.yacc()

import sys

if(len(sys.argv) != 2):
    sys.exit("invalid arguments")
fd = open(sys.argv[1], 'r')
code = ""
for line in fd:
    code += line.strip('\n')
lex.input(code)
while True:
    token = lex.token()
    if not token: break
ast = yacc.parse(code)
try:
    ast.execute()
except AttributeError:
    pass


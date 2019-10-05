from .import token
tokens = token.tokens

t_DOT, t_EQL, t_LB, t_RB, t_SPL = r'\.', r'=', r'\(', r'\)', r'\,'
t_NAME = r'[a-zA-Z_]\w*'


def t_COMMENT_MUL(t):
    r'"""[^"]*"""'
    pass


def t_COMMENT_SIN(t):
    r'\#.*'
    pass


def t_DELIMS(t):
    r'\s+'
    pass


# define new line
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# define error handler
def t_error(t):
    # TODO report error
    t.lexer.skip(1)

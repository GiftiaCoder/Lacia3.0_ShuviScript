from .import token
tokens = token.tokens

# parse doc root
def p_root(p):
    'root : root root'


def p_root_node_def(p):
    'root : node_def'


# parse node
def p_node_def(p):
    'node_def : node_name EQL output_list placeholder_list method_name input_list'
    node_name = p[1]
    method_name = p[5]
    output_list = p[3]
    placeholder_list = p[4]
    input_list = p[6]
    if hasattr(p.parser, '__define_node__'):
        p.parser.__define_node__(node_name, method_name, output_list, placeholder_list, input_list)
    elif hasattr(p.parser, '__logger__'):
        p.parser.__logger__.error('__define_node__ attribute not found in parser')


# parse node name
def p_node_name(p):
    'node_name : NAME'
    p[0] = p[1]


# parse method name
def p_method_name(p):
    'method_name : NAME'
    p[0] = p[1]


# parse output_list
def p_output_list(p):
    'output_list : LB outputs RB'
    p[0] = p[2]


def p_output_list_empty(p):
    'output_list : LB RB'
    p[0] = []


def p_outputs_sin(p):
    'outputs : NAME'
    p[0] = [p[1]]


def p_outputs_mul(p):
    'outputs : outputs SPL NAME'
    p[1].append(p[3])
    p[0] = p[1]


# parse placeholder_list
def p_placeholder_list(p):
    'placeholder_list : LB placeholders RB'
    p[0] = p[2]


def p_placeholder_list_empty(p):
    'placeholder_list : LB RB'
    p[0] = []


def p_placeholders_sin(p):
    'placeholders : NAME'
    p[0] = [p[1]]


def p_placeholders_mul(p):
    'placeholders : placeholders SPL NAME'
    p[1].append(p[3])
    p[0] = p[1]


# parse input_list
def p_input_list(p):
    'input_list : LB inputs RB'
    p[0] = p[2]


def p_input_list_empty(p):
    'input_list : LB RB'
    p[0] = []


def p_inputs_sin(p):
    'inputs : input'
    p[0] = [p[1]]


def p_inputs_mul(p):
    'inputs : inputs SPL input'
    p[1].append(p[3])
    p[0] = p[1]


def p_input(p):
    'input : NAME DOT NAME'
    p[0] = [p[1], p[3]]

def purify_line(line):
    line = line.strip()
    index = line.find("//")
    if index != -1:
        line = line[0:index]
    return line


# since strings that doesn't have finishing quotes are not valid but may be valid later
# we have to define semi_strings that have only the beginning quote
def is_semi_string(token):
    if len(token) == 0:
        return False
    if token[0] != "\"": # only difference from regular check is we don't check the last quote
        return False
    banned_characters = "\n\""
    for c in token[1:-1]:
        if c in banned_characters:
            return False
    return True


def is_string_constant(token):
    if len(token) < 2:
        return False
    if token[0] != "\"" or token[-1] != "\"":
        return False
    banned_characters = "\n\""
    for c in token[1:-1]:
        if c in banned_characters:
            return False
    return True


def is_int_constant(token):
    if len(token) == 0:
        return False
    digits = "0123456789"
    for c in token:
        if c not in digits:
            return False
    return True


def is_identifier(token):
    if len(token) == 0:
        return False
    digits = "0123456789"
    characters = "0123456789" \
                 "qwertyuıopğüasdfghjklşizxcvbnmöç" \
                 "QWERTYUIOPĞÜASDFGHJKLŞİZXCVBNMÖÇ" \
                 "_"
    for character in token:
        if character not in characters:
            return False
    if token[0] in digits:
        return False
    return True


def is_token_valid(token):
    keywords = ["class", "constructor", "function", "method",
                "field", "static", "var", "int", "char", "boolean",
                "void", "true", "false", "null", "this", "let", "do",
                "if", "else", "while", "return"]
    symbols = ["{", "}", "(", ")", "[", "]", ".", ",", ";", "+", "-",
               "*", "/", "&", "|", "<", ">", "=", "~"]

    if token in keywords:
        return "KEYWORD"
    elif token in symbols:
        return "SYMBOL"
    elif is_int_constant(token):
        return "INT"
    elif is_string_constant(token):
        return "STRING"
    elif is_semi_string(token):
        return "SEMI_STRING"
    elif is_identifier(token):
        return "IDENTIFIER"
    else:
        return False


def parse(line):
    line = purify_line(line)
    tokens = []
    current_word = ""
    for letter in line:
        # if token was valid but now it became invalid, than add it to tokens
        if is_token_valid(current_word + letter):
            current_word += letter
        elif is_token_valid(current_word) not in ["SEMI_STRING", False]:
            tokens.append(current_word)
            current_word = ""
            if is_token_valid(letter):
                current_word += letter
    if is_token_valid(current_word) not in ["SEMI_STRING", False]:
        tokens.append(current_word)
        current_word = ""
    if current_word != "":
        print("not all tokens was identified")
    return tokens


def is_keyword_constant(token):
    # "true" | "false" | "null" | "this" |

    constants = ["true", "false", "null", "this"]
    if token not in constants:
        return False
    return True


def is_unary_operation(token):
    # "-" | "~"

    operations = ["-", "~"]
    if token not in operations:
        return False
    return True


def is_operation(token):
    # "+" | "-" | "*" | "/" | "&" | "<" | ">" | "="

    operations = ["+", "-", "*", "/", "&", "<", ">", "="]
    if token not in operations:
        return False
    return True


def is_term(token):
    # integer_constant | string_constant | keyword_constant

    if is_int_constant(token):
        return True

    if is_string_constant(token):
        return True

    if is_keyword_constant(token):
        return True
    return False


def is_expression(tokens):
    # term (operation term)*
    if len(tokens) < 1:
        return False

    if not is_term(tokens[0]):
        return False

    for i in range(1, len(tokens)-1, 2):
        if not is_operation(tokens[i]):
            return False
        if not is_term(tokens[i+1]):
            return False
    return True


def is_expression_list(tokens):     # NEED TEST
    # (expression ("," expression)* )?

    if tokens == []:
        return True

    expression = []     # store the current expression
    for i, token in enumerate(tokens):
        if token != ";":    # generate the expression until ; in encountered
            expression.append(token)
        else:
            if not is_expression(expression):   # if expression isn't valid return False
                return False
            expression = []                     # if it is valid reset the expression and continue


def is_subroutine_call(tokens):
    # subroutine_name"("expression_list")" | (class_name | subroutine_name) "." subroutine_name "("expression_list")"
    result = True

    if len(tokens) < 4:
        result = False

    if not is_subroutine_name(tokens[0]):
        result = False

    if tokens[1] != "(":
        result = False

    if not tokens.index(")"):
        result = False

    if not is_expression_list(tokens[2: tokens.index(")")]):
        result = False

    if tokens[-1] != ")":  # there are no left-over tokens
        result = False

    if result:              # if all previous checks are positive then return True
        return result       # otherwise check the second option

    # second option
    result = True

    if len(tokens) < 6:
        result = False

    if not (is_subroutine_name(tokens[0]) or is_class_name(tokens[0])):
        result = False

    if tokens[1] != ".":
        result = False

    if not is_subroutine_name(tokens[2]):
        result = False




def is_class_name(token):   # NOT COMPLETE
    # identifier
    # must be an identifier
    if not is_identifier(token):
        return False
    # must be defined as a class
    return True


def is_subroutine_name(token):  # NOT COMPLETE
    # identifier
    # must be an identifier
    if not is_identifier(token):
        return False
    # must be defined as a subroutine
    return True


def is_var_name(token):     # NOT COMPLETE
    # identifier
    # must be an identifier
    if not is_identifier(token):
        return False
    # must be defined as a variable
    return True


def is_type(token):
    # "int" | "char" | "boolean" | class_name

    types = ["int", "char", "boolean"]
    if token in types:
        return True

    if is_class_name(token):
        return True
    return False


def is_variable_declaration(tokens):
    # "var" type var_name ("," var_name)* ";"

    if len(tokens) < 4:
        return False

    if tokens[0] != "var":
        return False

    if not is_type(tokens[1]):
        return False

    if not is_var_name(tokens[2]):
        return False

    for i in range(3, len(tokens) - 2, 2):
        if tokens[i] != ",":
            return False
        if is_var_name(tokens[i+1]):
            return False

    if tokens[-1] != ";":
        return False


with open("examples.jack", "r") as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
        arguments = parse(line)
        print(i, arguments)

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
    if token[0] != "\"":  # only difference from regular check is we don't check the last quote
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

# (keyword, symbol, identifier, int_constant, str_constant) are pre-defined
grammer = {
    "var_name": [["identifier"], ["int_constant"]],
    "subroutine_name": [["identifier"]],
    "class_name": [["identifier"]],

    "temp1": [["var_name", "class_name"]],
    "temp2": [["var_name", "symbol:=", "int_constant"]],
    "temp3": [["temp1", "symbol:=", "temp2"]]
}


# temporarily same as is_token_valid for now
def is_primitive_token(token):
    # class_name, var_name, subroutine_name are also needs extra evaluation than their definition and might be defined
    #  as a primitive token as well, in which case identifier wouldn't be needed as a token
    primitive_tokens = ["keyword", "symbol", "identifier", "int_constant", "str_constant"]

    keywords = ["class", "constructor", "function", "method",
                "field", "static", "var", "int", "char", "boolean",
                "void", "true", "false", "null", "this", "let", "do",
                "if", "else", "while", "return"]
    symbols = ["{", "}", "(", ")", "[", "]", ".", ",", ";", "+", "-",
               "*", "/", "&", "|", "<", ">", "=", "~"]

    if token in ["keyword:"+keyword for keyword in keywords]:
        return "KEYWORD"
    elif token in ["symbol:"+symbol for symbol in symbols]:
        return "SYMBOL"
    elif token == "int_constant":
        return "INT"
    elif token == "str_constant":
        return "STRING"
    elif token == "identifier":
        return "IDENTIFIER"
    else:
        return False


def clear_definitions(definitions):
    #  input -> [[[['identifier'], ['int_constant']], [['identifier']]]]
    # output -> [["identifier", "int_constant"], ["identifier", "identifier"]]
    pass


def expend_terminal(terminal):

    # there may be different permutations of one terminal and that may cause multiple definitions for terminals
    # which include that terminal in their higher-level definition
    # each of these permutations of definitions will be stored as a list in "raw_definitions"
    raw_definitions = []

    for definition in grammer[terminal]:  # a definition of terminal
        # for each definition must be expended differently and must be appended to raw_definitions

        # final extended version of the definition will be stored in "extended_terminals" each terminal in definition
        # extends separately and as they expend they will appended one by one
        extended_terminals = []

        # an element may be a primitive token or a terminal
        for element in definition:
            if is_primitive_token(element):
                # as iterating through definition
                # if element it already primitive then append it to extended_terminals directly
                extended_terminals.append(element)
            else:
                # if element is a complex terminal than expend it through recursive call of this function
                # and append to extended_terminals
                extended_element = expend_terminal(element)
                extended_terminals.append(extended_element)

        raw_definitions.append(extended_terminals)

    # different permutations can occur while expending elements
    # they are added to extended_terminals as list of lists so they have to be expended after the process

    return raw_definitions # should be results





for terminal in grammer:
    print(expend_terminal(terminal))

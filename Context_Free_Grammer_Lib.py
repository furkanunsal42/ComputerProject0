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
        return "keyword:{}".format(token)
    elif token in symbols:
        return "symbol:{}".format(token)
    elif is_int_constant(token):
        return "int_constant"
    elif is_string_constant(token):
        return "str_constant"
    # elif is_semi_string(token):
        # return "SEMI_STRING"
    elif is_identifier(token):
        return "identifier"
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

    # for terminals that has logic operations such as (terminal | terminal2)*
    # since they are not found in grammer table just return them in their pure format
    if terminal not in grammer:
        return [[terminal]]

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

                # extended_terminals can be in three different state and each require its own action
                # 1- it can be empty
                # 2- it can be consist of only one definition
                # 3- it can consist of several definitions
                # empty:
                if not extended_terminals:
                    extended_terminals.append(element)

                else:
                    # decide between single and multiple definition
                    is_multiple_definition = False
                    for elem in extended_terminals:
                        if type(elem) == list:
                            is_multiple_definition = True

                    # single definition
                    if not is_multiple_definition:
                        extended_terminals.append(element)

                    # multiple definition
                    else:
                        for defin in extended_terminals:
                            defin.append(element)

            else:
                # if element is a complex terminal than expend it through recursive call of this function
                # and append to extended_terminals
                extended_element = expend_terminal(element)

                # duplicate extended terminal for each different definition
                # if there is more than one definition in extended element
                etx_terminal_len = len(extended_terminals)
                for i, _ in enumerate(extended_element):    # for each definition in extended element
                    if i != 0:
                        for i in range(etx_terminal_len):     # duplicate extended_terminals
                            extended_terminals.append(extended_terminals[i].copy())

                # append extended_element's altering element to each extended_terminals definition
                # since we will add element during this for loop we have to save ext_terminals' length at the begining
                ext_terminal_len = len(extended_terminals)
                for i in range(ext_terminal_len):
                    ext_elem_len = len(extended_element)
                    repeat_count = ext_terminal_len / ext_elem_len
                    # print(i)
                    # extended terminals -> 012345 (i%ext_elem_len) 012345 int(i / repeat_count)
                    # extended elements ->  012012                  001122
                    for elem in extended_element[int(i / repeat_count)]:
                        extended_terminals[i].append(elem)

                # if extended_terminals empty the above code will not function
                # so here we will instantiate extended_terminals
                if extended_terminals == []:
                    for defin in extended_element:
                        extended_terminals.append(defin.copy())

        is_ext_terminals_multi_definitional = False
        for element in extended_terminals:
            if type(element) == list:
                is_ext_terminals_multi_definitional = True
        if is_ext_terminals_multi_definitional:
            for line in extended_terminals:
                raw_definitions.append(line)
        else:
            raw_definitions.append(extended_terminals)
    # different permutations can occur while expending elements
    # they are added to extended_terminals as list of lists so they have to be expended after the process

    return raw_definitions # should be results


def display_definitions(expended_terminal):
    for definition in expended_terminal:
        print(definition)


# (keyword, symbol, identifier, int_constant, str_constant) are pre-defined
grammer = {
    "var_name": [["identifier"], ["int_constant"], ["str_constant"]],
    "subroutine_name": [["identifier"]],
    "class_name": [["identifier"]],

    "type": [["keyword:int"], ["keyword:char"], ["keyword:boolean"]],
    "var_dec": [["type", "var_name", "symbol:;"],
                ["type", "var_name", "symbol:=", "int_constant", "symbol:;"]]
}

with open("examples.jack", "r") as f:
    for terminal in grammer:
        grammer[terminal] = expend_terminal(terminal)
    lines = f.readlines()
    for line_index, line in enumerate(lines):
        tokens = parse(line)
        for i in range(len(tokens)):
            tokens[i] = is_token_valid(tokens[i])
        found = False
        for terminal in grammer:
            for definition in grammer[terminal]:
                if len(definition) != len(tokens):
                    continue
                else:
                    found = True
                    for i in range(len(tokens)):
                        if tokens[i] != definition[i]:
                            found = False
                    if found:
                        print(terminal)
                        break
        if not found:
            print("compiler error at line {}".format(line_index))
# prints parsed input
""" 
with open("examples.jack", "r") as f:
    lines = f.readlines()
    for line in lines:
        tokens = parse(line)
        for token in tokens:
            type = is_token_valid(token)
            print(type, end=" ")
        print()
"""

# prints extended version of all grammer rules
""" 
for terminal in grammer:
    print(terminal)
    display_definitions(expend_terminal(terminal))
"""
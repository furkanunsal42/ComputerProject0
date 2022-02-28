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
    elif is_semi_string(token):
        return "SEMI_STRING"
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
        return token
    elif token in ["symbol:"+symbol for symbol in symbols]:
        return token
    elif token == "int_constant":
        return token
    elif token == "str_constant":
        return token
    elif token == "identifier":
        return token
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


def extend_grammer(grammer):
    for terminal in grammer:
        grammer[terminal] = expend_terminal(terminal)
    return grammer


def is_token_valid_rule(token):
    keywords = ["class", "constructor", "function", "method",
                "field", "static", "var", "int", "char", "boolean",
                "void", "true", "false", "null", "this", "let", "do",
                "if", "else", "while", "return"]
    symbols = ["{", "}", "(", ")", "[", "]", ".", ",", ";", "+", "-",
               "*", "/", "&", "|", "<", ">", "=", "~"]
    symbols_rule = ["(", ")", "*", "|", "?"]

    if len(token) == 0:
        return False
    if token in [("keyword:"+keyword)[:len(token)] for keyword in keywords]:
        return token
    elif token in [("symbol:"+symbol)[:len(token)] for symbol in symbols]:
        return token
    elif token == "int_constant"[:len(token)]:
        return "int_constant"
    elif token == "str_constant"[:len(token)]:
        return "str_constant"
    elif token == "identifier"[:len(token)]:
        return "identifier"
    elif token in symbols_rule:
        return "grammer_symbols"
    else:
        return False


def rule_parse(line):
    line = purify_line(line)
    tokens = []
    current_word = ""
    for letter in line:
        # if token was valid but now it became invalid, than add it to tokens
        if is_token_valid_rule(current_word + letter):
            current_word += letter
        elif is_token_valid_rule(current_word):
            if current_word != "":
                tokens.append(current_word)
            current_word = ""
            if is_token_valid_rule(letter):
                current_word += letter
    if is_token_valid_rule(current_word):
        tokens.append(current_word)
        current_word = ""
    if current_word != "":
        print("not all tokens was identified")

    # (var_name | str_name)  -> ["var_name", "str_name"] type:' '
    # (var_name | str_name)? -> ["var_name", "str_name"] type:'?'
    # (var_name | str_name)* -> ["var_name", "str_name"] type:'*'

    # (var_name | (var_name|int_constant)*)? -> ["var_name", "(var_name|int_constant)*"] type:?

    parsed_rule = []
    type = 's'
    next_word = ""
    in_brackets = False
    brackets_just_ended = False
    for index, rule_token in enumerate(tokens):
        if rule_token == '(':
            if index == 0:
                continue
            in_brackets = True
            next_word += rule_token

        elif rule_token == ')':
            if index == len(tokens)-1 or (index == len(tokens)-2 and tokens[-1] in ['*', '?']):
                continue
            in_brackets = False
            brackets_just_ended = True
            next_word += rule_token

        elif in_brackets:
            next_word += rule_token

        elif brackets_just_ended:
            if rule_token in ['*', '?']:
                next_word += rule_token
            parsed_rule.append(next_word)
            next_word = ""
            brackets_just_ended = False

        elif rule_token not in ['|', '*', '?'] and not in_brackets:
            parsed_rule.append(rule_token)

        elif rule_token in ['*', '?'] and not in_brackets:
            if tokens[index-1] == ')':
                type = rule_token
            else:
                parsed_rule[-1] = "({}){}".format(parsed_rule[-1], rule_token)

    if brackets_just_ended:
        parsed_rule.append(next_word)

    return parsed_rule, type


def is_token_fits(token, rule):
    # is_fit -> does token fit the rule?
    # is_error -> is this situation an error?
    # is_force_skip -> is next token must be a different rule
    # output [is_fit, is_error, is_force_skip]

    # rule can be a single terminal or a logic expression
    # we need to parse the rule first then evaluate it

    # rule parsing *****
    parsed_rule, type = rule_parse(rule)
    print(parsed_rule)
    abstract_token = is_primitive_token(token)

    # rule is not an expression:
    if parsed_rule[0][0] != '(' and len(parsed_rule) == 1:
        # output [is_fit, is_error, is_force_skip]
        if abstract_token == is_token_valid_rule(parsed_rule[0]):
            return [True, False, True]
        else:
            return [False, True, True]

    # rule is an expression:
    else:
        is_fit = False
        for option in parsed_rule:
            # even if one option in rule fits then is_fit is true
            if is_token_fits(token, option)[0]:
                is_fit = True

        if type == '*':

            # fit   error  skip  / fit    error skip
            # true, false, false / false, true, true
            is_error = False
            is_force_skip = not is_fit
            return[is_fit, is_error, is_force_skip]

        elif type == '?':

            # fit   error  skip  / fit    error skip
            # true, false, true / false, true, true
            is_error = False
            is_force_skip = True
            return[is_fit, is_error, is_force_skip]

        elif type == "s":

            # fit   error  skip  / fit    error skip
            # true, false, true / false, true, true
            is_error = not is_fit
            is_force_skip = True
            return[is_fit, is_error, is_force_skip]




def identify_token_group(tokens):
    # this function identifies the terminal of given group of tokens
    # input: int name = 12; -> output: var_dec

    abstract_tokens = []
    for token in tokens:
        abstract_tokens.append(is_token_valid(token))

    for terminal in grammer:
        for definition in grammer[terminal]:
            # for each definition for each terminal in grammer
            # ignore all definitions whose length do not match
            if len(definition) != len(abstract_tokens):
                continue
            else:
                # if length are matching compare the definition and group
                found = True
                for i in range(len(abstract_tokens)):
                    if abstract_tokens[i] != definition[i]:
                        found = False
                if found:
                    # if all elements are matching than return terminal
                    return terminal

    # if nothing found return none
    return None


# (keyword, symbol, identifier, int_constant, str_constant) are pre-defined
grammer = {
    "blank_line": [[]],
    "var_name": [["identifier"], ["int_constant"], ["str_constant"]],
    "subroutine_name": [["identifier"]],
    "class_name": [["identifier"]],

    "type": [["keyword:int"], ["keyword:char"], ["keyword:boolean"]],
    "value": [["keyword:true"], ["keyword:false"], ["int_constant"], ["str_constant"], ["keyword:null"]],

    "var_dec": [["type", "var_name", "symbol:;"],
                ["type", "var_name", "symbol:=", "value", "symbol:;"]]
}

result = is_token_fits("keyword:int", "(keyword:int|int_constant)")
print(result)

with open("examples.jack", "r") as f:
    grammer = extend_grammer(grammer)
    lines = f.readlines()
    for line_index, line in enumerate(lines):
        tokens = parse(line)
        terminal = identify_token_group(tokens)
        if not terminal:
            print("compiler error at line " + str(line_index))
        else:
            print(terminal)

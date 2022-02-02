import sys


def purify_line(line):
    line = line.strip()
    index = line.find("//")
    if index != -1:
        line = line[0:index]
    return line


def parse_line(line):
    line = purify_line(line)
    arguments = []
    current_word = ""
    for letter in line:
        if letter != " " and letter != "\n" and letter != "\t":
            current_word += letter
        else:
            if current_word != "":
                arguments.append(current_word)
                current_word = ""
    if current_word != "":
        arguments.append(current_word)
    return arguments


def command_type(line):
    type = parse_line(line)[0]
    arithmetic_operations = ["add", "sub", "neg", "eq", "gt", "lt", "and",
                             "or", "not"]

    if type in arithmetic_operations:
        return "C_ARITHMETIC"
    elif type == "pop":
        return "C_POP"
    elif type == "push":
        return "C_PUSH"
    elif type == "label":
        return "C_LABEL"
    elif type == "goto":
        return "C_GOTO"
    elif type == "if-goto":
        return "C_IF"
    elif type == "function":
        return "C_FUNCTION"
    elif type == "return":
        return "C_RETURN"
    elif type == "call":
        return "C_CALL"
    raise Exception("Illegal Command Type")


def write_push(arguments):
    #   get data to D register  // changes depending on segment (argument[1])
    #   set A register to SP and increment by 1     // always constant
    #   set M to D                                  // always constant

    segment = arguments[1]
    value = arguments[2]
    code = ""
    # get data to D register
    if segment == "constant":
        code += "@" + str(value) + "\n"  # set A register to constant
        code += "D = A\n"  # set D to A
        code += "@SP\n"
        code += "AM = M + 1\n"  # go to top of the stack and update SP
        code += "M = D\n"  # set it to new value

    elif segment == "argument" or segment == "local" or segment == "this" or segment == "that":
        if segment == "argument":
            code += "@ARG\n"  # set A to ARG (where arguments are located)
        elif segment == "local":
            code += "@LCL\n"  # set A to LCL (where local variables are located)
        elif segment == "this":
            code += "@THIS\n"  # set A to THIS
        elif segment == "that":
            code += "@THAT\n"  # set A to THAT
        code += "D = M\n"

        if value == "0":  # if value == 0 no need to incrementation
            pass
        elif value == "1":  # increment by one if value == 1
            code += "D = D + 1\n"
        elif value.isdigit():  # add value and ARG if value > 1
            code += "@" + value + "\n"
            code += "D = D + A\n"

        code += "A = D\n"  # set A to argument location
        code += "D = M\n"  # set D to argument's value

        code += "@SP\n"
        code += "AM = M + 1\n"  # go to top of the stack and update SP
        code += "M = D\n"  # set it to new value

    elif segment == "pointer":
        if int(value) == 0:
            code += "@3\n"  # set A to 3 (THIS)
        elif int(value) == 1:
            code += "@4\n"  # set A to 4 (THAT)
        else:
            raise Exception("value cannot be greater than 1 for pointer segment")

        code += "D = M\n"
        code += "@SP\n"
        code += "AM = M + 1\n"  # go to top of the stack and update SP
        code += "M = D\n"  # set it to new value

    elif segment == "static":
        if int(value) > 255 - 16 or int(value) < 0:
            raise Exception("static variables must be between 16-239 range")

        code += "@{}\n".format(16 + int(value)) # go to static address
        code += "D = M\n"                       # remember static value

        code += "@SP\n"
        code += "AM = M + 1\n"
        code += "M = D\n"                       # push value to stack

    else:
        raise Exception("illegal segment")

    return code


def write_pop(arguments):
    segment_keywords = {"argument": "ARG",
                        "local": "LCL",
                        "this": "THIS",
                        "that": "THAT"}
    #   increment and store new address (if value > 1)

    #   update SP address
    #   get the topmost value of stack

    #   remember the incremented address (if value > 1)
    #   go to address
    #   increment address by 1 (if value == 1)
    #   set address to stack value

    segment = arguments[1]
    value = arguments[2]
    code = ""

    if segment == "argument" or segment == "local" or segment == "this" or segment == "that":

        if int(value) > 1:
            code += "@" + str(value) + "\n"
            code += "D = A\n"
            code += "@" + segment_keywords[segment] + "\n"
            code += "D = M + D\n"  # calculate saving address

            code += "@R13\n"
            code += "M = D\n"  # remember saving address at R13

        code += "@SP\n"  # go to top of the state
        code += "M = M - 1\n"  # update SP
        code += "A = M + 1\n"  # go to top of the stack
        code += "D = M\n"  # get the value of stack
        code += "M = 0\n"  # set removed data in stack to 0

        if int(value) <= 1:
            code += "@" + segment_keywords[segment] + "\n"
            if int(value) == 0:
                code += "A = M\n"  # go to the address
            if int(value) == 1:
                code += "A = M + 1\n"  # increment by one if value == 1
            code += "M = D\n"  # set address's value to stack's value

        elif int(value) > 1:
            code += "@R13\n"
            code += "A = M\n"  # remember saved address
            code += "M = D\n"  # update it

    elif segment == "pointer":
        if int(value) > 1:
            raise Exception("value of pointer cannot be larger than 1")

        code += "@SP\n"  # go to top of the state
        code += "M = M - 1\n"  # update SP
        code += "A = M + 1\n"  # go to top of the stack
        code += "D = M\n"  # get the value of stack
        code += "M = 0\n"  # set removed data in stack to 0

        if int(value) == 0:
            code += "@3\n"  # go to pointer of THIS
        if int(value) == 1:
            code += "@4\n"  # go to pointer of THAT

        if int(value) == 0:
            code += "A = M\n"  # go to the address
        if int(value) == 1:
            code += "A = M + 1\n"  # increment by one if value == 1
        code += "M = D\n"  # set address's value to stack's value

    elif segment == "static":

        if int(value) > 255 - 16 or int(value) < 0:
            raise Exception("static variables must be between 16-239 range")

        code += "@SP\n"
        code += "M = M - 1\n"
        code += "A = M + 1\n"
        code += "D = M\n"
        code += "M = 0\n"                               # pop stack value

        code += "@{}\n".format(str(int(value) + 16))    # go to static address
        code += "M = D\n"                               # set it to stack value

    else:
        raise Exception("illegal segment")

    return code


last_defined_functions_name = ""

jump_counter = {"eq": 0,
                "lt": 0,
                "gt": 0,
                "call": 0,
                "function_end": 0}


def write_arithmetic(arguments):
    type = arguments[0]
    code = ""

    if type == "add" or type == "sub" or type == "and" or type == "or":
        code += "@SP\n"
        code += "M = M - 1\n"  # update the SP value
        code += "A = M + 1\n"  # go to top of the stack
        code += "D = M\n"  # remember the topmost value
        code += "M = 0\n"  # erase the top value
        code += "A = A - 1\n"  # go to previous value
        if type == "add":
            code += "M = M + D\n"
        elif type == "sub":
            code += "M = M - D\n"
        elif type == "and":
            code += "M = M&D\n"
        elif type == "or":
            code += "M = M|D\n"  # change the previous value to sum

    elif type == "not" or type == "neg":

        code += "@SP\n"
        code += "A = M\n"  # go to stack
        if type == "not":
            code += "M = !M\n"  # invert it
        if type == "neg":
            code += "M = !M\n"
            code += "M = M + 1\n"
    elif type == "eq" or type == "lt" or type == "gt":
        code += "@SP\n"
        code += "M = M - 1\n"  # update the SP value            |
        code += "A = M + 1\n"  # go to top of the stack         |
        code += "D = M\n"  # remember the topmost value         |   -> same with other binary operations
        code += "M = 0\n"  # erase the top value                |
        code += "A = A - 1\n"  # go to previous value           |

        code += "D = M - D\n"  # calculate the difference between bottom and top stack (bottom - top)
        code += "@" + type.upper() + ".IF." + str(jump_counter[type]) + "\n"
        if type == "eq":
            code += "D;JEQ\n"
        elif type == "gt":
            code += "D;JGT\n"
        elif type == "lt":
            code += "D;JLT\n"   # jump to space 0 if condition is met
        #                         ------ if condition failed --------
        code += "@SP\n"
        code += "A = M\n"   # go to stack
        code += "M = 0\n"   # set it to false
        code += "@" + type.upper() + ".IF." + str(jump_counter[type] + 1) + "\n"
        code += "0;JMP\n"   # skip to space 1
        #                      --------- if condition succeed --------
        code += "(" + type.upper() + ".IF." + str(jump_counter[type]) + ")\n"     # space 0
        code += "@SP\n"
        code += "A = M\n"   # go to stack
        code += "M = -1\n"  # set it to true
        code += "(" + type.upper() + ".IF." + str(jump_counter[type] + 1) + ")\n"  # space 1
        jump_counter[type] += 2

    else:
        raise Exception("illegal type")

    return code


def write_label(arguments):
    type = arguments[0]
    name = arguments[1]
    code = ""

    if type == "label":
        code += "({})\n".format(name)       # (name) is already implemented in assembly
    else:
        raise Exception("illegal segment")

    return code


def write_goto(arguments):
    type = arguments[0]
    name = arguments[1]
    code = ""

    if type == "goto":
        code += "@{}\n".format(name)        # set the destination
        code += "0;JMP\n"                   # jump
    else:
        raise Exception("illegal segment")

    return code


def write_if(arguments):
    type = arguments[0]
    name = arguments[1]
    code = ""

    if type == "if-goto":

        code += "@SP\n"                                   # |
        code += "M = M - 1\n"   # update SP value           |
        code += "A = M + 1\n"   # go to top of the stack    | -> same with ordinary pop operations
        code += "D = M\n"       # get the value of stack    |
        code += "M = 0\n"       # set it to zero            |

        code += "@{}\n".format(name)    # set a to destination
        code += "!D;JEQ\n"              # jump to destination if stack is anything but 0 (false)

    else:
        raise Exception("illegal segment")

    return code


def write_call(arguments):
    type = arguments[0]
    name = arguments[1]
    argument_amount = arguments[2]
    code = ""

    if type == "call":

        code += "@RETURN.ADDRESS.{}\n".format(jump_counter["call"])
        code += "D = A\n"
        code += "@SP\n"
        code += "AM = M + 1\n"
        code += "M = D\n"           # push return address

        code += "@LCL\n"
        code += "D = M\n"
        code += "@SP\n"
        code += "AM = M + 1\n"
        code += "M = D\n"           # push local address

        code += "@ARG\n"
        code += "D = M\n"
        code += "@SP\n"
        code += "AM = M + 1\n"
        code += "M = D\n"           # push argument address

        code += "@THIS\n"
        code += "D = M\n"
        code += "@SP\n"
        code += "AM = M + 1\n"
        code += "M = D\n"           # push this address

        code += "@THAT\n"
        code += "D = M\n"
        code += "@SP\n"
        code += "AM = M + 1\n"
        code += "M = D\n"           # push that address

        code += "@{}\n".format(str(int(argument_amount) + 5))
        code += "D = A\n"
        code += "@SP\n"
        code += "D = M - D\n"
        code += "@ARG\n"
        code += "M = D + 1\n"           # set ARG to SP - n - 5

        code += "@SP\n"
        code += "D = M\n"
        code += "@LCL\n"
        code += "M = D + 1\n"           # set LCL to SP

        code += "@{}\n".format(name)
        code += "0;JMP\n"           # transfer control to function
        code += "(RETURN.ADDRESS.{})\n".format(jump_counter["call"])      # set return address
        jump_counter["call"] += 1   # update return counter

    else:
        raise Exception("illegal segment")

    return code


def write_function(arguments):
    type = arguments[0]
    name = arguments[1]
    local_count = arguments[2]
    code = ""

    if type == "function":
        global last_defined_functions_name
        last_defined_functions_name = name
        code += "@FUNCTION.{}.END\n".format(name)
        code += "0;JMP\n"
        code += "({})\n".format(name)
        for _ in range(int(local_count)):
            code += "@0\n"
            code += "D = A\n"
            code += "@SP\n"
            code += "AM = M + 1\n"
            code += "M = D\n"

    else:
        raise Exception("illegal segment")

    return code


def write_return(arguments):
    type = arguments[0]
    code = ""

    if type == "return":
        code += "@LCL\n"
        code += "D = M\n"
        code += "@R14\n"
        code += "M = D\n"   # save LCL to a temp variable in R14

        code += "@5\n"
        code += "D = A\n"
        code += "@R14\n"
        code += "D = M - D\n"   # find return address
        code += "A = D\n"
        code += "D = M\n"
        code += "@R15\n"
        code += "M = D\n"       # save return address to an another temp variable at R15

        code += "@SP\n"
        code += "A = M\n"       # go to top of the stack
        code += "D = M\n"       # get the value of the stack value

        code += "@ARG\n"
        code += "A = M\n"
        code += "M = D\n"       # set argument 0 to function's return

        code += "@ARG\n"
        code += "D = M\n"

        code += "@SP\n"
        code += "M = D\n"   # set SO = ARG + 1 (not + 1 because our implementation likes to increment itself)

        code += "@R14\n"
        code += "A = M - 1\n"
        code += "D = M\n"
        code += "@THAT\n"
        code += "M = D\n"       # THAT = *(FRAME - 1)

        code += "@2\n"
        code += "D = A\n"
        code += "@R14\n"
        code += "A = M - D\n"
        code += "D = M\n"
        code += "@THIS\n"
        code += "M = D\n"       # THIS = *(FRAME - 2)

        code += "@3\n"
        code += "D = A\n"
        code += "@R14\n"
        code += "A = M - D\n"
        code += "D = M\n"
        code += "@ARG\n"
        code += "M = D\n"       # ARG = *(FRAME - 3)

        code += "@4\n"
        code += "D = A\n"
        code += "@R14\n"
        code += "A = M - D\n"
        code += "D = M\n"
        code += "@LCL\n"
        code += "M = D\n"       # LCL = *(FRAME - 4)

        code += "@R15\n"
        code += "A = M\n"
        code += "0;JMP\n"       # transfer control back to caller function

        global last_defined_functions_name
        code += "(FUNCTION.{}.END)\n".format(last_defined_functions_name)
        last_defined_functions_name = ""
    else:
        raise Exception("illegal segment")

    return code


def write_initial():
    code = ""
    code += "@255\n"
    code += "D = A\n"
    code += "@SP\n"
    code += "M = D\n"
    code += write("call main 0")
    return code


def write(line):
    arguments = parse_line(line)
    code = ""
    if arguments == []:
        return
    else:
        type = command_type(line)
        if type == "C_ARITHMETIC":
            code += write_arithmetic(arguments)
        elif type == "C_POP":
            code += write_pop(arguments)
        elif type == "C_PUSH":
            code += write_push(arguments)
        elif type == "C_LABEL":
            code += write_label(arguments)
        elif type == "C_GOTO":
            code += write_goto(arguments)
        elif type == "C_IF":
            code += write_if(arguments)
        elif type == "C_CALL":
            code += write_call(arguments)
        elif type == "C_FUNCTION":
            code += write_function(arguments)
        elif type == "C_RETURN":
            code += write_return(arguments)
        else:
            raise Exception("classification error")
    return code


code = write_initial()
with open("code.vm", "r") as f:
    lines = f.readlines()
    for e, line in enumerate(lines):
        try:
            result = write(line)
            if result is not None:
                code += result
        except Exception:
            raise Exception("error occored at line {}: ".format(e + 1) + str(sys.exc_info()[1]))

with open("code.asm", "w") as f:
    print(code)
    f.write(code)

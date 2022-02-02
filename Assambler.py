def purify_line(line):
    line = line.strip()
    index = line.find("//")
    if index != -1:
        line = line[0:index]
    return line


def clear_white_space(line):
    new_line = ""
    for character in line:
        if character != ' ' and character != '\n' and character != '\t':
            new_line += character
    return new_line


def j_instruction(line, index):
    line = purify_line(line)
    line = clear_white_space(line)
    VariableTable.table[line[1:-1]] = index


def c_instruction(line):
    #                        a123456
    alu_instuctioin = {"0": "0101010",
                       "1": "0111111",
                       "-1": "0111010",
                       "D": "0001100",
                       "A": "0110000",
                       "!D": "0001101",
                       "!A": "0110001",
                       "-D": "0001111",
                       "-A": "0110011",
                       "D+1": "0011111",
                       "1+D": "0011111",
                       "A+1": "0110111",
                       "1+A": "00110111",
                       "D-1": "0001110",
                       "A-1": "0110010",
                       "D+A": "0000010",
                       "A+D": "0000010",
                       "D-A": "0010011",
                       "A-D": "0000111",
                       "D&A": "0000000",
                       "A&D": "0000000",
                       "D|A": "0010101",
                       "A|D": "0010101",
                       "M": "1110000",
                       "!M": "1110001",
                       "-M": "1110011",
                       "M+1": "1110111",
                       "1+M": "1110111",
                       "M-1": "1110010",
                       "D+M": "1000010",
                       "M+D": "1000010",
                       "D-M": "1010011",
                       "M-D": "1000111",
                       "D&M": "1000000",
                       "M&D": "1000000",
                       "D|M": "1010101",
                       "M|D": "1010101",
                       }
    line = purify_line(line)
    #       0123456789012345
    #       111accccccdddjjj
    code = "1110000000000000"
    if line.find("=") != -1:
        index = line.find("=")

        target = clear_white_space(line[0:index])
        if 'A' in target:
            code = code[0:10] + '1' + code[11::]
        if 'D' in target:
            code = code[0:11] + '1' + code[12::]
        if 'M' in target:
            code = code[0:12] + '1' + code[13::]

        source = clear_white_space(line[index+1::])
        if source not in alu_instuctioin:
            print("illegal alu expression")
            return None
        code = code[0:3] + alu_instuctioin[source] + code[10::]
    elif line.find(';') != -1:
        jump_codes = {"JGT": "001",
                      "JEQ": "010",
                      "JGE": "011",
                      "JLT": "100",
                      "JNE": "101",
                      "JLE": "110",
                      "JMP": "111",
                    }

        index = line.find(";")

        condition = clear_white_space(line[0:index])
        operation = clear_white_space(line[index+1::])

        code = code[0:3] + alu_instuctioin[condition] + code[10::]
        code = code[0:13] + jump_codes[operation]

    return code


def a_instruction(line):
    line = purify_line(line)
    if line[0] != '@':
        print("use @ for A-instructions")
        return None
    data = line[1::]
    if not data.isdigit():
        data = VariableTable.get_variable(data)
    code = '0' + bin(int(data))[2::].zfill(15)
    return code


class VariableTable:
    table = {"SCREEN": 16384,
             "KBD": 24576,
             "SP": 0,
             "LCL": 1,
             "ARG": 2,
             "THIS": 3,
             "THAT": 4,
             }
    for x in range(16):
        table['R' + str(x)] = x
    variable_count = 0

    @staticmethod
    def get_variable(name):
        if name not in VariableTable.table:
            VariableTable.table[name] = VariableTable.variable_count + 16
            VariableTable.variable_count += 1
        return VariableTable.table[name]


output = []
with open("code.asm") as f:
    lines = f.readlines()
    line_count = 0
    for line in lines:
        if purify_line(line) == "":
            continue
        elif purify_line(line)[0] == '(' and purify_line(line)[-1] == ')':
            j_instruction(line, line_count)
        else:
            line_count += 1

    line_count = 0
    for line in lines:
        if purify_line(line) == "":
            continue
        elif purify_line(line)[0] == "@":
            output.append(a_instruction(line))
            print(a_instruction(line))
            line_count += 1
        elif purify_line(line)[0] == '(' and purify_line(line)[-1] == ')':
            continue
        else:
            output.append(c_instruction(line))
            print(c_instruction(line))
            line_count += 1


with open("code.hack", "w") as f:
    for line in output:
        f.writelines(line + '\n')

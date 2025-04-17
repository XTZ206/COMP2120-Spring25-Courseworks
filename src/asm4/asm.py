import sys


def get_opcode_field(opcode: str) -> str:
    opcodes = {"ADD": "00", "SUB": "01", "NOT": "02",
               "AND": "03", "OR": "04", "MOV": "05",
               "LD": "06", "ST": "07", "BR": "08",
               "BZ": "08", "BNZ": "08", "HLT": "09",
               "PUSH": "0a", "POP": "0b",
               "CALL": "0c", "RET": "0d",
               ".WORD": ""}

    if opcode not in opcodes:
        raise ValueError(f"{opcode} is not a valid opcode")

    return opcodes[opcode]


def get_register_field(operand: str) -> str:
    if not operand.startswith("R"):
        raise ValueError(f"{operand} not a valid register")
    reg_num = int(operand[1:])
    return hex(reg_num)[2:].rjust(2, '0')


def get_label_field(operand: str, labels: dict[str, int]) -> str:
    if operand not in labels:
        raise ValueError(f"{operand} not a valid label")
    return hex(labels[operand])[2:].rjust(8, '0')


def get_data_field(operand: str) -> str:
    return operand.lower().rjust(8, '0')


def compile(assembles: list[str]):
    address: int = 0
    labels: dict[str, int] = {}

    # store the label addresses first
    for assemble in assembles:
        assemble: str = assemble.ljust(24)
        label: str = assemble[0:4].strip().rstrip(':')
        opcode: str = assemble[4:12].strip()

        if label != "":
            labels[label] = address

        # one-word instructions
        if opcode in ("ADD", "SUB", "NOT", "AND", "MOV", "HLT", "PUSH", "POP", "RET"):
            address += 4

        # double-word instructions
        elif opcode in ("LD", "ST", "BR", "BZ", "BNZ", "CALL"):
            address += 8

        # data
        elif opcode in (".WORD",):
            address += 4

        else:
            raise ValueError(f"Unknown Opcode: {opcode}")

    # generate actual instructions
    for assemble in assembles:
        assemble: str = assemble.ljust(24)
        opcode: str = assemble[4:12].strip()
        operands: list[str] = assemble[12:24].strip().split(',')

        if opcode in ("ADD", "SUB", "AND", "OR"):
            # operand R R R
            yield get_opcode_field(opcode) + "".join(map(get_register_field, operands))

        elif opcode in ("NOT", "MOV"):
            # operand R N R
            yield get_opcode_field(opcode) + \
                get_register_field(operands[0]) + "00" + \
                get_register_field(operands[1])

        elif opcode in ("LD",):
            # operand L R
            yield get_opcode_field(opcode) + "00ff" + get_register_field(operands[1])
            yield get_label_field(operands[0], labels)

        elif opcode in ("ST",):
            # operand R L
            yield get_opcode_field(opcode) + get_register_field(operands[0]) + "ff00"
            yield get_label_field(operands[1], labels)

        elif opcode in ("BR", "BZ", "BNZ", "CALL"):
            # operand L
            yield get_opcode_field(opcode) + {"BR": "00", "BZ": "01", "BNZ": "02", "CALL": "00"}[opcode] + "ff00"
            yield get_label_field(operands[0], labels)

        elif opcode in ("PUSH",):
            # operand R N N
            yield get_opcode_field(opcode) + get_register_field(operands[0]) + "0000"

        elif opcode in ("POP", ):
            # operand N N R
            yield get_opcode_field(opcode) + "0000" + get_register_field(operands[0])

        elif opcode in ("HLT", "RET"):
            # operand N
            yield get_opcode_field(opcode) + "000000"

        elif opcode in (".WORD"):
            # operand data
            if len(operands) == 0:
                yield get_data_field("")
            else:
                yield get_data_field(operands[0])

        else:
            raise ValueError(f"Unknown Opcode: {opcode}")

    return


def main():

    argc = len(sys.argv)
    if (argc == 1):
        print("usage: python3 asm.py <input filepath> -o <output filepath>")
        return

    if sys.argv[1].endswith(".asm"):

        if argc == 2:
            with open(sys.argv[1], 'r') as fin:
                result = compile(fin.readlines())
            print("assemble output: ")
            print(result)

        elif argc >= 4 and sys.argv[2] == "-o":
            with open(sys.argv[1], 'r') as fin:
                result = compile(fin.readlines())

            with open(sys.argv[3], 'w') as fout:
                fout.writelines(l + '\r\n' for l in result)

    else:
        print("usage: python3 asm.py <input filepath> -o <output filepath>")
        return


main()

#! /usr/bin/python3
import sys 


# read_number()
# read input number and convert it to a numeric value.
#
# |line|: input string
# |index|: the index of |line|, which indicates the start of the number to be read
# Return value: token of the number, and the next index of |line| to read
def read_number(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        decimal = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * decimal
            decimal /= 10
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index


# read_plus() ~ read_divide()
# read input sign and convert it to a token.
#
# |line|: input string
# |index|: the index of |line|, which indicates the start of the number to be read
# Return value: token of the number, and the next index of |line| to read
def read_plus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1


def read_minus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1


def read_multiply(line, index):
    token = {'type': 'MULTIPLY'}
    return token, index + 1


def read_divide(line, index):
    token = {'type': 'DIVIDE'}
    return token, index + 1


def read_bracket_open(line, index):
    token = {'type': 'BRACKET_OPEN'}
    return token, index + 1


def read_bracket_close(line, index):
    token = {'type': 'BRACKET_CLOSE'}
    return token, index + 1


# tokenize()
# read input and convert it to a list of tokens.
#
# |line|: input string
# Return value: list of tokens
def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = read_number(line, index)
        elif line[index] == '+':
            (token, index) = read_plus(line, index)
        elif line[index] == '-':
            (token, index) = read_minus(line, index)
        elif line[index] == '*':
            (token, index) = read_multiply(line, index)
        elif line[index] == '/':
            (token, index) = read_divide(line, index)
        elif line[index] == '(':
            (token, index) = read_bracket_open(line, index)
        elif line[index] == ')':
            (token, index) = read_bracket_close(line, index)
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens

# convert()
# convert infix to postfix.
#
# |tokens|: list of tokens
# Return value: list of converted tokens
def convert(tokens):
    # list of converted tokens
    result = []
    # list of operators
    operators = []
    # priority of operators
    priority = {
        "PLUS": 1,
        "MINUS": 1,
        "MULTIPLY": 2,
        "DIVIDE": 2,
        "BRACKET_OPEN": 0,
        "BRACKET_CLOSE": 0
    }
    for token in tokens:
        if token['type'] in ("PLUS", "MINUS", "MULTIPLY", "DIVIDE","BRACKET_OPEN","BRACKET_CLOSE"):
            if operators and token['type'] == "BRACKET_OPEN":
                operators.append(token)
                continue
            # if operator is ), pop operators until found (
            elif token['type'] == 'BRACKET_CLOSE':
                while operators and operators[-1]['type'] != "BRACKET_OPEN":
                    result.append(operators.pop())
                # pop )'s pair (
                operators.pop()
                continue
            # pop operators until found operator with lower priority
            elif operators and priority[operators[-1]['type']] > priority[token['type']]:
                while operators:
                    result.append(operators.pop())
            operators.append(token)
        # if number, append it to result
        else:
            result.append(token)
    # append the rest of operators to result (reverse order)
    while operators:
        result.append(operators.pop())

    return result


# evaluate()
# evaluate the list of tokens and return the calculated value.
#
# |tokens|: list of tokens
# Return value: calculated value
def evaluate(tokens):
    # convert infix to postfix
    tokens = convert(tokens)
    answer = []
    index = 0
    while index < len(tokens):
        if tokens[index]['type'] == 'PLUS':
            right = answer.pop()
            left = answer.pop()
            answer.append(left + right)
        elif tokens[index]['type'] == 'MINUS':
            right = answer.pop()
            left = answer.pop()
            answer.append(left - right)
        elif tokens[index]['type'] == 'MULTIPLY':
            right = answer.pop()
            left = answer.pop()
            answer.append(left * right)
        elif tokens[index]['type'] == 'DIVIDE':
            right = answer.pop()
            left = answer.pop()
            answer.append(left / right)
        else:
            answer.append(tokens[index]['number'])
        index += 1
    return answer.pop()


def test(line):
    tokens = tokenize(line)
    actual_answer = evaluate(tokens)
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8: 
        print('\033[32m' +"PASS!" + '\033[0m' +"(%s = %f)" % (line, expected_answer))
    else:
        print('\033[31m' + "FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer) + '\033[0m') #color red


# Add more tests to this function :)
def run_test():
    print("==== Test started! ====")
    # normal
    test("1+2")
    test("1.0+2.1-3")
    test("3.0+4*2-1/5")
    # only a number
    print("-----only a number-----")
    test("1")
    #! test("-1")
    test("2147483647")
    # only integer
    print("-----only integer-----")
    test("1+2")
    test("1-2")
    test("1*2")
    test("1/2")
    # float and integer
    print("-----float and integer-----")
    test("1.0+2")
    test("1.0-2")
    test("1.0*2")
    test("1.0/2")
    # only float
    print("-----only float-----")
    test("1.0+2.1")
    test("1.0-2.1")
    test("1.0*2.1")
    test("1.0/2.1")
    # negative number and positiv number
    print("-----negative number and positive number-----")
    #!test("-1+2")
    #!test("-1-2")
    #!test("-1*2")
    #!test("-1/2")
    #!test("1*-2")
    #!test("1/-2")
    # only negative number
    print("-----only negative number-----")
    #!test("-1*-2")
    #!test("-1/-2")
    # include 0
    print("-----include 0-----")
    test("0+1")
    test("0-1")
    test("0*1")
    test("0/1")
    # mix
    print("-----mix------")
    test("1+2*3")
    test("1-2*3")
    test("1*2*3")
    test("1/2/3")
    test("1/3+2/3")
    test("4+2-3.0*4/2.1")
    test("4.5-2*3.0")
    test("6.2+2/4.5")
    test("4.8+2.1*3-1.3")
    test("6.6/3.2+1.7-2.5")
    test("2.4+3.7*4.2-6.5/2.8")
    # boundary value
    print("-----boundary value-----")
    test(f"{sys.maxsize}+1")
    test(f"{sys.maxsize}-1")

    # bracket
    print("-----bracket-----")
    test("(1+2)*3")
    test("1*(2+3)")
    test("(1+2)*(3+4)")
    test("9*(8+7)-6/3+(21+2)")
    test("1+2*(3+4*(5+6))")
    test("9*(8+7)-(6-(5+4)/3)*21")
    test("(3.0+4*(2-1))/5")
    print("==== Test finished! ====\n")

run_test()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)

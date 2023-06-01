#! /usr/bin/python3
import sys

# read_number()
# read input number and convert it to a numeric value.
#
# |line|: input string
# |index|: the index of |line|, which indicates the start of the number to be read
# |tokens|: list of tokens
# Return value: token of the number, and the next index of |line| to read
def read_number(line, index, tokens):
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
    # if before the number there is a minus sign, then make the number negative
    if tokens and tokens[-1]['type'] == 'MINUS':
        number *= -1
        #if the number is to be multiplied/divided, then delete the minus sign (to calculate expressions like n *-1 or n/-1)
        # e.g. 1*-1
        # before [{'type': 'NUMBER', 'number': 1},  {'type': 'MULTIPLY'}, {'type': 'MINUS'}, {'type': 'NUMBER', 'number': 1}]
        # after [{'type': 'NUMBER', 'number': 1}, {'type': 'MULTIPLY'}, {'type': 'NUMBER', 'number': -1}]
        if len(tokens) > 2 and (tokens[-2]['type'] == 'MULTIPLY' or tokens[-2]['type'] == 'DIVIDE'):
            tokens.pop()
        #if the number is to be added/subtracted, then change the operator to plus
        # e.g. 1-1 => 1+(-1)
        # before [{'type': 'NUMBER', 'number': 1},   {'type': 'MINUS'}, {'type': 'NUMBER', 'number': 1}]
        # after [{'type': 'NUMBER', 'number': 1}, {'type': 'PLUS'},  {'type': 'NUMBER', 'number': -1}]
        else:
            tokens[-1]['type'] = 'PLUS'
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
            (token, index) = read_number(line, index,tokens)
        elif line[index] == '+':
            (token, index) = read_plus(line, index)
        elif line[index] == '-':
            (token, index) = read_minus(line, index)
        elif line[index] == '*':
            (token, index) = read_multiply(line, index)
        elif line[index] == '/':
            (token, index) = read_divide(line, index)
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    return tokens


# evaluate_multiply_divide()
# evaluate MULTIPLY and DIVIDE in the list of tokens and update the list.
#
# |tokens|: list of tokens
# Return value: None
def evaluate_multiply_divide(tokens):
    temp = 0
    index = 1
    # Caluculate '*' and '/'
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            # if operator is '+' or '-', just skip
            if tokens[index-1]['type'] == 'PLUS' or tokens[index-1]['type'] == 'MINUS':
                index += 1
                continue
            # if operator is '*' or '/'
            elif tokens[index -1]['type'] == 'MULTIPLY' or tokens[index -1]['type'] == 'DIVIDE':
                left = tokens[index - 2]['number']
                right = tokens[index]['number']
                if tokens[index - 1]['type'] == 'MULTIPLY':
                    temp = left * right
                else:
                    temp = left / right
                tokens[index - 2]['number'] = temp
                del tokens[index - 1:index + 1]
            else:
                print('Invalid syntax: '+str(tokens[index - 1]['type']))
                exit(1)
        else:
            index += 1


# evaluate_plus_minus()
# evaluate PLUS and MINUS in the list of tokens and update the list.
#
# |tokens|: list of tokens
# Return value: None
def evaluate_plus_minus(tokens):
    answer = 0
    index = 1
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            # keep MINUS to handle expressions with bracket like 1-(3+2)
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']
            else:
                print('Invalid syntax: '+str(tokens[index - 1]['type']))
                exit(1)
        index += 1
    return answer


# evaluate()
# evaluate the list of tokens and return the calculated value.
#
# |tokens|: list of tokens
# Return value: calculated value
def evaluate(tokens):
    # Caluculate '*' and '/' first
    evaluate_multiply_divide(tokens)
    # then Calculate '+' and '-'
    answer = evaluate_plus_minus(tokens)
    return answer


def test(line):
    tokens = tokenize(line)
    actual_answer = evaluate(tokens)
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8: # 1e-8 = 10^-8
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
    test("-1")
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
    test("-1+2")
    test("-1-2")
    test("-1*2")
    test("-1/2")
    test("1*-2")
    test("1/-2")
    # only negative number
    print("-----only negative number-----")
    test("-1*-2")
    test("-1/-2")
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
    

    print("==== Test finished! ====\n")

run_test()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)

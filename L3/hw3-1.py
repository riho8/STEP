#! /usr/bin/python3
import sys

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
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    return tokens


def evaluate_multiply_divide(tokens):
    temp = 0
    index = 1
    # Caluculate '*' and '/'
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            # if operator is '+' or '-', basicaly just skip
            if tokens[index-1]['type'] == 'PLUS' or tokens[index-1]['type'] == 'MINUS':
                # Handle division or multiplication of negative number like n * -1 or n / -1
                if tokens[index-1]['type'] == 'MINUS' and (tokens[index - 2]['type'] == 'MULTIPLY' or tokens[index - 2]['type'] == 'DIVIDE'):
                    temp = tokens[index]['number'] * -1
                    if tokens[index - 2]['type'] == 'MULTIPLY':
                        tokens[index - 3]['number'] *= temp
                    elif tokens[index - 2]['type'] == 'DIVIDE':
                        tokens[index - 3]['number'] /= temp
                    del tokens[index - 2:index + 1]
                    index += 1
                    continue
                # else (just plus or minus, skip)
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
                print('Invalid syntax')
                exit(1)
        else:
            index += 1


def evaluate_plus_minus(tokens):
    answer = 0
    index = 1
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']
            else:
                print('Invalid syntax')
                exit(1)
        index += 1
    return answer


def evaluate(tokens):
    # Caluculate '*' and '/' first
    evaluate_multiply_divide(tokens)
    # Calculate '+' and '-'
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

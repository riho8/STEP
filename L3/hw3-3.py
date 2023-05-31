#! /usr/bin/python3

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
    token = {'type': 'MALTIPLY'}
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

def read_curly_bracket_open(line, index):
    token = {'type': 'CURLY_BRACKET_OPEN'}
    return token, index + 1

def read_curly_bracket_close(line, index):
    token = {'type': 'CURLY_BRACKET_CLOSE'}
    return token, index + 1

def read_square_bracket_open(line, index):
    token = {'type': 'SQUARE_BRACKET_OPEN'}
    return token, index + 1

def read_square_bracket_close(line, index):
    token = {'type': 'SQUARE_BRACKET_CLOSE'}
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
        elif line[index] == '(':
            (token, index) = read_bracket_open(line, index)
        elif line[index] == ')':
            (token, index) = read_bracket_close(line, index)
        elif line[index] == '{':
            (token, index) = read_curly_bracket_open(line, index)
        elif line[index] == '}':
            (token, index) = read_curly_bracket_close(line, index)
        elif line[index] == '[':
            (token, index) = read_square_bracket_open(line, index)
        elif line[index] == ']':
            (token, index) = read_square_bracket_close(line, index)
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
                if tokens[index-1]['type'] == 'MINUS' and (tokens[index - 2]['type'] == 'MALTIPLY' or tokens[index - 2]['type'] == 'DIVIDE'):
                    temp = tokens[index]['number'] * -1
                    if tokens[index - 2]['type'] == 'MALTIPLY':
                        tokens[index - 3]['number'] *= temp
                    elif tokens[index - 2]['type'] == 'DIVIDE':
                        tokens[index - 3]['number'] /= temp
                    tokens.pop(index)
                    tokens.pop(index-1)
                    tokens.pop(index-2)
                    index += 1
                    continue
                # else (just plus or minus, skip)
                index += 1
                continue
            # if operator is '*' or '/'
            elif tokens[index -1]['type'] == 'MALTIPLY' or tokens[index -1]['type'] == 'DIVIDE':
                if tokens[index - 1]['type'] == 'MALTIPLY':
                    temp = tokens[index - 2]['number'] * tokens[index]['number']
                else:
                    temp = tokens[index - 2]['number'] / tokens[index]['number']
                tokens[index - 2]['number'] = temp
                tokens.pop(index)
                tokens.pop(index-1)
                index -= 1
            else:
                print('Invalid syntax')
                exit(1)
        index += 1

def evaluate_plus_minus(tokens):
    answer = 0
    index = 1
    # Calculate '+' and '-'
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

def evaluate_without_bracket(tokens):
    evaluate_multiply_divide(tokens)
    answer = evaluate_plus_minus(tokens)
    return answer

def evaluate(tokens):
    evaluate_bracket(tokens)
    evaluate_multiply_divide(tokens)
    answer = evaluate_plus_minus(tokens)
    return answer

def evaluate_bracket(tokens):
    index = 0
    while index < len(tokens):
        # print(tokens)
        if tokens[index]['type'] == 'BRACKET_OPEN' or tokens[index]['type'] == 'CURLY_BRACKET_OPEN' or tokens[index]['type'] == 'SQUARE_BRACKET_OPEN':
            if tokens[index]['type'] == 'BRACKET_OPEN':
                closing_bracket = 'BRACKET_CLOSE'
            elif tokens[index]['type'] == 'CURLY_BRACKET_OPEN':
                closing_bracket = 'CURLY_BRACKET_CLOSE'
            elif tokens[index]['type'] == 'SQUARE_BRACKET_OPEN':
                closing_bracket = 'SQUARE_BRACKET_CLOSE'
            index_open = index
            index_close = index_open + 1
            while index_close < len(tokens):
                if tokens[index_close]['type'] == closing_bracket:
                    break
                index_close += 1
            target = tokens[index_open+1:index_close]
            target.insert(0, {'type': 'PLUS'})
            answer = evaluate(target)
            # print(answer)
            tokens[index_open]['type'] = 'NUMBER'
            tokens[index_open]['number'] = answer
            del tokens[index_open+1:index_close+1]
        index += 1
    # print(tokens)
    return tokens

def test(line):
    tokens = tokenize(line)
    actual_answer = evaluate(tokens)
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8: 
        print("PASS! (%s = %f)" % (line, expected_answer))
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
    test("2147483647+1")
    test("-2147483648-1")

    # bracket
    print("-----bracket-----")
    test("(1+2)*3")
    test("1*(2+3)")
    test("(1+2)*(3+4)")
    test("9*(8+7)-6/3+(21+2)")
    
    print("==== Test finished! ====\n")

run_test()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)

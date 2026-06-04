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
    token = {'type': 'MULTIPLY'}
    return token, index + 1

def read_divide(line, index):
    token = {'type': 'DIVIDE'}
    return token, index + 1

# Add reading for (
def read_open(line, index):
    token = {'type': 'OPEN'}
    return token, index + 1

# Add reading for )
def read_close(line, index):
    token = {'type': 'CLOSE'}
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
            (token, index) = read_open(line, index)
        elif line[index] == ')':
            (token, index) = read_close(line, index)
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens

def multiply_divide_evaluate(tokens):
    answer_tokens = []
    index = 0
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            temp = tokens[index]['number']
            index += 1
            while (index < len(tokens) 
                and (tokens[index]['type'] == 'MULTIPLY' 
                or tokens[index]['type'] == 'DIVIDE')):
                if tokens[index]['type'] == 'MULTIPLY':
                    temp *= tokens[index+1]['number']
                    index += 2
                elif tokens[index]['type'] == 'DIVIDE':
                    temp /= tokens[index+1]['number']
                    index += 2
            answer_tokens.append({'type': 'NUMBER', 'number': temp})
        else:
            answer_tokens.append(tokens[index])
            index += 1
    return answer_tokens

def plus_minus_evaluate(tokens):
    answer = 0
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
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

def evaluate_basic(tokens):
    after_multiply_divide = multiply_divide_evaluate(tokens)
    answer = plus_minus_evaluate(after_multiply_divide)
    return answer

def evaluate_parentheses(tokens):
    found = True #this is true first, so the while loop can start
    while found:
        found = False
        stack = [] #save the positions of OPEN
        for i in range(len(tokens)):
            if tokens[i]['type'] == 'OPEN':
                stack.append(i)
            elif tokens[i]['type'] == 'CLOSE':
                start = stack.pop()
                inside = tokens[start + 1:i] #get only the tokens inside parentheses
                partial_answer = evaluate_basic(inside) #calculate inside parentheses
                # make new tokens:
                # before OPEN + answer inside parentheses + after CLOSE
                tokens = ( 
                    tokens[:start]
                    + [{'type': 'NUMBER', 'number': partial_answer}]
                    + tokens[i + 1:]
                )
                found = True
                break
    return tokens

# First remove all parentheses
# Then calculate the normal expression without parentheses      
def evaluate(tokens):
    tokens = evaluate_parentheses(tokens)
    return evaluate_basic(tokens)

def test(line):
    tokens = tokenize(line)
    actual_answer = evaluate(tokens)
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))


# Add more tests to this function :)
def run_test():
    print("==== Test started! ====")
    test_cases = [
        # basic plus/minus
        "1+2",
        "5-3",
        "2.0+4.0-1.0",
        # basic multiply and divide
        "2*3",
        "4/2",
        "4/3",
        "1*2*3*4*5",
        "24/3/2",
        "24/3/2/9",
        # mixed
        "1+2*3",
        "1*2+3",
        "1-2*3",
        "10/2+3",
        "1+5*3/4-5-5*3*3*3/2",
        # decimals
        "0.5+1.5",
        "1.5*2",
        "3.0/2",
        "5/3.0",
        "1.2+3.2*2",
        # mixed * and / only
        "1/2*3",
        "2*8/4",
        "100/10/2*4*6/3",
        #　parentheses
        "(1+2)",
        "2*(3+4)",
        "(2+3)*4",
        "5/(2+3)",
        "4-(2+3)",
        "1+(2*3)",
        "1+(2+3)*4",
        "2*3+(4*5)",
        "2*(3+4)/7",
        "1+(2*(3+4))",
        "((1+2)*3)",
        "100/(2*(3+2))",
        "1+(2+(3+(4+5)))",
        "(10-3)/(1+6)",
        "(2*3-4)+(4*5)",
        "(1+2)+(3+4)+(5+6)",
        "(0.5+2.5)*2",
        "1.2*(3.2+5.2)",
        "(5/2)+(3/4)",
        "9/(2.5+2.5)",
    ]

    for line in test_cases:
        test(line)

    print("==== Test finished! ====\n")

run_test()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)
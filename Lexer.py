def lexer(input):
    i = 0
    n = len(input)

    tokens = []

    if n == 0:
            raise SyntaxError("Empty Input")

    while i < n:
        char = input[i]

        if char.isdigit():
            number_str = char
            i += 1

            while i < n and input[i].isdigit():
                number_str += input[i]
                i += 1
            
            tokens.append(('NUMBER', int(number_str)))
            continue

        if char == '+':
            tokens.append(('PLUS', char))
            i += 1
            continue

        if char == '−':
            tokens.append(('MINUS', char))
            i += 1
            continue

        if char == '×':
            tokens.append(('MULT', char))
            i += 1
            continue

        if char == '=':
            tokens.append(('EQUALS', char))
            i += 1
            continue

        if char == '?':
            tokens.append(('CONDITIONAL', char))
            i += 1
            continue

        if char == 'λ':
            tokens.append(('LAMBDA', char))
            i += 1
            continue

        if char == '≜':
            tokens.append(('LET', char))
            i += 1
            continue

        if char == '(':
            tokens.append(('LPAREN', char))
            i += 1
            continue
        
        if char == ')':
            tokens.append(('RPAREN', char))
            i += 1
            continue
        
        if char.isalpha():
            identifier_str = char
            i += 1

            while i < n and input[i].isalpha():
                identifier_str += input[i]
                i += 1
            
            tokens.append(('IDENTIFIER', identifier_str))
            continue

        if char.isspace():
            i += 1
            continue

        else:
            raise SyntaxError("Unexpected Char")
    
    return tokens
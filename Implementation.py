def lexer(input):
    i = 0
    n = len(input)

    tokens = []

    for i in range(n):
        char = input[i]

        if char.isdigit():
            number_str = char
            i += 1

            while input[i].isdigit() and i < n:
                number_str += input[i]
                i += 1
            
            tokens.append(('NUMBER', int(number_str)))
            continue
        
        if char.isalpha():
            identifier_str = char
            i += 1

            while input[i].isalpha() and i < n:
                identifier_str += input[i]
                i += 1
            
            tokens.append(('IDENTIFIER', identifier_str))
            continue
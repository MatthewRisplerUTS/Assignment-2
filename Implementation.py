def lexer(input):
    i = 0
    n = len(input)

    tokens = []

    for i in range(n):
        char = input[i]
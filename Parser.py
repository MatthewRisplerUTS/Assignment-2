from Lexer import lexer

parse_table = {}

def parser(tokens, parse_table):
    parser_stack = ['$', '<program>']
    position = 0
    next_token = tokens[position][0]

    while len(parser_stack) != 0:
        top_symbol = parser_stack.pop()

        if type(top_symbol) == str and top_symbol.startswith('<'):
            if (top_symbol, next_token) in parse_table:
                non_reversed_pt = parse_table(top_symbol, next_token)
                for symbol in reversed(non_reversed_pt):
                    parser_stack.append(symbol)
            else:
                raise SyntaxError("Unexpected lexer token")
            
        if top_symbol.startswith('<') == False:
            if top_symbol == next_token:
                parser_stack.pop()
                position += 1
                next_token = tokens[position][0]
            else:
                raise SyntaxError("Error")
        
    if next_token == '$':
        print("Complete")
    else:
        raise SyntaxError("Error")
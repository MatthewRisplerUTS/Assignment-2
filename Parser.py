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
                for element in reversed(non_reversed_pt):
                    parser_stack.append(element)
            else:
                raise SyntaxError("Unexpected lexer token")
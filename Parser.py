from Lexer import lexer

parse_table = {

    #<program>
    ('<program>', 'NUMBER'): ['<expr>'],
    ('<program>', 'IDENTIFIER'): ['<expr>'],
    ('<program>', 'LPAREN'): ['<expr>'],

    #<expr>
    ('<expr>', 'NUMBER'): ['NUMBER'],
    ('<expr>', 'IDENTIFIER'): ['IDENTIFIER'],
    ('<expr>', 'LPAREN'): ['LPAREN', '<paren-expr>', 'RPAREN'],

    #<paren-expr>
    ('<paren-expr>', 'NUMBER'): ['<expr>', '<more_expr>'],
    ('<paren-expr>', 'IDENTIFIER'): ['<expr>', '<more_expr>'],
    ('<paren-expr>', 'LPAREN'): ['<expr>', '<more_expr>'],
    ('<paren-expr>', 'PLUS'): ['PLUS', '<expr>', '<expr>'],
    ('<paren-expr>', 'MULT'): ['MULT', '<expr>', '<expr>'],
    ('<paren-expr>', 'EQUALS'): ['EQUALS', '<expr>', '<expr>'],
    ('<paren-expr>', 'MINUS'): ['MINUS', '<expr>', '<expr>'],
    ('<paren-expr>', 'CONDITIONAL'): ['CONDITIONAL', '<expr>', '<expr>', '<expr>'],
    ('<paren-expr>', 'LAMBDA'): ['LAMBDA', 'IDENTIFIER', '<expr>'],
    ('<paren-expr>', 'LET'): ['LET', 'IDENTIFIER', '<expr>', '<expr>'],

    #<more_expr>
    ('<more_expr>', 'RPAREN'): [''],
    ('<more_expr>', 'NUMBER'): ['<expr>', '<more_expr>'],
    ('<more_expr>', 'IDENTIFIER'): ['<expr>', '<more_expr>'],
    ('<more_expr>', 'LPAREN'): ['<expr>', '<more_expr>'],

}

def parser(tokens, parse_table):
    parser_stack = ['$', '<program>']
    position = 0
    next_token = tokens[position][0]

    while len(parser_stack) != 0:
        top_symbol = parser_stack.pop()

        # Non-terminal handling
        if type(top_symbol) == str and top_symbol.startswith('<'):
            if (top_symbol, next_token) in parse_table:
                non_reversed_pt = parse_table[(top_symbol, next_token)]
                for symbol in reversed(non_reversed_pt):
                    parser_stack.append(symbol)
            else:
                raise SyntaxError("Unexpected lexer token")
            
        # Terminal handling
        if top_symbol.startswith('<') == False:
            if top_symbol == next_token:
                if next_token != '$':
                    position += 1
                    next_token = tokens[position][0]
            else:
                raise SyntaxError("Error")
            
        # RPAREN handling
        if top_symbol == '':
            continue
        
    if next_token == '$':
        print("Complete")
    else:
        raise SyntaxError("Error")
    
if __name__ == "__main__":
    test_input = "(+ 2 3)"
    tokens = lexer(test_input) + [('$',  '$')]
    print(tokens)
    parser(tokens, parse_table)
from lexer import lexer

parse_table = {
    # <program>
    ('<program>', 'NUMBER'): ['<expr>'],
    ('<program>', 'IDENTIFIER'): ['<expr>'],
    ('<program>', 'LPAREN'): ['<expr>'],

    # <expr>
    ('<expr>', 'NUMBER'): ['NUMBER'],
    ('<expr>', 'IDENTIFIER'): ['IDENTIFIER'],
    ('<expr>', 'LPAREN'): ['LPAREN', '<paren-expr>', 'RPAREN'],

    # <paren-expr>
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

    # <more_expr>
    ('<more_expr>', 'RPAREN'): [''],
    ('<more_expr>', 'NUMBER'): ['<expr>', '<more_expr>'],
    ('<more_expr>', 'IDENTIFIER'): ['<expr>', '<more_expr>'],
    ('<more_expr>', 'LPAREN'): ['<expr>', '<more_expr>'],
}


def parser(tokens, parse_table):
    position = [0]

    def peek():
        if position[0] < len(tokens):
            return tokens[position[0]]
        return ('$', '$')

    def advance():
        token = peek()
        position[0] += 1
        return token

    def parse_expr():
        token_type, token_value = peek()

        if token_type == 'NUMBER':
            advance()
            return ['NUMBER', token_value]
        elif token_type == 'IDENTIFIER':
            advance()
            return ['IDENTIFIER', token_value]
        elif token_type == 'LPAREN':
            advance()  # consume '('
            result = parse_paren_expr()
            if peek()[0] != 'RPAREN':
                raise SyntaxError(f"Expected ')' but found '{peek()[0]}'")
            advance()  # consume ')'
            return result
        else:
            raise SyntaxError(f"Unexpected token in <expr>: {token_type}")

    def parse_paren_expr():
        token_type, token_value = peek()
        if token_type == 'PLUS':
            advance()
            expr1 = parse_expr()
            expr2 = parse_expr()
            return ['PLUS', expr1, expr2]

        elif token_type == 'MULT':
            advance()
            expr1 = parse_expr()
            expr2 = parse_expr()
            return ['MULT', expr1, expr2]

        elif token_type == 'EQUALS':
            advance()
            expr1 = parse_expr()
            expr2 = parse_expr()
            return ['EQUALS', expr1, expr2]

        elif token_type == 'MINUS':
            advance()
            expr1 = parse_expr()
            expr2 = parse_expr()
            return ['MINUS', expr1, expr2]

        elif token_type == 'CONDITIONAL':
            advance()
            expr1 = parse_expr()
            expr2 = parse_expr()
            expr3 = parse_expr()
            return ['CONDITIONAL', expr1, expr2, expr3]

        elif token_type == 'LAMBDA':
            advance()
            if peek()[0] != 'IDENTIFIER':
                raise SyntaxError("Lambda requires IDENTIFIER parameter")
            _, param = advance()
            body = parse_expr()
            return ['LAMBDA', param, body]

        elif token_type == 'LET':
            advance()
            if peek()[0] != 'IDENTIFIER':
                raise SyntaxError("Let requires IDENTIFIER")
            _, var = advance()
            value = parse_expr()
            body = parse_expr()
            return ['LET', var, value, body]

        elif token_type in ['NUMBER', 'IDENTIFIER', 'LPAREN']:
            exprs = []
            exprs.append(parse_expr())

            while peek()[0] in ['NUMBER', 'IDENTIFIER', 'LPAREN']:
                exprs.append(parse_expr())

            if len(exprs) == 1:
                return exprs[0]
            return exprs

        else:
            raise SyntaxError(f"Unexpected token in <paren-expr>: {token_type}")

    result = parse_expr()

    if peek()[0] != '$':
        raise SyntaxError(f"Unexpected tokens after parse: {peek()}")

    return result


parser_with_tree = parser

if __name__ == "__main__":
    try:
        from lexer import lexer
    except ImportError:
        from .lexer import lexer

    # Test cases
    test_cases = [
        "42",
        "x",
        "(+ 2 3)",
        "(× 2 3)",
        "(+ (× 2 3) 4)",
        "(? (= x 0) 1 0)",
        "(λ x x)",
        "(≜ y 10 y)",
        "((λ x (+ x 1)) 5)",
    ]

    print("Testing Parser with Parse Tree Construction")
    print("=" * 60)

    for test_input in test_cases:
        try:
            tokens = lexer(test_input)
            tokens.append(('$', '$'))
            tree = parser(tokens, parse_table)
            print(f"\nInput:  {test_input}")
            print(f"Tree:   {tree}")
        except Exception as e:
            print(f"\nInput:  {test_input}")
            print(f"Error:  {type(e).__name__}: {e}")

    print("\n" + "=" * 60)

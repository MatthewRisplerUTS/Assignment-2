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
def construct_parse_tree(token_stream):
    # recursively builds a parse tree from the token list."""
    
    def interpret_expr(cursor):
        tok_type, tok_val = token_stream[cursor]
        
        # case: numeric literal or identifier
        if tok_type in ('NUMBER', 'IDENTIFIER'):
            return tok_val, cursor + 1
            
        # case: parenthesised expression
        if tok_type == 'LPAREN':
            op_t, op_v = token_stream[cursor + 1]
            
            # Handle λ expression
            if op_t == 'LAMBDA':
                var_token = token_stream[cursor + 2][1]
                body_node, nxt = interpret_expr(cursor + 3)
                assert token_stream[nxt][0] == 'RPAREN', "Missing ) after lambda body"
                return ['LAMBDA', var_token, body_node], nxt + 1
            
            # Handle ≜ let-binding
            if op_t == 'LET':
                var_token = token_stream[cursor + 2][1]
                val_node, nxt1 = interpret_expr(cursor + 3)
                body_node, nxt2 = interpret_expr(nxt1)
                assert token_stream[nxt2][0] == 'RPAREN', "Missing ) after let body"
                return ['LET', var_token, val_node, body_node], nxt2 + 1

            # Conditional form (? cond true false)
            if op_t == 'CONDITIONAL':
                cond_node, nxt1 = interpret_expr(cursor + 2)
                true_node, nxt2 = interpret_expr(nxt1)
                false_node, nxt3 = interpret_expr(nxt2)
                assert token_stream[nxt3][0] == 'RPAREN', "Missing ) after conditional"
                return ['CONDITIONAL', cond_node, true_node, false_node], nxt3 + 1

            # Binary operators (+, ×, =, −)
            if op_t in ('PLUS', 'MULT', 'EQUALS', 'MINUS'):
                left_node, nxt1 = interpret_expr(cursor + 2)
                right_node, nxt2 = interpret_expr(nxt1)
                assert token_stream[nxt2][0] == 'RPAREN', f"Missing ) after {op_v} expression"
                return [op_t, left_node, right_node], nxt2 + 1
            
            expr_nodes = []
            op_node = interpret_expr(cursor + 1)[0]
            cursor_pos = cursor + 2
            while token_stream[cursor_pos][0] != 'RPAREN':
                arg_node, cursor_pos = interpret_expr(cursor_pos)
                expr_nodes.append(arg_node)
            return ['CALL', op_node] + expr_nodes, cursor_pos + 1
        raise SyntaxError(f"Unexpected token '{tok_val}' at position {cursor}")

    root_node, end_index = interpret_expr(0)
    if token_stream[end_index][0] != '$':
        raise SyntaxError("Unexpected extra tokens at end of input")
    return root_node

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
    
    print("Parse Tree Output:")
    tree_view = construct_parse_tree(tokens)
    print(tree_view)

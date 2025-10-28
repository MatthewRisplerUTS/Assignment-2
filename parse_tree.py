# imports and exceptions

class ParseError(Exception):
  #raised when an expression can't be parsed correctly
  pass


# lexer

def lexer(source):
  '''
  converts a raw string input into a sequence of tokens
  handles identifiers, numbers, parentheses and symbolic operators
  '''
  symbols = {
    '+': 'PLUS',
    'x': 'MULT',
    '=': 'EQUALS',
    '?': 'COND',
    'λ': 'LAMBDA',
    '≜': 'LET',
    '(': 'LPAREN',
    ')': 'RPAREN'
  }
  tokens = []
  current = ""
  for ch in source:
    if ch.isspace():
      if current:
        tokens.append(('IDENT' if not current.isdigit() else 'NUMBER', current))
        current = ""
    elif ch in symbols:
      if current:
        tokens.append(('IDENT' if not current.isdigit() else 'NUMBER', current))
        current = ""
      tokens.append((symbols[ch], ch))
    elif ch in '()':
      if current:
        tokens.append(('IDENT' if not current.isdigit() else 'NUMBER', current))
        current = ""
      tokens.append(('LPAREN' if ch == '(' else 'RPAREN',ch))
    else:
      current += ch
  if current:
    tokens.append(('IDENT' if not current.isdigit() else 'NUMBER', current))
  tokens.append(('$', '$')) # end marker
  return tokens
  

# operator rules and grammar 

operator_arity = {
  'PLUS': 2,
  'MULT': 2,
  'EQUALS': 2,
  'COND': 3,
  'LAMBDA': None,
  'LET': None
}

token_to_name = {
    'PLUS': 'PLUS',
    'MULT': 'MULT',
    'EQUALS': 'EQUALS',
    'COND': 'COND',
    'LAMBDA': 'LAMBDA',
    'LET': 'LET'
}
# core parser ===

def parser_build_tree(tokens):
    '''
    builds a raw parse tree from a token sequence.
    uses a recursive expansion model with minimal error recovery
    '''
    stack = []
    pos = 0

    def peek():
        return tokens[pos][0]

    def advance():
        nonlocal pos
        tok = tokens[pos]
        pos += 1
        return tok

    def parse_expr():
        tok_type = peek()
        if tok_type == 'NUMBER':
            return [int(advance()[1])]
        elif tok_type == 'IDENT':
            return [advance()[1]]
        elif tok_type == 'LPAREN':
            advance()  # consume '('
            op = peek()
            if op not in token_to_name:
                raise ParseError(f"Unexpected token '{op}' when expanding <expr>")
            op_token = token_to_name[advance()[0]]
            children = [op_token]
            while peek() not in ('RPAREN', '$'):
                children.append(parse_expr())
            if peek() != 'RPAREN':
                raise ParseError(f"Expected ')' but found '{peek()}' at position {pos}")
            advance()  # consume ')'
            return children
        else:
            raise ParseError(f"Unexpected token '{tok_type}' when expanding <expr>")

    result = parse_expr()
    if peek() != '$':
        raise ParseError(f"Extra tokens after parsing at position {pos}")
    return result


# post processing utilities
# these methods clean, validate and flatten the raw parse tree.

def _prune_nested_nodes(raw_node):
    '''
    simplifies redundant nested list structures from the raw parser output
    keeps the logical hierarchy intact while removing unnecessary wrapping
    '''
    if not isinstance(raw_node, list):
        return raw_node
    simplified = [_prune_nested_nodes(child) for child in raw_node]
    if len(simplified) == 1 and isinstance(simplified[0], list):
        return simplified[0]
    return simplified


def _sanity_check_tree(node):
    '''
    Validates that all operator nodes match the expected arity
    and that lambda/let constructs follow correct syntax patterns.
    '''
    if not isinstance(node, list):
        return node
    if not node:
        return []

    head = node[0]
    if isinstance(head, str) and head in operator_arity:
        if head == 'LAMBDA':
            if len(node) != 3 or not isinstance(node[1], str):
                raise ParseError("Malformed lambda expression – expected one parameter and one body.")
            return ['LAMBDA', node[1], _sanity_check_tree(node[2])]
        if head == 'LET':
            if len(node) != 4 or not isinstance(node[1], str):
                raise ParseError("Malformed let expression – expected identifier, value, and body.")
            return ['LET', node[1], _sanity_check_tree(node[2]), _sanity_check_tree(node[3])]

        arity = operator_arity[head]
        if arity is not None and len(node) - 1 != arity:
            raise ParseError(f"Operator '{head}' expects {arity} argument(s) but got {len(node)-1}.")
        return [head] + [_sanity_check_tree(x) for x in node[1:]]

    return [_sanity_check_tree(x) for x in node]


def _finalize_tree_format(tree):
    '''
    produces a clean, human-readable AST by unwrapping trivial lists and flattening operator arguments 
    this is the final step before interpretation or pretty-printing
    '''
    if not isinstance(tree, list):
        return tree
    if len(tree) == 1 and not isinstance(tree[0], list):
        return tree[0]

    formatted = [_finalize_tree_format(x) for x in tree]

    if formatted and isinstance(formatted[0], str) and formatted[0] in token_to_name.values():
        result = [formatted[0]]
        for arg in formatted[1:]:
            if isinstance(arg, list) and len(arg) == 1 and not isinstance(arg[0], list):
                result.append(arg[0])
            else:
                result.append(arg)
        return result

    if len(formatted) == 1 and isinstance(formatted[0], list):
        return formatted[0]

    return formatted


# testing section 
if __name__ == "__main__":
    examples = [
        "42",
        "x",
        "(+ 2 3)",
        "(× x 5)",
        "(+ (× 2 3) 4)",
        "(? (= x 0) 1 0)",
        "(λ x x)",
        "(≜ y 10 y)",
        "((λ x (+ x 1)) 5)",
        "(+ 2",
        ")",
        "(+ 2 3 4)"
    ]

    for expr in examples:
        try:
            toks = lexer(expr)
            raw_tree = parser_build_tree(toks)
            step1 = _prune_nested_nodes(raw_tree)
            step2 = _sanity_check_tree(step1)
            final_tree = _finalize_tree_format(step2)
            print(f"{expr} → {final_tree}")
        except Exception as e:
            print(f"{expr} → {type(e).__name__}: {e}")
        

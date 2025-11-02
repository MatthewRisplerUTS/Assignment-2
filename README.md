# **Assessment Task 2 \- Group Programming Assignment README**

**Due:** 31/10/2025 • **Language:** Python 3  
**Authors:** Kyler Chen (25972377), Matthew Rispler (24638189), Anushikha Narayan (25323647)

## **Overview**

In this project, a table-driven LL(1) parser for a simplified MiniLisp grammar is implemented.  
It includes:

* A lexer that converts raw input strings into tokens.

* A predictive parser that uses an explicit parse table to guide expansion.

* A parse-tree generator that outputs nested list structures, e.g.  
   `['PLUS', ['NUMBER', 2], ['NUMBER', 3]].`

* A comprehensive automated test suite validating correctness and error handling.

The parse-table design and grammatical analysis from Part A of the assignment specification are directly applied in the implementation.

## **Directory Structure**

`Assignment/`  
`├── lexer.py          # B.1  Tokeniser: converts source → token list`  
`├── parser.py         # B.2  LL(1) parser + B.3 parse-tree builder`  
`├── Test.parser.py    # C.1 & C.2 – Automated testing and validation`  
`└── __init__.py       # Empty file to make 'Assignment' a Python package`

## **Requirements**

* Python ≥ 3.9  
* All modules utilise the Python standard library exclusively and there are no external dependencies.

## **Running Tests**

From the project’s parent directory, run:

`python Assignment/Test.parser.py`

This executes all automated tests for Parts C.1 and C.2.

## **Expected output:**

`======================================================================`  
`MINILISP PARSER - COMPREHENSIVE TEST SUITE`  
`Part C: Testing and Validation`  
`======================================================================`

`MINILISP PARSER TEST RESULTS`  
`======================================================================`

`Overall Results:`  
  `Total Tests: 30`  
  `Passed: 30`  
  `Failed: 0`  
  `Pass Rate: 100.0%`

`Results by Category:`  
  `Basic: 5/5 passed`  
  `Nested: 4/4 passed`  
  `Function: 5/5 passed`  
  `Error: 9/9 passed`  
  `Edge: 7/7 passed`

`✓ All tests passed!`  
`Detailed results saved to test_results.json`

## **Test Categories**

| Category | Example | Purpose |
| :---- | :---- | :---- |
| Basic | `42, x, (+ 2 3)` | Validates simple expressions |
| Nested | `(+ (× 2 3) 4)` | Tests recursive parsing |
| Function | `(λ x x), (≜ y 10 y)` | Lambda and Let expressions |
| Error | `(+ 2, ), (× 5)` | Detects malformed syntax |
| Edge | `a, 123456, (f x y z)` | Handles identifiers, large numbers and spaces |

## **Test Results**

test\_results.json  
`{`  
  `"summary": {`  
    `"total_tests": 30,`  
    `"passed": 30,`  
    `"failed": 0,`  
    `"pass_rate": "100.0%"`  
  `},`  
  `"by_category": {`  
    `"basic": {"total":5,"passed":5,"failed":0},`  
    `...`  
  `},`  
  `"all_results": [ ... ]`  
`}`

## **Modifying Expected Results**

To update or add tests:

1. Open **`Test.parser.py`**.  
2. Locate the `run_all_tests()` function.  
3. Add or modify `tester.run_test(...)` entries:

    `tester.run_test(`  
       `"basic", "simple_addition", "(+ 2 3)",`  
       `['PLUS', ['NUMBER', 2], ['NUMBER', 3]]`  
   `)`

4. Save the file and rerun:  
    `python Assignment/Test.parser.py`

5. The new results will appear in the console and `test_results.json`.

## **Troubleshooting**

| Issue | Cause | Solution |
| :---- | :---- | :---- |
| `ModuleNotFoundError: No module named ‘Assignment’` | Missing `__init__.py` | Add an empty `__init__.py` file in `Assignment/` |
| `SyntaxError: Unexpected Char` | Invalid symbol or character in input | Ensure inputs only use valid MiniLisp symbols (+ − × \= ? λ ≜) |
| Script runs but no output | Script not run directly | Run with `python Assignment/Test.parser.py` |
| Parser fails on valid input | Missing `$` end token in test | Ensure tests append `(‘$’, ‘$’)` before parsing |

## **Integration with CI/CD**

The test script is made to be easily integrated into pipelines for continuous integration (e.g., Jenkins, GitLab CI, GitHub Actions).

**Example CI step:**  
`- name: Run MiniLisp Parser Tests`  
  `run: |`  
    `python Assignment/Test.parser.py`

* The script is compatible with CI pipelines since it exits with code 1 (sys.exit(1)) in the event that any test fails.  
* When it passes completely, test\_results.json is saved and code 0 is returned.  
* Reports can be produced by parsing the JSON file or uploading it as an artifact.

## **Components Summary**

**lexer.py**

* Converts raw input into token tuples (TOKEN\_TYPE, VALUE).  
* Recognises:  
  * Numbers (NUMBER)  
  * Identifiers (IDENTIFIER)  
  * Operators (+ − × \= ? λ ≜)  
  * Parentheses ((, ))  
  * Raises SyntaxError for empty or invalid input.

**parser.py**

* Employs a dictionary based parse\_table to implement an LL(1) predictive parser.  
* Grammar rules are expanded by the parser using a stack until all of the input has been used.  
* Includes a helper function to construct parse trees, producing nested Python lists.


**Examples:**

`Input: (+ 2 x)`  
`Output: ['PLUS', 2, 'x']`

`Input: (× (+ 1 2) 3)`  
`Output: ['MULT', ['PLUS', 1, 2], 3]`

`Input: (λ x (+ x 1))`  
`Output: ['LAMBDA', 'x', ['PLUS', 'x', 1]]`

**Test.parser.py**

* Provides a complete testing framework for all parts (C.1 & C.2).

* Uses a MiniLispTester class that:  
  * Runs tests grouped by category (basic, nested, function, error, edge)

  * Compares expected and actual parse trees

  * Displays a formatted summary

  * Saves detailed JSON results to test\_results.json

* Automatically exits with a failure code if any test fails.

## **Design Highlights**

* The predictive parsing loop is implemented directly via the manual LL(1) algorithm, which does not need parser generators.  
* Grammar Consistent: Complements the grammar examined in Part A.  
* Error Handling: Indicates incorrect argument counts, missing parenthesis, etc. by raising detailed SyntaxErrors.  
* Simple Parse Trees: For clarity, use nested lists rather than class-based ASTs.

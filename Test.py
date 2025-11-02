import json
import sys
from typing import Dict, List, Any

from .parser import parser, parse_table
from .lexer import lexer

class TestResult:
    def __init__(self, name: str, input_expr: str, expected_result: Any,
                 actual_result: Any, passed: bool, error_msg: str = ""):
        self.name = name
        self.input_expr = input_expr
        self.expected_result = expected_result
        self.actual_result = actual_result
        self.passed = passed
        self.error_msg = error_msg

    def to_dict(self):
        return {
            "test_name": self.name,
            "input": self.input_expr,
            "expected": self.expected_result,
            "actual": self.actual_result,
            "passed": self.passed,
            "error": self.error_msg
        }


class MiniLispTester:
    def __init__(self):
        self.results: List[TestResult] = []
        self.categories = {
            "basic": [],
            "nested": [],
            "function": [],
            "error": [],
            "edge": []
        }

    def run_test(self, category: str, name: str, input_expr: str,
                 expected_result: Any, should_error: bool = False):

        try:
            tokens = lexer(input_expr)
            tokens.append(('$', '$'))
            parse = parser(tokens, parse_table)

            if should_error:
                result = TestResult(
                    name, input_expr, expected_result, parse,
                    False, "Expected error but parsing succeeded"
                )
            else:
                # Check expected
                passed = self._compare_results(parse, expected_result)
                result = TestResult(
                    name, input_expr, expected_result, parse, passed
                )

        except Exception as e:
            if should_error:
                error_type = type(e).__name__
                passed = error_type == expected_result or expected_result == "Error"
                result = TestResult(
                    name, input_expr, expected_result, error_type, passed
                )
            else:
                result = TestResult(
                    name, input_expr, expected_result, None,
                    False, f"{type(e).__name__}: {str(e)}"
                )

        self.results.append(result)
        self.categories[category].append(result)
        return result

    def _compare_results(self, actual: Any, expected: Any) -> bool:
        return str(actual) == str(expected) or actual == expected

    def generate_report(self) -> Dict:
        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)

        report = {
            "summary": {
                "total_tests": total,
                "passed": passed,
                "failed": total - passed,
                "pass_rate": f"{(passed / total * 100):.1f}%" if total > 0 else "0%"
            },
            "by_category": {},
            "all_results": [r.to_dict() for r in self.results]
        }

        for category, tests in self.categories.items():
            if tests:
                cat_passed = sum(1 for t in tests if t.passed)
                report["by_category"][category] = {
                    "total": len(tests),
                    "passed": cat_passed,
                    "failed": len(tests) - cat_passed
                }

        return report

    def print_summary(self):
        report = self.generate_report()

        print("\n" + "=" * 70)
        print("MINILISP PARSER TEST RESULTS")
        print("=" * 70)

        summary = report["summary"]
        print(f"\nOverall Results:")
        print(f"  Total Tests: {summary['total_tests']}")
        print(f"  Passed: {summary['passed']}")
        print(f"  Failed: {summary['failed']}")
        print(f"  Pass Rate: {summary['pass_rate']}")

        print(f"\nResults by Category:")
        for category, stats in report["by_category"].items():
            print(f"  {category.capitalize()}: {stats['passed']}/{stats['total']} passed")

        # Show failed tests
        failed = [r for r in self.results if not r.passed]
        if failed:
            print(f"\nFailed Tests ({len(failed)}):")
            for r in failed:
                print(f"  ✗ {r.name}")
                print(f"    Input: {r.input_expr}")
                print(f"    Expected: {r.expected_result}")
                print(f"    Got: {r.actual_result}")
                if r.error_msg:
                    print(f"    Error: {r.error_msg}")

        print("\n" + "=" * 70)

    def save_results(self, filename: str = "test_results.json"):
        report = self.generate_report()
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"\nDetailed results saved to {filename}")


def run_all_tests():
    tester = MiniLispTester()

    # C.1

    # Numbers
    tester.run_test(
        "basic", "number_literal", "42",
        ['NUMBER', 42]
    )

    # Identifiers
    tester.run_test(
        "basic", "identifier", "x",
        ['IDENTIFIER', 'x']
    )

    # Addition
    tester.run_test(
        "basic", "simple_addition", "(+ 2 3)",
        ['PLUS', ['NUMBER', 2], ['NUMBER', 3]]
    )

    # Multiplication
    tester.run_test(
        "basic", "simple_multiplication", "(× x 5)",
        ['MULT', ['IDENTIFIER', 'x'], ['NUMBER', 5]]
    )

    # Subtraction
    tester.run_test(
        "basic", "simple_subtraction", "(- 10 3)",
        ['MINUS', ['NUMBER', 10], ['NUMBER', 3]]
    )


    # Nested arithmetic
    tester.run_test(
        "nested", "nested_arithmetic", "(+ (× 2 3) 4)",
        ['PLUS', ['MULT', ['NUMBER', 2], ['NUMBER', 3]], ['NUMBER', 4]]
    )

    tester.run_test(
        "nested", "nested_subtraction", "(- (+ 5 3) 2)",
        ['MINUS', ['PLUS', ['NUMBER', 5], ['NUMBER', 3]], ['NUMBER', 2]]
    )

    # Conditional
    tester.run_test(
        "nested", "conditional", "(? (= x 0) 1 0)",
        ['CONDITIONAL', ['EQUALS', ['IDENTIFIER', 'x'], ['NUMBER', 0]],
         ['NUMBER', 1], ['NUMBER', 0]]
    )

    tester.run_test(
        "nested", "deeply_nested", "(+ (× 2 (+ 3 4)) 5)",
        ['PLUS', ['MULT', ['NUMBER', 2],
                  ['PLUS', ['NUMBER', 3], ['NUMBER', 4]]],
         ['NUMBER', 5]]
    )

    tester.run_test(
        "function", "lambda_identity", "(λ x x)",
        ['LAMBDA', 'x', ['IDENTIFIER', 'x']]
    )

    tester.run_test(
        "function", "let_binding", "(≜ y 10 y)",
        ['LET', 'y', ['NUMBER', 10], ['IDENTIFIER', 'y']]
    )

    tester.run_test(
        "function", "function_application", "((λ x (+ x 1)) 5)",
        [['LAMBDA', 'x', ['PLUS', ['IDENTIFIER', 'x'], ['NUMBER', 1]]],
         ['NUMBER', 5]]
    )

    tester.run_test(
        "function", "complex_lambda", "(λ x (× x (+ x 1)))",
        ['LAMBDA', 'x', ['MULT', ['IDENTIFIER', 'x'],
                         ['PLUS', ['IDENTIFIER', 'x'], ['NUMBER', 1]]]]
    )

    tester.run_test(
        "function", "nested_let", "(≜ x 5 (≜ y 10 (+ x y)))",
        ['LET', 'x', ['NUMBER', 5],
         ['LET', 'y', ['NUMBER', 10],
          ['PLUS', ['IDENTIFIER', 'x'], ['IDENTIFIER', 'y']]]]
    )

    # C.2 ERROR HANDLING

    # Missing closing parenthesis
    tester.run_test(
        "error", "missing_closing_paren", "(+ 2",
        "SyntaxError", should_error=True
    )

    tester.run_test(
        "error", "unmatched_closing_paren", ")",
        "SyntaxError", should_error=True
    )

    # Wrong argument count for +
    tester.run_test(
        "error", "wrong_arg_count_plus", "(+ 2 3 4)",
        "SyntaxError", should_error=True
    )

    # Wrong argument count for ×
    tester.run_test(
        "error", "wrong_arg_count_mult", "(× 5)",
        "SyntaxError", should_error=True
    )

    # Wrong argument count for -
    tester.run_test(
        "error", "wrong_arg_count_minus", "(- 5)",
        "SyntaxError", should_error=True
    )

    # Empty input
    tester.run_test(
        "error", "empty_input", "",
        "SyntaxError", should_error=True
    )

    tester.run_test(
        "error", "invalid_character", "(+ 2 @)",
        "SyntaxError", should_error=True
    )

    tester.run_test(
        "error", "incomplete_conditional", "(? x 1)",
        "SyntaxError", should_error=True
    )

    tester.run_test(
        "error", "lambda_no_param", "(λ (+ x 1))",
        "SyntaxError", should_error=True
    )


    # Single character identifier
    tester.run_test(
        "edge", "single_char_identifier", "a",
        ['IDENTIFIER', 'a']
    )

    tester.run_test(
        "edge", "long_identifier", "myVariable",
        ['IDENTIFIER', 'myVariable']
    )

    tester.run_test(
        "edge", "zero", "0",
        ['NUMBER', 0]
    )

    # Large number
    tester.run_test(
        "edge", "large_number", "123456",
        ['NUMBER', 123456]
    )

    # Multiple spaces
    tester.run_test(
        "edge", "multiple_spaces", "(+    2    3)",
        ['PLUS', ['NUMBER', 2], ['NUMBER', 3]]
    )

    tester.run_test(
        "edge", "same_operator_nested", "(+ (+ 1 2) (+ 3 4))",
        ['PLUS', ['PLUS', ['NUMBER', 1], ['NUMBER', 2]],
         ['PLUS', ['NUMBER', 3], ['NUMBER', 4]]]
    )

    # Application with multiple arguments
    tester.run_test(
        "edge", "multi_arg_application", "(f x y z)",
        [['IDENTIFIER', 'f'], ['IDENTIFIER', 'x'],
         ['IDENTIFIER', 'y'], ['IDENTIFIER', 'z']]
    )

    return tester


if __name__ == "__main__":
    print("=" * 70)
    print("MINILISP PARSER - COMPREHENSIVE TEST SUITE")
    print("Part C: Testing and Validation")
    print("=" * 70)

    tester = run_all_tests()

    tester.print_summary()

    tester.save_results("test_results.json")

    report = tester.generate_report()
    if report["summary"]["failed"] > 0:
        sys.exit(1)
    else:
        print("\n✓ All tests passed!")
        sys.exit(0)

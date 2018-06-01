import unittest

from lu6.parserengine import ParserHelper, ExpressionParser
from lu6.syntaxtree.expression.arithmeticexpressions import *
from lu6.syntaxtree.literals import IntLiteral, StringLiteral
from lu6.scanner import StringScanner


class ArithmeticExpressionTest(unittest.TestCase):

    def subexpression(self, expr, expr_settings, lhs_settings, rhs_settings):
        # Check types
        self.assertIsInstance(expr.lhs, lhs_settings["type"])
        self.assertTrue(lhs_settings["eval"](expr.lhs))

        self.assertIsInstance(expr.rhs, rhs_settings["type"])
        self.assertTrue(rhs_settings["eval"](expr.rhs))

        self.assertIsInstance(expr, expr_settings["type"])
        self.assertTrue(expr_settings["eval"](expr))

    def make_test(self, string_to_test, parser_type, method, **settings):
        scanner = StringScanner()
        scanner.set_source(string_to_test)

        parser = parser_type(ParserHelper(scanner))
        parser.get_next_token()
        result = method(parser)
        self.subexpression(result, **settings)

    def test_addition(self):
        self.make_test(
            "2 + 2", ExpressionParser, ExpressionParser.parse_addition_expression,
            expr_settings={"type": AdditionExpression, "eval": lambda expr: expr.get_value() == 4},
            lhs_settings={"type": IntLiteral, "eval": lambda lhs: lhs.value == 2},
            rhs_settings={"type": IntLiteral, "eval": lambda rhs: rhs.value == 2}
        )

    def test_subtraction(self):
        self.make_test(
            "10 - 7", ExpressionParser, ExpressionParser.parse_addition_expression,
            expr_settings={"type": SubtractionExpression, "eval": lambda expr: expr.get_value() == 3},
            lhs_settings={"type": IntLiteral, "eval": lambda lhs: lhs.value == 10},
            rhs_settings={"type": IntLiteral, "eval": lambda rhs: rhs.value == 7}
        )

    def test_multiplication(self):
        self.make_test(
            "4 * 2", ExpressionParser, ExpressionParser.parse_multiplicative_expression,
            expr_settings={"type": MultiplicationExpression, "eval": lambda expr: expr.get_value() == 8},
            lhs_settings={"type": IntLiteral, "eval": lambda lhs: lhs.value == 4},
            rhs_settings={"type": IntLiteral, "eval": lambda rhs: rhs.value == 2}
        )

    def test_division(self):
        self.make_test(
            "6 / 2", ExpressionParser, ExpressionParser.parse_multiplicative_expression,
            expr_settings={"type": DivisionExpression, "eval": lambda expr: expr.get_value() == 3},
            lhs_settings={"type": IntLiteral, "eval": lambda lhs: lhs.value == 6},
            rhs_settings={"type": IntLiteral, "eval": lambda rhs: rhs.value == 2}
        )

        self.make_test(
            "5 / 2", ExpressionParser, ExpressionParser.parse_multiplicative_expression,
            expr_settings={"type": DivisionExpression, "eval": lambda expr: expr.get_value() == 2.5},
            lhs_settings={"type": IntLiteral, "eval": lambda lhs: lhs.value == 5},
            rhs_settings={"type": IntLiteral, "eval": lambda rhs: rhs.value == 2}
        )

    def test_remainder(self):
        self.make_test(
            "10 % 7", ExpressionParser, ExpressionParser.parse_multiplicative_expression,
            expr_settings={"type": RemainderExpression, "eval": lambda expr: expr.get_value() == 3},
            lhs_settings={"type": IntLiteral, "eval": lambda lhs: lhs.value == 10},
            rhs_settings={"type": IntLiteral, "eval": lambda rhs: rhs.value == 7}
        )

    def test_boolean(self):
        self.skipTest("Skipped because boolean True/False have not been implemented yet")

    def test_less(self):
        self.make_test(
            "10 < 2", ExpressionParser, ExpressionParser.parse_relational_expression,
            expr_settings={"type": StrictSmallerExpression, "eval": lambda expr: not expr.get_value()},
            lhs_settings={"type": IntLiteral, "eval": lambda lhs: lhs.value == 10},
            rhs_settings={"type": IntLiteral, "eval": lambda rhs: rhs.value == 2}
        )

        self.make_test(
            "2 <= 7", ExpressionParser, ExpressionParser.parse_relational_expression,
            expr_settings={"type": SmallerExpression, "eval": lambda expr: expr.get_value()},
            lhs_settings={"type": IntLiteral, "eval": lambda lhs: lhs.value == 2},
            rhs_settings={"type": IntLiteral, "eval": lambda rhs: rhs.value == 7}
        )

    def test_greater(self):
        self.make_test(
            "10 > 7", ExpressionParser, ExpressionParser.parse_relational_expression,
            expr_settings={"type": StrictGreaterExpression, "eval": lambda expr: expr.get_value()},
            lhs_settings={"type": IntLiteral, "eval": lambda lhs: lhs.value == 10},
            rhs_settings={"type": IntLiteral, "eval": lambda rhs: rhs.value == 7}
        )

        self.make_test(
            "2 >= 7", ExpressionParser, ExpressionParser.parse_relational_expression,
            expr_settings={"type": GreaterExpression, "eval": lambda expr: not expr.get_value()},
            lhs_settings={"type": IntLiteral, "eval": lambda lhs: lhs.value == 2},
            rhs_settings={"type": IntLiteral, "eval": lambda rhs: rhs.value == 7}
        )

    def test_equals(self):
        self.make_test(
            "2 == 7", ExpressionParser, ExpressionParser.parse_equality_expression,
            expr_settings={"type": EqualsExpression, "eval": lambda expr: not expr.get_value()},
            lhs_settings={"type": IntLiteral, "eval": lambda lhs: lhs.value == 2},
            rhs_settings={"type": IntLiteral, "eval": lambda rhs: rhs.value == 7}
        )

        self.make_test(
            "2 != 7", ExpressionParser, ExpressionParser.parse_equality_expression,
            expr_settings={"type": NotEqualExpression, "eval": lambda expr: expr.get_value()},
            lhs_settings={"type": IntLiteral, "eval": lambda lhs: lhs.value == 2},
            rhs_settings={"type": IntLiteral, "eval": lambda rhs: rhs.value == 7}
        )


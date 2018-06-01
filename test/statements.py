from parserengine.parserhelper import ParserHelper
from parserengine.expressionparser import ExpressionParser
from syntaxtree.literals import IntLiteral


class StatementTester:

    def __init__(self, scanner):
        self._parser = ExpressionParser(ParserHelper(scanner))
        self._parser.get_next_token()

    def start(self):
        addition = self._parser.parse_addition_expression()

        assert(isinstance(addition.lhs, IntLiteral))
        assert(isinstance(addition.rhs, IntLiteral))



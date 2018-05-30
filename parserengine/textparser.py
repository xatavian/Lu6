from .parserhelper import ParserHelper
from syntaxtree import TextStatement, LineStatement
from .parser import Parser
from scanner.scannerhelper import ScannerHelper


import tokens.tokens as tokens
from .expressionparser import ExpressionParser


class TextParser(Parser):

    def parse_text_statement(self):

        line = self.parserhelper.current_line
        result = None

        result = TextStatement(self.parserhelper.current_line, ExpressionParser(self.parserhelper).parse_or_expression())

        return result
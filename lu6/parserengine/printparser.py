from ..syntaxtree import PrintStatement, PrintlnStatement, InstructionStatement
from .parser import Parser

from .expressionparser import ExpressionParser
from ..tokens import tokens

class PrintParser(Parser):

    def parse_print_statement(self):
        line = self.parserhelper.current_line

        self.current_token_must_be(tokens.ReservedWordsTokens.PrintToken)
        self.get_next_token()

        return PrintStatement(line, ExpressionParser(self.parserhelper).parse_expression())

    def parse_println_statement(self):
        line = self.parserhelper.current_line

        self.current_token_must_be(tokens.ReservedWordsTokens.PrintlnToken)
        self.get_next_token()

        return PrintlnStatement(line, ExpressionParser(self.parserhelper).parse_expression())

    def parse_instruction_statement(self):
        line = self.parserhelper.current_line

        self.current_token_must_be(tokens.ReservedWordsTokens.InstructionToken)
        self.get_next_token()

        return InstructionStatement(line, ExpressionParser(self.parserhelper).parse_expression())

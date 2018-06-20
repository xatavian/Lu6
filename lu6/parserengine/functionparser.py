from .parser import Parser
from ..tokens import tokens

from .identifierparser import IdentifierParser
from .statementparser import StatementParser
from .expressionparser import ExpressionParser

from ..syntaxtree import FunctionDeclaration, Block, FormalParameter


class FunctionParser(Parser):

    def parse_function_declaration(self):
        line = self._parser_helper.current_line
        self.current_token_must_be(tokens.ReservedWordsTokens.FunctionToken)
        self.get_next_token()

        return_type, function_name, arguments, function_body = self.parse_function_declaration_details()
        return FunctionDeclaration(line, return_type, function_name, arguments, function_body)

    def parse_function_declaration_details(self):
        return_type = ExpressionParser(self.parserhelper).parse_expression()
        function_name = ExpressionParser(self.parserhelper).parse_expression()

        arguments = self.parse_arguments()

        function_body = None
        if not self.current_token_is(tokens.SpecialTokens.SemiColonToken):
            function_body = StatementParser(self.parserhelper).parse_block_statement()

        return return_type, function_name, arguments, function_body

    def parse_arguments(self):
        arguments = []
        line = self._parser_helper.current_line

        self.current_token_must_be(tokens.SpecialTokens.LParenToken)
        self.get_next_token()

        while not self.current_token_is(tokens.SpecialTokens.RParenToken):
            arg_type = IdentifierParser(self.parserhelper).parse_type()
            arg_name = IdentifierParser(self.parserhelper).parse_qualified_identifier()
            arguments.append(FormalParameter(line, arg_type, arg_name))

            if self.current_token_is(tokens.SpecialTokens.CommaToken):
                self.get_next_token()

        self.current_token_must_be(tokens.SpecialTokens.RParenToken)
        self.get_next_token()

        return arguments

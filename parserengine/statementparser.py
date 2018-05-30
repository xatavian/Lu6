from .parser import Parser
import tokens.tokens as tokens

from .textparser import TextParser
from .expressionparser import ExpressionParser

from syntaxtree.statements import *


class StatementParser(Parser):

    def parse_statement(self):
        line = self.parserhelper.current_line
        result = None

        if self.current_token_is(tokens.ReservedWordsTokens.PrintToken):
            self.get_next_token()
            result = TextParser(self.parserhelper).parse_text_statement()
            self.current_token_must_be(tokens.SpecialTokens.SemiColonToken)
            self.get_next_token()
        elif self.current_token_is(tokens.ReservedWordsTokens.IfToken):
            result = self.parse_if_statement()
        elif self.current_token_is(tokens.ReservedWordsTokens.WhileToken):
            result = self.parse_while_statement()
        elif self.current_token_is(tokens.SpecialTokens.LCurlyToken):
            result = self.parse_block_statement()
        else:
            result = ExpressionParser(self.parserhelper).parse_expression()
            self.current_token_must_be(tokens.SpecialTokens.SemiColonToken)
            self.get_next_token()

        # else: # self.current_token_is(tokens.IdentifierTokensList):
        #     raise ParserEngineException("{} cannot be directly used in "
        #                                 "function declaration. Use a print "
        #                                 "statement to write generated code.".format(self.current_token.type.name),
        #                                 line)
        return result

    def parse_if_statement(self):
        line = self.parserhelper.current_line

        self.current_token_must_be(tokens.ReservedWordsTokens.IfToken)
        self.get_next_token()

        condition = ExpressionParser(self.parserhelper).parse_par_expression()
        if_body = self.parse_statement()
        else_body = None
        if self.current_token_is(tokens.ReservedWordsTokens.ElseToken):
            self.get_next_token()
            else_body = self.parse_statement()

        return IfStatement(line, condition, if_body, else_body)

    def parse_block_statement(self):
        line = self._parser_helper.current_line
        self.current_token_must_be(tokens.SpecialTokens.LCurlyToken)
        self.get_next_token()

        statements = []
        while not self.current_token_is(tokens.SpecialTokens.RCurlyToken):
            statements.append(self.parse_statement())

        self.current_token_must_be(tokens.SpecialTokens.RCurlyToken)
        self.get_next_token()
        return Block(line, statements)

    def parse_while_statement(self):
        line = self.parserhelper.current_line

        self.current_token_must_be(tokens.ReservedWordsTokens.WhileToken)
        self.get_next_token()

        self.current_token_must_be(tokens.SpecialTokens.LParenToken)
        self.get_next_token()

        condition = ExpressionParser(self.parserhelper).parse_or_expression()

        self.current_token_must_be(tokens.SpecialTokens.RParenToken)
        self.get_next_token()

        body = self.parse_statement()

        return WhileStatement(line, condition, body)


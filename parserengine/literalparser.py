from .parser import Parser
from exceptions import ParserEngineException
import tokens.tokens as tokens
from syntaxtree import StringLiteral, IntLiteral


class LiteralParser(Parser):

    def parse_string_literal(self):
        self.current_token_must_be(tokens.LiteralTokens.StringLiteral)

        result = StringLiteral(self.parserhelper.current_line, self.current_token)
        self.get_next_token()

        return result

    def parse_int_literal(self):
        self.current_token_must_be(tokens.LiteralTokens.IntLiteral)

        result = IntLiteral(self.parserhelper.current_line, self.current_token)
        self.get_next_token()
        return result

    def parse_literal(self):
        if self.current_token_is(tokens.LiteralTokens.StringLiteral):
            return self.parse_string_literal()
        elif self.current_token_is(tokens.LiteralTokens.IntLiteral):
            return self.parse_int_literal()
        else:
            raise ParserEngineException("Could not parse literal", self.parserhelper.current_line)
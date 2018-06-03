from .parser import Parser
from ..syntaxtree import QualifiedIdentifier, Variable
from ..tokens import tokens


class IdentifierParser(Parser):

    def parse_qualified_identifier(self):
        self.current_token_must_be_one_of(tokens.IdentifierTokensList)
        return self.parse_identifier(True)

    def parse_identifier(self, allow_double_colon):
        qualified_identifier = QualifiedIdentifier(self.parserhelper.current_line)
        qualified_identifier.add_identifier(self.current_token)
        self.get_next_token()

        while self.current_token_is(tokens.SpecialTokens.DotToken) or \
            (allow_double_colon and self.current_token_is(tokens.SpecialTokens.DoubleColonToken)):
            self.get_next_token()
            self.current_token_must_be_one_of(tokens.IdentifierTokensList)
            qualified_identifier.add_identifier(self.current_token)
            self.get_next_token()

        return qualified_identifier

    def parse_single_identifier(self):
        self.current_token_must_be_one_of(tokens.IdentifierTokensList)
        qualified_identifier = QualifiedIdentifier(self.parserhelper.current_line)
        qualified_identifier.add_identifier(self.current_token)
        self.get_next_token()

        return qualified_identifier

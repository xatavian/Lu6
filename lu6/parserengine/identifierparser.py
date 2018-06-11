from .parser import Parser
from ..syntaxtree import QualifiedIdentifier, ParameterType
from ..syntaxtree.modifier import CONST, REFERENCE, POINTER
from ..tokens import tokens


class IdentifierParser(Parser):

    def parse_qualified_identifier(self):
        self.current_token_must_be_one_of(tokens.IdentifierTokensList)
        return self.parse_identifier(True)

    def parse_identifier(self, allow_double_colon):
        qualified_identifier = QualifiedIdentifier(self.parserhelper.current_line)
        qualified_identifier.add_identifier(self.current_token)
        self.get_next_token()

        while True:
            if self.current_token_is(tokens.SpecialTokens.DotToken):
                self.get_next_token()
                self.current_token_must_be_one_of(tokens.IdentifierTokensList)
                qualified_identifier.add_identifier(
                    self.current_token,
                    tokens.Token(tokens.SpecialTokens.DotToken.value, ".", self.parserhelper.current_line)
                )
                self.get_next_token()
            elif allow_double_colon and self.current_token_is(tokens.SpecialTokens.DoubleColonToken):
                self.get_next_token()
                self.current_token_must_be_one_of(tokens.IdentifierTokensList)
                qualified_identifier.add_identifier(
                    self.current_token,
                    tokens.Token(tokens.SpecialTokens.DoubleColonToken.value, "::", self.parserhelper.current_line)
                )
                self.get_next_token()
            else:
                break

        return qualified_identifier

    def parse_single_identifier(self):
        self.current_token_must_be_one_of(tokens.IdentifierTokensList)
        qualified_identifier = QualifiedIdentifier(self.parserhelper.current_line)
        qualified_identifier.add_identifier(self.current_token)
        self.get_next_token()

        return qualified_identifier

    def parse_type(self):
        line = self.parserhelper.current_line
        done, modifiers, type_name = False, [], None

        while not done:
            done = True
            if self.current_token_is(tokens.ReservedWordsTokens.ConstToken):
                done = False
                modifiers.append(CONST)
                self.get_next_token()
            elif self.current_token_is(tokens.SpecialTokens.StarToken):
                done = False
                modifiers.append(POINTER)
                self.get_next_token()
            elif self.current_token_is(tokens.SpecialTokens.AmpersandToken):
                done = False
                modifiers.append(REFERENCE)
                self.get_next_token()
            elif type_name is None and self.current_token_is_one_of(tokens.IdentifierTokensList):
                done = False
                type_name = self.parse_qualified_identifier()

        return ParameterType(line, modifiers, type_name)


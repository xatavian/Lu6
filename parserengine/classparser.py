# Parser Object import
from .parser import Parser
from exceptions import ParserEngineException
# Tokens import
import tokens.tokens as tokens
# Other parser objects imports
from .identifierparser import IdentifierParser
from .functionparser import FunctionParser
from .statementparser import StatementParser

# AST imports
from syntaxtree import ClassBody, ClassDeclaration, ConstructorDeclaration, MethodDeclaration, AttributeDeclaration
import syntaxtree.classes.accessmodifier as accessmodifier


class ClassParser(Parser):

    def parse_class_declaration(self):
        line = self._parser_helper.current_line

        # Get the Class Token
        self.current_token_must_be(tokens.ReservedWordsTokens.ClassToken)
        self.get_next_token()

        # Get the class name
        class_name = IdentifierParser(self.parserhelper).parse_qualified_identifier()

        # Get the extends name
        extends_name = None
        if self.current_token_is(tokens.ReservedWordsTokens.ExtendsToken):
            self.get_next_token()
            extends_name = IdentifierParser(self.parserhelper).parse_qualified_identifier()

        class_body = None
        if self.current_token_is(tokens.SpecialTokens.SemiColonToken):
            pass
        else:
            class_body = self.parse_class_body()

        return ClassDeclaration(line, class_name, extends_name, class_body)

    def parse_class_body(self):
        line = self.parserhelper.current_line
        self.current_token_must_be(tokens.SpecialTokens.LCurlyToken)
        self.get_next_token()

        members = []
        while not self.current_token_is(tokens.SpecialTokens.RCurlyToken):
            members.append(self.parse_member_declaration())
            self.get_next_token()

        self.current_token_is(tokens.SpecialTokens.RCurlyToken)
        self.get_next_token()

        return ClassBody(line, members)

    def parse_member_declaration(self):
        line = self._parser_helper.current_line

        result = None
        if self.current_token_is(tokens.ReservedWordsTokens.ConstructorToken):
            self.get_next_token()

            modifiers = [accessmodifier.PUBLIC]
            if self.current_token_is(tokens.SpecialTokens.ColonToken):
                self.get_next_token()
                modifiers = self.parse_access_modifier()

            arguments = FunctionParser(self.parserhelper).parse_arguments()
            body = None
            if not self.current_token_is(tokens.SpecialTokens.SemiColonToken):
                body = StatementParser(self.parserhelper).parse_block_statement()
            result = ConstructorDeclaration(line, modifiers, arguments, body)

        elif self.current_token_is(tokens.ReservedWordsTokens.MethodToken):
            self.get_next_token()

            modifiers = [accessmodifier.PUBLIC]
            if self.current_token_is(tokens.SpecialTokens.ColonToken):
                self.get_next_token()
                modifiers = self.parse_access_modifier()

            return_type, function_name, arguments, function_body = FunctionParser(self.parserhelper).parse_function_declaration_details()
            result = MethodDeclaration(line, modifiers, return_type, function_name, arguments, function_body)

        elif self.current_token_is(tokens.ReservedWordsTokens.AttributeToken):
            self.get_next_token()

            modifiers = [accessmodifier.PRIVATE]
            if self.current_token_is(tokens.SpecialTokens.ColonToken):
                self.get_next_token()
                modifiers = self.parse_access_modifier()

            attribute_type, attribute_name = self.parse_attribute_declaration()
            result = AttributeDeclaration(line, modifiers, attribute_type, attribute_name)
        self.current_token_must_be(tokens.SpecialTokens.SemiColonToken)
        return result

    def parse_access_modifier(self):
        result = []

        legal_tokens_list = [
            tokens.ReservedWordsTokens.PublicToken,
            tokens.ReservedWordsTokens.PrivateToken,
            tokens.ReservedWordsTokens.ProtectedToken,
            tokens.ReservedWordsTokens.StaticToken,
            tokens.ReservedWordsTokens.ConstToken
        ]

        if not self.current_token_is_one_of(legal_tokens_list):
            raise ParserEngineException("Member modifier was sought but {} "
                                        "was found".format(self.current_token.image),
                                        self.parserhelper.current_line)

        while self.current_token_is_one_of(legal_tokens_list):
            if self.current_token_is(tokens.ReservedWordsTokens.PublicToken):
                result.append(accessmodifier.PUBLIC)
            elif self.current_token_is(tokens.ReservedWordsTokens.PrivateToken):
                result.append(accessmodifier.PRIVATE)
            elif self.current_token_is(tokens.ReservedWordsTokens.ProtectedToken):
                result.append(accessmodifier.PROTECTED)
            elif self.current_token_is(tokens.ReservedWordsTokens.StaticToken):
                result.append(accessmodifier.STATIC)
            elif self.current_token_is(tokens.ReservedWordsTokens.ConstToken):
                result.append(accessmodifier.CONST)

            self.get_next_token()
            if self.current_token_is(tokens.SpecialTokens.CommaToken):
                self.get_next_token()

        return result

    def parse_attribute_declaration(self):
        self.current_token_must_be_one_of(tokens.IdentifierTokensList)
        attr_type = IdentifierParser(self.parserhelper).parse_qualified_identifier()
        attr_name = IdentifierParser(self.parserhelper).parse_qualified_identifier()

        return attr_type, attr_name
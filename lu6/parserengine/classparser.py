# Parser Object import
from .parser import Parser
from ..exceptions import ParserEngineException
# Tokens import
from ..tokens import tokens
# Other parser objects imports
from .identifierparser import IdentifierParser
from .expressionparser import ExpressionParser
from .functionparser import FunctionParser
from .statementparser import StatementParser

# AST imports
from ..syntaxtree import AttributeDeclaration, Block, ClassCategory, ClassBody, \
                         ClassDeclaration, ConstructorDeclaration, MethodDeclaration
from lu6.syntaxtree import modifier, IfStatement, WhileStatement


class ClassParser(Parser):

    def parse_class_declaration(self):
        line = self._parser_helper.current_line

        # Get the Class Token
        self.current_token_must_be(tokens.ReservedWordsTokens.ClassToken)
        self.get_next_token()

        # Get the class name
        class_name = ExpressionParser(self.parserhelper).parse_expression()

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

        self.current_token_is(tokens.SpecialTokens.RCurlyToken)
        self.get_next_token()

        return ClassBody(line, members)

    def parse_member_declaration(self):
        line = self._parser_helper.current_line

        result = None
        if self.current_token_is(tokens.ReservedWordsTokens.ConstructorToken):
            self.get_next_token()

            modifiers = [modifier.PUBLIC]
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

            modifiers = [modifier.PUBLIC]
            if self.current_token_is(tokens.SpecialTokens.ColonToken):
                self.get_next_token()
                modifiers = self.parse_access_modifier()

            return_type, function_name, arguments, function_body = FunctionParser(self.parserhelper).parse_function_declaration_details()
            result = MethodDeclaration(line, modifiers, return_type, function_name, arguments, function_body)

        elif self.current_token_is(tokens.ReservedWordsTokens.AttributeToken):
            self.get_next_token()

            modifiers = [modifier.PRIVATE]
            if self.current_token_is(tokens.SpecialTokens.ColonToken):
                self.get_next_token()
                modifiers = self.parse_access_modifier()

            attribute_type, attribute_name = self.parse_attribute_declaration()
            result = AttributeDeclaration(line, modifiers, attribute_type, attribute_name)

        elif self.current_token_is(tokens.ReservedWordsTokens.CategoryToken):
            self.get_next_token()

            category_name = ExpressionParser(self.parserhelper).parse_expression()
            body = self.parse_category_body()

            result = ClassCategory(line, category_name, body)

        elif self.current_token_is_one_of(tokens.StatementTokens):
            return self.parse_statement_member()  # Skip ending semicolon

        elif self.current_token_is(tokens.SpecialTokens.LCurlyToken):
            return self.parse_class_block()  # Skip ending semicolon
        else:
            result = ExpressionParser(self.parserhelper).parse_expression()

        self.current_token_must_be(tokens.SpecialTokens.SemiColonToken)
        self.get_next_token()
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
                result.append(modifier.PUBLIC)
            elif self.current_token_is(tokens.ReservedWordsTokens.PrivateToken):
                result.append(modifier.PRIVATE)
            elif self.current_token_is(tokens.ReservedWordsTokens.ProtectedToken):
                result.append(modifier.PROTECTED)
            elif self.current_token_is(tokens.ReservedWordsTokens.StaticToken):
                result.append(modifier.STATIC)
            elif self.current_token_is(tokens.ReservedWordsTokens.ConstToken):
                result.append(modifier.CONST)

            self.get_next_token()
            if self.current_token_is(tokens.SpecialTokens.CommaToken):
                self.get_next_token()

        return result

    def parse_attribute_declaration(self):
        attr_type = ExpressionParser(self.parserhelper).parse_expression()
        attr_name = ExpressionParser(self.parserhelper).parse_expression()

        return attr_type, attr_name

    def parse_category_body(self):
        line = self.parserhelper.current_line

        self.current_token_must_be(tokens.SpecialTokens.LCurlyToken)
        self.get_next_token()

        statements = []
        while not self.current_token_is(tokens.SpecialTokens.RCurlyToken):
            statements.append(self.parse_member_declaration())

        self.current_token_must_be(tokens.SpecialTokens.RCurlyToken)
        self.get_next_token()

        return Block(line, statements)

    def parse_statement_member(self):
        line = self.parserhelper.current_line
        if self.current_token_is(tokens.ReservedWordsTokens.WhileToken):
            self.get_next_token()
            condition = ExpressionParser(self.parserhelper).parse_par_expression()
            body = self.parse_member_declaration()

            return WhileStatement(line, condition, body)

        elif self.current_token_is(tokens.ReservedWordsTokens.IfToken):
            self.get_next_token()
            condition = ExpressionParser(self.parserhelper).parse_par_expression()
            if_body = self.parse_member_declaration()
            else_body = None
            if self.current_token_is(tokens.ReservedWordsTokens.ElseToken):
                self.get_next_token()
                else_body = self.parse_member_declaration()

            return IfStatement(line, condition, if_body, else_body)

    def parse_class_block(self):
        line = self.parserhelper.current_line
        self.current_token_must_be(tokens.SpecialTokens.LCurlyToken)
        self.get_next_token()

        statements = []
        while not self.current_token_is(tokens.SpecialTokens.RCurlyToken):
            statements.append(self.parse_member_declaration())

        self.current_token_must_be(tokens.SpecialTokens.RCurlyToken)
        self.get_next_token()

        return Block(line, statements)

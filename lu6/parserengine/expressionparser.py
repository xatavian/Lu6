from .parser import Parser
from ..tokens import tokens
from ..syntaxtree import AssignementExpression, AssignmentMultiplicationExpression, AssignmentAdditionExpression, \
                        AssignmentDivisionExpression, AssignmentSubtractionExpression, AssignmentRemainderExpression, \
                        OrExpression, AndExpression, EqualsExpression, SmallerExpression, GreaterExpression, \
                        StrictGreaterExpression, StrictSmallerExpression, AdditionExpression, SubtractionExpression, \
                        DivisionExpression, MultiplicationExpression, RemainderExpression, Variable, FieldSelection

from .identifierparser import IdentifierParser
from .literalparser import LiteralParser
from ..exceptions import ParserEngineException


class ExpressionParser(Parser):

    def parse_expression(self):
        return self.parse_assignment_expression()

    def parse_assignment_expression(self):
        line = self.parserhelper.current_line
        result = self.parse_or_expression()
        if self.current_token_is(tokens.SpecialTokens.AssignToken):
            self.get_next_token()
            result = AssignementExpression(line, result, self.parse_assignment_expression())
        elif self.current_token_is(tokens.SpecialTokens.MultiplyAssignToken):
            self.get_next_token()
            result = AssignmentMultiplicationExpression(line, result, self.parse_assignment_expression())
        elif self.current_token_is(tokens.SpecialTokens.PlusAssignToken):
            self.get_next_token()
            result = AssignmentAdditionExpression(line, result, self.parse_assignment_expression())
        elif self.current_token_is(tokens.SpecialTokens.MinusAssignToken):
            self.get_next_token()
            result = AssignmentSubtractionExpression(line, result, self.parse_assignment_expression())
        elif self.current_token_is(tokens.SpecialTokens.DivisionAssignToken):
            self.get_next_token()
            result = AssignmentDivisionExpression(line, result, self.parse_assignment_expression())
        elif self.current_token_is(tokens.SpecialTokens.RemainderAssignToken):
            self.get_next_token()
            result = AssignmentRemainderExpression(line, result, self.parse_assignment_expression())
        return result

    def parse_or_expression(self):
        line = self.parserhelper.current_line
        result = self.parse_and_expression()
        while self.current_token_is(tokens.SpecialTokens.OrToken):
            self.get_next_token()
            result = OrExpression(line, result, self.parse_and_expression())

        return result

    def parse_and_expression(self):
        line = self.parserhelper.current_line
        result =  self.parse_equality_expression()
        while self.current_token_is(tokens.SpecialTokens.AndToken):
            self.get_next_token()
            result = AndExpression(line, result, self.parse_equality_expression())

        return result

    def parse_equality_expression(self):
        line = self.parserhelper.current_line
        result = self.parse_relational_expression()
        while self.current_token_is(tokens.SpecialTokens.EqualsToken):
            self.get_next_token()
            result = EqualsExpression(line, result, self.parse_relational_expression())

        return result

    def parse_relational_expression(self):
        line = self.parserhelper.current_line
        result = self.parse_addition_operation()
        while self.current_token_is_one_of([tokens.SpecialTokens.LessToken, tokens.SpecialTokens.StrictLessToken,
                                            tokens.SpecialTokens.GreaterToken, tokens.SpecialTokens.StrictGreaterToken]):

            if self.current_token_is(tokens.SpecialTokens.LessToken):
                self.get_next_token()
                result = SmallerExpression(line, result, self.parse_addition_operation())
            elif self.current_token_is(tokens.SpecialTokens.StrictLessToken):
                self.get_next_token()
                result = StrictSmallerExpression(line, result, self.parse_addition_operation())
            elif self.current_token_is(tokens.SpecialTokens.GreaterToken):
                self.get_next_token()
                result = GreaterExpression(line, result, self.parse_addition_operation())
            elif self.current_token_is(tokens.SpecialTokens.StrictGreaterToken):
                self.get_next_token()
                result = StrictGreaterExpression(line, result, self.parse_addition_operation())

        return result

    def parse_addition_operation(self):
        line = self.parserhelper.current_line
        result = self.parse_multiplicative_expression()
        while self.current_token_is_one_of([tokens.SpecialTokens.PlusToken, tokens.SpecialTokens.MinusToken]):
            if self.current_token_is(tokens.SpecialTokens.PlusToken):
                self.get_next_token()
                result = AdditionExpression(line, result, self.parse_multiplicative_expression())
            elif self.current_token_is(tokens.SpecialTokens.MinusToken):
                self.get_next_token()
                result = SubtractionExpression(line, result, self.parse_multiplicative_expression())

        return result

    def parse_multiplicative_expression(self):
        line = self.parserhelper.current_line
        result = self.parse_unary_expression()

        while self.current_token_is_one_of([tokens.SpecialTokens.StarToken, tokens.SpecialTokens.SlashToken,
                                            tokens.SpecialTokens.RemToken]):

            if self.current_token_is(tokens.SpecialTokens.StarToken):
                self.get_next_token()
                result = MultiplicationExpression(line, result, self.parse_unary_expression())
            elif self.current_token_is(tokens.SpecialTokens.SlashToken):
                self.get_next_token()
                result = DivisionExpression(line, result, self.parse_unary_expression())
            elif self.current_token_is(tokens.SpecialTokens.RemToken):
                self.get_next_token()
                result = RemainderExpression(line, result, self.parse_unary_expression())

        return result

    def parse_unary_expression(self):
        return self.parse_primary_expression() # Ignore unary expressions for now

    def parse_par_expression(self):
        self.current_token_must_be(tokens.SpecialTokens.LParenToken)
        self.get_next_token()

        expr = self.parse_expression()

        self.current_token_must_be(tokens.SpecialTokens.RParenToken)
        self.get_next_token()

        return expr

    def parse_primary_expression(self):
        line = self.parserhelper.current_line
        if self.current_token_is(tokens.IdentifierTokens.VariableIdentifier):
            expression = IdentifierParser(self.parserhelper).parse_identifier(allow_double_colon=False)
            if self.current_token_is(tokens.SpecialTokens.LParenToken):
                # TODO: parse message expression
                pass
            elif expression.is_field_selection:
                return FieldSelection(line, expression)
            else:
                return Variable.from_qualified_identifier(expression)
        elif self.current_token_is(tokens.SpecialTokens.LParenToken):
            return self.parse_par_expression()
        elif self.current_token_is_one_of(tokens.LiteralTokens):
            return LiteralParser(self.parserhelper).parse_literal()

        raise ParserEngineException("No primary expression was found (token {})".format(self.current_token), line)

from .parser import Parser
from .parser import ParserHelper

from ..tokens import tokens

from .classparser import ClassParser
from .functionparser import FunctionParser
from .literalparser import LiteralParser
from .expressionparser import ExpressionParser

from ..syntaxtree import CompilationUnit
from ..exceptions import ParserEngineException


class CompilationUnitParser(Parser):
    def __init__(self, scanner):
        super().__init__(ParserHelper(scanner))
        self.get_next_token()

    def parse_compilation_unit(self):
        line = self.parserhelper.current_line

        include_list = []
        while self.current_token_is(tokens.ReservedWordsTokens.IncludeToken):
            self.get_next_token()
            include_list.append(ExpressionParser(self.parserhelper).parse_expression())
            self.current_token_must_be(tokens.SpecialTokens.SemiColonToken)
            self.get_next_token()

        type_declarations = []
        while not self.current_token_is(tokens.SpecialTokens.EOFToken):
            type_declarations.append(self.parse_type_declaration())

        return CompilationUnit(self._parser_helper.filename, line, include_list, type_declarations)

    def parse_type_declaration(self):
        result = None
        line = self.parserhelper.current_line

        if self.current_token_is(tokens.ReservedWordsTokens.ClassToken):
            result = ClassParser(self.parserhelper).parse_class_declaration()
        elif self.current_token_is(tokens.ReservedWordsTokens.FunctionToken):
            result = FunctionParser(self.parserhelper).parse_function_declaration()
        else:
            raise ParserEngineException("Token \"{}\" (type {}) is not valid "
                                        "for type declaration".format(self.current_token.image,
                                                                      self.current_token.type.name), line)
        self.current_token_must_be(tokens.SpecialTokens.SemiColonToken)
        self.get_next_token()
        return result

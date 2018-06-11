from ..astnode import ASTNode
from ..modifier import *
from ...exceptions import TemplateEngineException


class ParameterType(ASTNode):
    def __init__(self, line, modifiers, type_name):
        super().__init__(line)
        self._modifiers = modifiers
        self._type_name = type_name

    def analyse(self, context=None):
        self.context = context

        if PUBLIC in self._modifiers:
            raise TemplateEngineException("public is an invalid modifier in this context", self.line)
        if PROTECTED in self._modifiers:
            raise TemplateEngineException("protected is an invalid modifier in this context", self.line)
        if PRIVATE in self._modifiers:
            raise TemplateEngineException("private is an invalid modifier in this context", self.line)
        if STATIC in self._modifiers:
            raise TemplateEngineException("static is an invalid modifier in this context", self.line)

        self._type_name = self._type_name.analyse(self.context)
        return self

    def codegen(self, output_stream, base_indent=0):
        if CONST in self._modifiers:
            output_stream.print("const ", "h_file", base_indent)

        self._type_name.codegen(output_stream, base_indent)

        for mod in self._modifiers:
            if mod is POINTER:
                output_stream.print("*", "h_file", base_indent)
            if mod is REFERENCE:
                output_stream.print("&", "h_file", base_indent)

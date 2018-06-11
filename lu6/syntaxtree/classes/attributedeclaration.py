from ..astnode import ASTNode
from lu6.syntaxtree.modifier import CONST, STATIC


class AttributeDeclaration(ASTNode):

    def __init__(self, line, modifiers, type, name):
        super().__init__(line)
        self._modifiers = modifiers
        self._type = type
        self._name = name

    @property
    def modifiers(self):
        return self._modifiers

    def analyse(self, context=None):
        self.context = context

    def codegen(self, output_stream, base_indent=0):

        if CONST in self._modifiers:
            output_stream.print("const ", "h_file", base_indent)
        if STATIC in self._modifiers:
            output_stream.print("static ", "h_file", base_indent)

        output_stream.print("{type} {name};".format(
            type=self._type,
            name=self._name
        ),
            "h_file", base_indent)
        output_stream.newline("h_file")
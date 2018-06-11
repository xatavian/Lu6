from lu6.syntaxtree.astnode import ASTNode


class FormalParameter(ASTNode):
    def analyse(self, context=None):
        self.context = context

        self._type = self._type.analyse(context)
        if self._name is not None:
            self._name = self._name.analyse(context)

        return self

    def codegen(self, output_stream, base_indent=0):
        self._type.codegen(output_stream, base_indent)
        output_stream.print(" ", "h_file", base_indent)
        self._name.codegen(output_stream, base_indent)

    def __init__(self, line, type, name):
        super().__init__(line)
        self._name = name
        self._type = type

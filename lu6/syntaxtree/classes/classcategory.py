from ..astnode import ASTNode
from ..statements.block import Block


class ClassCategory(ASTNode):
    def __init__(self, line, name, body=None):
        super().__init__(line)
        self._name = name
        if body is not None:
            self._body = body
        else:
            self._body = Block(line, [])

    def analyse(self, context=None):
        print("Analysis")
        self.context = context
        self._name = self._name.analyse(self.context)

        if self._body is not None:
            self._body = self._body.analyse(self.context)

        return self

    @property
    def declarations(self):
        return self._body.statements

    def codegen(self, output_stream, base_indent=0):
        if self._body is None or len(self._body.statements) == 0:
            return

        if not isinstance(self._name, str):
            self._name.codegen(output_stream, base_indent)
        else:
            output_stream.print(self._name, "h_file", base_indent)

        output_stream.print(":", "h_file", base_indent)
        output_stream.newline("h_file")

        self._body.codegen(output_stream, base_indent + 2)
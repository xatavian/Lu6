from .astnode import ASTNode
from ..tokens import tokens

class FormalParameter(ASTNode):
    def analyse(self, context=None):
        self.context = context

        self._type.analyse(context)
        if self._name is not None:
            self._name.analyse(context)

    def codegen(self, output_stream, base_indent=0):
        output_stream.print(
            "{vType} {vName}".format(vType=str(self._type), vName=str(self._name)),
            "h_file", base_indent)
        #output_stream.newline("h_file")

    def __init__(self, line, type, name):
        super().__init__(line)
        self._name = name
        self._type = type

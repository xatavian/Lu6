from ..astnode import ASTNode
from .attributedeclaration import AttributeDeclaration
from .methoddeclaration import MethodDeclaration
from .classcategory import ClassCategory
from lu6.syntaxtree.modifier import PUBLIC, PRIVATE, PROTECTED


class ClassBody(ASTNode):
    def __init__(self, line, members):
        super().__init__(line)
        self._members = members

    def codegen(self, output_stream, base_indent=0):
        output_stream.print("{", "h_file")
        output_stream.newline("h_file")

        for member in self._members:
            member.codegen(output_stream, base_indent)

        output_stream.print("}", "h_file", base_indent)

    def analyse(self, context=None):
        self.context = context

        for i, member in enumerate(self._members):
            self._members[i] = member.analyse(context)

        return self

    @property
    def members(self):
        return self._members
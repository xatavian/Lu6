from ..astnode import ASTNode
from .attributedeclaration import AttributeDeclaration
from .methoddeclaration import MethodDeclaration
from .constructordeclaration import ConstructorDeclaration
from .accessmodifier import PUBLIC, PRIVATE, PROTECTED, STATIC, CONST

class ClassBody(ASTNode):

    def __init__(self, line, members):
        super().__init__(line)
        self._members = members

    def codegen(self, output_stream, base_indent=0):
        output_stream.print("{", "h_file")
        output_stream.newline("h_file")

        attributes = list(
            filter(lambda mem: isinstance(mem, AttributeDeclaration), self._members))
        methods = list(
            filter(lambda mem: isinstance(mem, MethodDeclaration) or isinstance(mem, ConstructorDeclaration),
                   self._members))

        meths = [
            list(filter(lambda meth: PUBLIC in meth.modifiers, methods)),
            list(filter(lambda meth: PRIVATE in meth.modifiers, methods)),
            list(filter(lambda meth: PROTECTED in meth.modifiers, methods))
        ]

        attrs = [
            list(filter(lambda attr: PUBLIC in attr.modifiers, attributes)),
            list(filter(lambda attr: PRIVATE in attr.modifiers, attributes)),
            list(filter(lambda attr: PROTECTED in attr.modifiers, attributes))
        ]

        labels = ["public", "private", "protected"]

        for meths_label, meths_list in zip(labels, meths):
            set_header = True
            for meth in meths_list:
                if set_header:
                    output_stream.print("{}: ".format(meths_label), "h_file", base_indent)
                    output_stream.newline("h_file")
                    set_header = False

                meth.codegen(output_stream, base_indent + 2)

        for attr_label, attr_list in zip(labels, attrs):
            set_header = True
            for attr in attr_list:
                if set_header:
                    output_stream.print("{}: ".format(attr_label), "h_file", base_indent)
                    output_stream.newline("h_file")
                    set_header = False
                attr.codegen(output_stream, base_indent + 2)

        output_stream.print("}", "h_file", base_indent)

    def analyse(self, context=None):
        self.context = context
        for member in self._members:
            member.analyse(context)

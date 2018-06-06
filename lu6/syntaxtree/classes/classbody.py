from ..astnode import ASTNode
from .attributedeclaration import AttributeDeclaration
from .methoddeclaration import MethodDeclaration
from .classcategory import ClassCategory
from .accessmodifier import PUBLIC, PRIVATE, PROTECTED, STATIC, CONST


class ClassBody(ASTNode):
    def __init__(self, line, members):
        super().__init__(line)
        self._members = members

        # Categories
        self._method_categories = {
            "public": ClassCategory(line, "public"),
            "protected": ClassCategory(line, "protected"),
            "private": ClassCategory(line, "private")
        }

        self._attributes_categories = {
            "public": ClassCategory(line, "public"),
            "protected": ClassCategory(line, "protected"),
            "private": ClassCategory(line, "private")
        }

        self._other_categories = []

    def codegen(self, output_stream, base_indent=0):
        output_stream.print("{", "h_file")
        output_stream.newline("h_file")

        self._method_categories["public"].codegen(output_stream, base_indent)
        self._method_categories["protected"].codegen(output_stream, base_indent)
        self._method_categories["private"].codegen(output_stream, base_indent)

        self._attributes_categories["public"].codegen(output_stream, base_indent)
        self._attributes_categories["protected"].codegen(output_stream, base_indent)
        self._attributes_categories["private"].codegen(output_stream, base_indent)

        for category in self._other_categories:
            category.codegen(output_stream, base_indent)

        output_stream.print("}", "h_file", base_indent)

    def analyse(self, context=None):
        self.context = context

        for member in self._members:
            member.analyse(context)

            if isinstance(member, AttributeDeclaration):
                if PUBLIC in member.modifiers:
                    self._attributes_categories["public"].declarations.append(member)
                elif PROTECTED in member.modifiers:
                    self._attributes_categories["protected"].declarations.append(member)
                elif PRIVATE in member.modifiers:
                    self._attributes_categories["private"].declarations.append(member)

            elif isinstance(member, MethodDeclaration):
                if PUBLIC in member.modifiers:
                    self._method_categories["public"].declarations.append(member)
                elif PROTECTED in member.modifiers:
                    self._method_categories["protected"].declarations.append(member)
                elif PRIVATE in member.modifiers:
                    self._method_categories["private"].declarations.append(member)

            elif isinstance(member, ClassCategory):
                self._other_categories.append(member)


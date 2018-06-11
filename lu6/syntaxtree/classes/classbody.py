from ..astnode import ASTNode
from .attributedeclaration import AttributeDeclaration
from .methoddeclaration import MethodDeclaration
from .classcategory import ClassCategory
from lu6.syntaxtree.modifier import PUBLIC, PRIVATE, PROTECTED


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

        for i, member in enumerate(self._members):
            self._members[i] = member.analyse(context)
            analyzed_member = self._members[i]
            if isinstance(analyzed_member, AttributeDeclaration):
                if PUBLIC in analyzed_member.modifiers:
                    self._attributes_categories["public"].declarations.append(analyzed_member)
                elif PROTECTED in analyzed_member.modifiers:
                    self._attributes_categories["protected"].declarations.append(analyzed_member)
                elif PRIVATE in analyzed_member.modifiers:
                    self._attributes_categories["private"].declarations.append(analyzed_member)

            elif isinstance(analyzed_member, MethodDeclaration):
                if PUBLIC in member.modifiers:
                    self._method_categories["public"].declarations.append(analyzed_member)
                elif PROTECTED in member.modifiers:
                    self._method_categories["protected"].declarations.append(analyzed_member)
                elif PRIVATE in member.modifiers:
                    self._method_categories["private"].declarations.append(analyzed_member)

            elif isinstance(analyzed_member, ClassCategory):
                self._other_categories.append(analyzed_member)

        return self


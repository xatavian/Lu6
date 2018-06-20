from .methoddeclaration import MethodDeclaration
from .classdeclaration import ClassDeclaration


class ConstructorDeclaration(MethodDeclaration):

    def __init__(self, line, modifiers, arguments, body):
        # Constructor gets its name from the class context
        super().__init__(line, modifiers, None, None, arguments, body)

    def analyse(self, context=None):
        super().analyse(context)

        self.name = context.get_value(ClassDeclaration.ClassNameVariableName).value
        self.extends = context.get_value(ClassDeclaration.ExtendsNameVariableName).value

        return self

    def codegen(self, output_stream, base_indent=0):
        self.name.codegen(output_stream, base_indent)
        output_stream.print(" ", "h_file", base_indent)

        self.codegen_arguments(output_stream, base_indent)

        if self.extends is not None:
            output_stream.print(": ", "h_file", base_indent)
            self.extends.codegen(output_stream, base_indent)
            output_stream.print("()", "h_file", base_indent)

        if self.body is not None:
            output_stream.print("{", "h_file", base_indent)
            output_stream.newline("h_file")

            self.body.codegen(output_stream, base_indent + 2)

            output_stream.print("}", "h_file", base_indent)
            output_stream.newline("h_file")
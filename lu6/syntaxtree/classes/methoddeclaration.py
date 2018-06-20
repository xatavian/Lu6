from lu6.syntaxtree.functions.functiondeclaration import FunctionDeclaration
from lu6.syntaxtree.modifier import CONST, STATIC, PUBLIC, PROTECTED, PRIVATE
from ...contexttable import MemberContext

class MethodDeclaration(FunctionDeclaration):

    @staticmethod
    def from_function_declaration(access_modifiers, function_declaration):
        return MethodDeclaration(function_declaration.line,
                                 access_modifiers,
                                 function_declaration.returnType,
                                 function_declaration.name,
                                 function_declaration.arguments,
                                 function_declaration.body)

    def __init__(self, line, modifiers, return_type, name, arguments, body):
        super().__init__(line, return_type, name, arguments, body)
        self._modifiers = modifiers

    def codegen(self, output_stream, base_indent=0):
        if CONST in self._modifiers:
            #output_stream.print("const ", "h_file", base_indent)
            print("Warning: const modifier used at line {} but is not yet supported".format(self.line))
        if STATIC in self._modifiers:
            output_stream.print("static ", "h_file", base_indent)

        super().codegen(output_stream, base_indent)

    @property
    def modifiers(self):
        return self._modifiers

    def analyse(self, context=None):
        super().analyse(context)
        self.context = context.build_child(MemberContext)

        return self

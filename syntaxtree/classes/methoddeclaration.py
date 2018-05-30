from syntaxtree.functiondeclaration import FunctionDeclaration


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

    @property
    def modifiers(self):
        return self._modifiers

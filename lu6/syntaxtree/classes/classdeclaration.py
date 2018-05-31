from ..astnode import ASTNode
from ...contexttable import ContextEntry

class ClassDeclaration(ASTNode):
    ClassNameVariableName = "$__compiler__classDeclarationName"
    ExtendsNameVariableName = "$__compiler__classDeclarationExtends"

    def __init__(self, line, className, extendsName, classBody):
        super().__init__(line)

        self._className = className
        self._extendsClass = extendsName
        self._classBody = classBody

    def analyse(self, context=None):
        self.context = self.create_context(context)

        self._className.analyse(self.context)
        if self._extendsClass is not None:
            self._extendsClass.analyse(self.context)

        self.context.add(ContextEntry(self.line, ClassDeclaration.ClassNameVariableName, self._className))
        self.context.add(ContextEntry(self.line, ClassDeclaration.ExtendsNameVariableName, self._extendsClass))

        if self._classBody is not None:
            self._classBody.analyse(self.context)

    def codegen(self, output_stream, base_indent=0):
        output_stream.print("class ", "h_file", base_indent)
        self._className.codegen(output_stream, base_indent)

        if self._extendsClass != "":
            output_stream.print(": public ", "h_file")
            self._extendsClass.codegen(output_stream, base_indent)

        if self._classBody is not None:
            output_stream.print(" ", "h_file")
            self._classBody.codegen(output_stream, base_indent)

        #output_stream.newline("h_file")
        output_stream.print(";", "h_file")

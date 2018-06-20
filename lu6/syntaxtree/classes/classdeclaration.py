from ..astnode import ASTNode
from ...contexttable import ContextEntry, ClassContext

class ClassDeclaration(ASTNode):
    ClassNameVariableName = "$__compiler__classDeclarationName"
    ExtendsNameVariableName = "$__compiler__classDeclarationExtends"

    def __init__(self, line, className, extendsName, classBody):
        super().__init__(line)

        self._class_name = className
        self._extends_name = extendsName
        self._class_body = classBody

    def analyse(self, context=None):
        self.context = context.build_child(ClassContext)

        self._class_name = self._class_name.analyse(self.context)
        if self._extends_name is not None:
            self._extends_name = self._extends_name.analyse(self.context)

        self.context.add(ContextEntry(self.line, ClassDeclaration.ClassNameVariableName, self._class_name))
        self.context.add(ContextEntry(self.line, ClassDeclaration.ExtendsNameVariableName, self._extends_name))

        if self._class_body is not None:
            self._class_body = self._class_body.analyse(self.context)

        return self

    def codegen(self, output_stream, base_indent=0):
        output_stream.print("class ", "h_file", base_indent)
        self._class_name.codegen(output_stream, base_indent)

        if self._extends_name is not None:
            output_stream.print(": public ", "h_file")
            self._extends_name.codegen(output_stream, base_indent)

        if self._class_body is not None:
            output_stream.print(" ", "h_file")
            self._class_body.codegen(output_stream, base_indent)

        #output_stream.newline("h_file")
        output_stream.print(";", "h_file")

    @property
    def class_body(self):
        return self._class_body

    @property
    def class_name(self):
        return self._class_name

    @property
    def extends_name(self):
        return self._extends_name

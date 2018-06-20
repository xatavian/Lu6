from .astnode import ASTNode
from ..contexttable import CompilationUnitContext


class CompilationUnit(ASTNode):

    def analyse(self, context=None):
        self.context = context.build_child(CompilationUnitContext)

        for i, typeDecl in enumerate(self._type_declarations):
            self._type_declarations[i] = typeDecl.analyse(self.context)

        return self

    def __init__(self, filename, line, includes_list, type_declarations):
        super().__init__(line)

        self._filename = filename
        self._type_declarations = type_declarations
        self._includes_list = includes_list

    def codegen(self, output_stream, base_indent=0):
        for include in self._includes_list:
            output_stream.print("#include ", "h_file", base_indent)
            include.codegen(output_stream, base_indent)
            output_stream.newline("h_file")

        output_stream.newline("h_file")
        for type_decl in self._type_declarations:
            type_decl.codegen(output_stream, base_indent)

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, value):
        self._filename = value

    @property
    def includes(self):
        return self._includes_list

    @includes.setter
    def includes(self, value):
        self._includes_list = value

    @property
    def type_declarations(self):
        return self._type_declarations

    @type_declarations.setter
    def type_declarations(self, value):
        self._type_declarations = value

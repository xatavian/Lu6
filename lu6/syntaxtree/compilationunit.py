from .astnode import ASTNode
from ..contexttable import Context


class CompilationUnit(ASTNode):

    def add_type_declaration(self, type_decl):
        self._typesDeclaration.append(type_decl)

    def analyse(self, context=None):
        self.context = Context(context)

        for i, typeDecl in enumerate(self._typesDeclaration):
            self._typesDeclaration[i] = typeDecl.analyse(self.context)

        return self

    def __init__(self, filename, line, includes_list, type_declarations):
        super().__init__(line)

        self._filename = filename
        self._typesDeclaration = type_declarations
        self._includes_list = includes_list

    def codegen(self, output_stream, base_indent=0):
        for include in self._includes_list:
            output_stream.print("#include ", "h_file", base_indent)
            include.codegen(output_stream, base_indent)
            output_stream.newline("h_file")

        output_stream.newline("h_file")
        for type_decl in self._typesDeclaration:
            type_decl.codegen(output_stream, base_indent)

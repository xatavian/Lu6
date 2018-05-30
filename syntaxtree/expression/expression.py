from ..astnode import ASTNode
from syntaxtree.general_interfaces import IGetValue


class Expression(ASTNode, IGetValue):
    def analyse(self, context=None):
        raise NotImplementedError()

    def get_value(self):
        raise NotImplementedError()

    def set_value(self, value):
        raise NotImplementedError()

    def codegen(self, output_stream, base_indent=0):
        # Never generating the value of a expression.
        # All objects that need the result of the evaluation of an expression
        # must use get_value() instead
        output_stream.print(self.get_value(), "h_file", base_indent)

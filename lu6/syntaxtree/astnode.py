from ..contexttable import Context


class ASTNode(object):
    def __init__(self, line):
        self._line = line
        self._context = None

    @property
    def context(self):
        return self._context

    @context.setter
    def context(self, value):
        self._context = value

    @property
    def line(self):
        return self._line

    @staticmethod
    def create_context(parent=None):
        return Context(parent)

    def analyse(self, context=None):
        raise NotImplementedError()

    def codegen(self, output_stream, base_indent=0):
        raise NotImplementedError()

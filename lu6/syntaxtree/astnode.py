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
        """
        Analysis of the AST Node.
        The method must allow tree rewriting by returning a reference
        to the resulting node of the analysis. This result can obviously
        be the node itself if no tree rewriting is necessary.
        """
        raise NotImplementedError()

    def codegen(self, output_stream, base_indent=0):
        raise NotImplementedError()


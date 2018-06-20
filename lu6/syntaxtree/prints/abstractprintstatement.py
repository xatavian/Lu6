from ..statements.statement import Statement

class AbstractPrintStatement(Statement):
    """
    Base class for all the statements that directly print code to the output
    """

    def __init__(self, line, text):
        super().__init__(line)

        self._text = text

    def analyse(self, context=None):
        self.context = context
        self._text = self._text.analyse(self.context)
        return self

    def codegen(self, output_stream, base_indent=0):
        raise NotImplementedError()

    def preCodegen(self, categories=None):
        pass

    @property
    def text(self):
        return self._text

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "PrintStatement ({type}): {text}".format(type=type(self), text=self._text)

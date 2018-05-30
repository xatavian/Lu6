from .astnode import ASTNode
import tokens.tokens as tokens
from .variable import Variable


class LineStatement(ASTNode):

    def __init__(self, line):
        super().__init__(line)
        self._words = []

    def isEmpty(self):
        for word in self._words:
            if isinstance(word, Variable):
                return False
            elif not word.has_type_one_of(tokens.WhitespaceTokens):
                return False
        return True

    def codegen(self, output_stream, base_indent=0):
        for word in self._words:
            if isinstance(word, Variable):
                output_stream.print(word.get_value(), "h_file", base_indent)
            else:
                output_stream.print(word.image, "h_file", base_indent)

    def analyse(self, context=None):
        self.context = context
        for word in self._words:
            if isinstance(word, Variable):
                word.analyse(context)

    def add(self, word):
        self._words.append(word)

    def __str__(self):
        return "".join([str(id.image) for id in self._words])
from lu6.tokens import tokens


class Modifier(object):

    def __init__(self, type):
        super().__init__()
        self._type = type

    @property
    def type(self):
        return self._type

    @property
    def value(self):
        return self._type.image

    def codegen(self, output_stream, base_indent=0):
        pass

    def analyse(self, context=None):
        return self


PUBLIC = Modifier(tokens.ReservedWordsTokens.PublicToken)
PRIVATE = Modifier(tokens.ReservedWordsTokens.PrivateToken)
PROTECTED = Modifier(tokens.ReservedWordsTokens.ProtectedToken)
STATIC = Modifier(tokens.ReservedWordsTokens.StaticToken)
CONST = Modifier(tokens.ReservedWordsTokens.ConstToken)
REFERENCE = Modifier(tokens.SpecialTokens.AmpersandToken)
POINTER = Modifier(tokens.SpecialTokens.StarToken)
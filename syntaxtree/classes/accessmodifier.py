import tokens.tokens


class AccessModifier(object):

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
        pass


PUBLIC = AccessModifier(tokens.ReservedWordsTokens.PublicToken)
PRIVATE = AccessModifier(tokens.ReservedWordsTokens.PrivateToken)
PROTECTED = AccessModifier(tokens.ReservedWordsTokens.ProtectedToken)
STATIC = AccessModifier(tokens.ReservedWordsTokens.StaticToken)
CONST = AccessModifier(tokens.ReservedWordsTokens.ConstToken)


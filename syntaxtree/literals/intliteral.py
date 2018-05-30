from .literal import Literal

class IntLiteral(Literal):
    def __init__(self, line, string_value):
            super().__init__(line, int(str(string_value.image)))

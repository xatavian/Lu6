from .astnode import ASTNode
from ..tokens import tokens
from ..exceptions import TypeCheckingException


class QualifiedIdentifier(ASTNode):
    def __init__(self, line):
        super().__init__(line)
        self._identifiers = []
        self._variable_identifier_positions = []

    @property
    def identifiers(self):
        return self._identifiers if len(self._identifiers) > 0 else self._identifiers

    @property
    def is_field_selection(self):
        return 0 in self._variable_identifier_positions and \
               len(self._identifiers) > 2

    def add_identifier(self, identifier, separator_type = None):
        if separator_type is not None:
            self._identifiers.append(separator_type)

        self._identifiers.append(identifier)
        if identifier.has_type(tokens.IdentifierTokens.VariableIdentifier.value):
            self._variable_identifier_positions.append(len(self._identifiers) - 1)

    def codegen(self, output_stream, base_indent=0):
        output_stream.print(self.get_value(), "h_file", base_indent)

    def get_value(self):
        result = ""
        for word in self._identifiers:
            result += str(word.image)
        return result

    def get_raw_value(self):
        return "".join(str(token.image) for token in self._identifiers)

    def analyse(self, context=None):
        self.context = context
        for var_pos in self._variable_identifier_positions:
            variable = self._identifiers[var_pos]
            if variable.image not in context:
                raise TypeCheckingException("{} was not declared in this scope".format(variable.image), self.line)

        return self

    def __str__(self):
        return "".join(str(id.image) for id in self._identifiers)

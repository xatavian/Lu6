from .astnode import ASTNode
from .general_interfaces import IGetValue

from ..contexttable import ContextEntry
from ..exceptions import TemplateEngineException


class Variable(IGetValue, ASTNode):
    def __init__(self, line, name):
        super().__init__(line)
        self._name = name
        self._corresponding_entry = None

    @property
    def name(self):
        return self._name

    def _is_valid(self):
        return self.get_entry() is not None

    def set_value(self, value):
        self._corresponding_entry.value = value

    @staticmethod
    def from_qualified_identifier(qualified_identifier):
        result = Variable(qualified_identifier.line, qualified_identifier.get_raw_value())
        return result

    def get_value(self):
        if self._corresponding_entry is not None:
            return self._corresponding_entry.value
        return None

    def get_entry(self):
        if self._corresponding_entry is None:
            self._corresponding_entry = self.context.get_value(self.name)
        return self._corresponding_entry

    def analyse(self, context=None):
        if self.context is None:
            self.context = context

        if not self._is_valid():
            raise TemplateEngineException("{} has not been declared in this scope".format(self.name),
                                          self.line)

    def analyse_as_lhs(self, context=None):
        if self.context is None:
            self.context = context

        if not self._is_valid():
            self._corresponding_entry = ContextEntry(self.line, self.name)
            context.add(self._corresponding_entry)

    def update_value(self, value):
        if self._corresponding_entry is not None:
            self._corresponding_entry.value = value

    def codegen(self, output_stream, base_indent=0):
        output_stream.print(self.get_value(), "h_file", base_indent)

    def __str__(self):
        return self.name

from ..tokens import Token
from copy import deepcopy


class Context(object):

    def add(self, member):
        self._localentries[member.name] = member

    @property
    def childcontexts(self):
        return self._childcontexts

    @childcontexts.setter
    def childcontexts(self, value):
        self._childcontexts = value

    def __contains__(self, name):
        if isinstance(name, str) and name in self._localentries:
            return True
        elif not isinstance(name, str) and str(name) in self._localentries:
            return True
        elif self._parentcontext is not None:
            return name in self._parentcontext
        return False

    def __init__(self, in_statement_context, parentcontext=None):
        self._parentcontext = parentcontext
        self._childcontexts = []
        self._localentries = dict()
        self._in_statement_context = in_statement_context

    @property
    def in_statement_context(self):
        return self._in_statement_context

    @property
    def localentries(self):
        return self._localentries

    @property
    def parentcontext(self):
        return self._parentcontext

    @parentcontext.setter
    def parentcontext(self, value):
        self._parentcontext = value

    def get_value(self, name):
        name_ = name
        if isinstance(name, Token):
            name_ = name.image

        if name_ in self._localentries:
            return self._localentries[name_]
        elif self._parentcontext is not None:
            return self._parentcontext.get_value(name_)

        return None

    def build_child(self, child_type):
        return child_type(self.in_statement_context, self)

    def copy(self):
        """
        Returns a copy of the context without any parent context
        """
        result = type(self)(self.in_statement_context)
        result._localentries = deepcopy(self.localentries)

        return result

class CompilationUnitContext(Context):
    pass


class ClassContext(Context):
    pass


class StatementContext(Context):
    def __init__(self, in_statement_context, parentcontext=None):
        super().__init__(True, parentcontext)


class BlockContext(Context):
    pass


class MemberContext(Context):

    @staticmethod
    def pre_codegen_rebuild(source_context):
        if not source_context.in_statement_context:
            return source_context

        source_context.localentries.clear()
        parent = source_context.parentcontext
        while parent is not None and parent.in_statement_context:
            for entry in parent.localentries:
                source_context.add(deepcopy(entry))

            parent = parent.in_statement_context

        return source_context

from ..tokens import Token


class Context(object):

    def __init__(self, parentcontext=None):
        self._parentcontext = parentcontext
        self._localentries = dict()

    def add(self, member):
        self._localentries[member.name] = member

    def __contains__(self, name):
        if isinstance(name, str) and name in self._localentries:
            return True
        elif not isinstance(name, str) and str(name) in self._localentries:
            return True
        elif self._parentcontext is not None:
            return name in self._parentcontext
        return False

    def get_value(self, name):
        name_ = name
        if isinstance(name, Token):
            name_ = name.image

        if name_ in self._localentries:
            return self._localentries[name_]
        elif self._parentcontext is not None:
            return self._parentcontext.get_value(name_)

        return None

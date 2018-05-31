from ..exceptions import ParserEngineException
from ..scanner import FileScanner

class ParserHelper(object):

    def __init__(self, scanner=None):
        self._scanner = scanner
        self._saved_tokens = []
        self._current_token = None
        self._in_print_statement = False

    @property
    def current_line(self):
        return self._scanner.current_line

    @property
    def current_token(self):
        return self._current_token

    def current_token_is(self, tKind):
        if self.current_token is None:
            return False
        return self._current_token.has_type(tKind.value)

    def current_token_is_one_of(self, tKinds):
        for tKind in tKinds:
            if self.current_token_is(tKind):
                return True
        return False

    def current_token_must_be(self, tKind):
        if not self._current_token.has_type(tKind.value):
            raise ParserEngineException("Expected token to be of type {} but "
                                        "type {} was encountered ({})".format(
                                                tKind.name, self.current_token.type.name,
                                                self.current_token.image
                                        ),
                                        self._scanner.current_line)

    def current_token_must_be_one_of(self, tKinds):
        for tKind in tKinds:
            try:
                self.current_token_must_be(tKind)
                return
            except ParserEngineException:
                pass

        raise ParserEngineException("Expected token to be of type {} but "
                                    "type {} ({}) was encountered".format(
            " / ".join([tKind.value.name for tKind in tKinds]),
            self.current_token.type.name,
            self.current_token.image),
            self._scanner.current_line)

    def get_next_token(self):
        if len(self._saved_tokens) > 0:
            self._current_token = self._saved_tokens.pop()
            return self.current_token

        if self._scanner is not None:
            self._current_token = self._scanner.next_token()

        return self._current_token

    @property
    def in_print_statement(self):
        return self._in_print_statement

    @in_print_statement.setter
    def in_print_statement(self, value):
        self._in_print_statement = value

    @property
    def read_whitespaces(self):
        return self._scanner.read_whitespaces

    @read_whitespaces.setter
    def read_whitespaces(self, value):
        self._scanner.read_whitespaces = value

    def save_token(self, token):
        self._saved_tokens.append(token)

    @property
    def scanner(self):
        return self._scanner

    @property
    def filename(self):
        if isinstance(self._scanner, FileScanner):
            return self._scanner.filename
        return "<INTERNAL_STRING>"

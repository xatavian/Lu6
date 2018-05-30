from .parserhelper import ParserHelper


class Parser(object):
    def __init__(self, parser_helper=None):
        self._parser_helper = parser_helper

    @property
    def parserhelper(self):
        return self._parser_helper

    @property
    def current_token(self):
        return self._parser_helper.current_token

    def current_token_is(self, tKind):
        return self._parser_helper.current_token_is(tKind)

    def current_token_is_one_of(self, tKinds):
        return self._parser_helper.current_token_is_one_of(tKinds)

    def current_token_must_be(self, tKind):
        self._parser_helper.current_token_must_be(tKind)

    def current_token_must_be_one_of(self, tKinds):
        self._parser_helper.current_token_must_be_one_of(tKinds)

    def get_next_token(self):
        return self._parser_helper.get_next_token()

    def save_token(self, token):
        self._parser_helper.save_token(token)

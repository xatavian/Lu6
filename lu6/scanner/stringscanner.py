from .scanner import Scanner


class StringScanner(Scanner):
    """
    Scanner that can tokenize content coming from a string
    """

    def __init__(self, string=None):
        super().__init__()
        self._source = string
        self._counter = 0

    def next_from_input_source(self):
        if self._counter < len(self._source):
            result = self._source[self._counter]
            self._counter += 1
            return result
        return None

    def cleanup(self):
        pass

    def on_reset(self):
        self._counter = 0

    def set_source(self, source_string):
        self._source = source_string

from .scanner import Scanner


class FileScanner(Scanner):
    """
    Scanner that can tokenize content coming from a file.
    """
    def __init__(self, filename=None):
        super().__init__()
        self._sourcefile = None
        self._filename = filename

        if filename is not None:
            self.choose_file(filename)

    def choose_file(self, filename):
        if self._sourcefile is not None:
            self._sourcefile.close()

        try:
            self._sourcefile = open(filename, "r")
            self.reset()
            return self
        except IOError:
            raise

    def next_from_input_source(self):
        if self._sourcefile is None:
            return None

        result = self._sourcefile.read(1)
        if len(result) == 0:
            return None

        return result

    @property
    def filename(self):
        return self._filename if self._filename is not None else ""

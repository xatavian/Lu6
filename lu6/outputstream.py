import sys
from .tokens import Token
from .syntaxtree.literals import Literal
from io import StringIO


class OutputStreamFactory(object):
    open_streams = []

    @staticmethod
    def to_file(filename):
        stream = OutputStream()
        stream._type = OutputStream.TO_FILE
        try:
            stream._h_stream = open("{}.h".format(filename), "w")
            stream._cpp_stream = open("{}.cpp".format(filename), "w")
        except IOError:
            print("Opening an OutputStream to {} has failed".format(filename))
        else:
            OutputStreamFactory.open_streams.append(stream)
            return stream

    @staticmethod
    def to_stdout():
        stream = OutputStream()
        stream._type = OutputStream.TO_STDOUT
        stream._h_stream = StringIO()
        stream._cpp_stream = StringIO()
        OutputStreamFactory.open_streams.append(stream)
        return stream

    @staticmethod
    def to_string():
        stream = OutputStream()
        stream._type = OutputStream.TO_STRING
        stream._h_stream = StringIO()
        stream._cpp_stream = StringIO()

        OutputStreamFactory.open_streams.append(stream)
        return stream

    @staticmethod
    def cleanup():
        for stream in OutputStreamFactory.open_streams:
            if hasattr(stream, "close"):
                stream.close()


class OutputStream:
    TO_STRING = "TO_STRING"
    TO_FILE = "TO_FILE"
    TO_STDOUT = "TO_STDOUT"

    @property
    def type(self):
        return self._type

    def cleanup(self):
        if self._h_stream is not None:
            self._h_stream.close()
        if self._cpp_stream is not None:
            self._cpp_stream.close()

    def __init__(self):
        self._h_stream = None
        self._cpp_stream = None
        self._h_is_newline = True
        self._cpp_is_newline = True
        self._type = OutputStream.TO_STRING

    @property
    def h_stream(self):
        return self._h_stream

    @property
    def cpp_stream(self):
        return self._h_stream

    @property
    def h_is_newline(self):
        return self._h_is_newline

    @property
    def cpp_is_newline(self):
        return self._cpp_is_newline

    def newline(self, stream_type, amount=1):
        stream, _ , update_nli = self.get_stream(stream_type)
        if stream is None:
            return

        update_nli(True)
        for i in range(amount):
            OutputStream.write(stream, "\n")

    def print(self, string, stream_type, base_indent=0):
        stream, new_line_indicator, update_nli = self.get_stream(stream_type)
        if stream is None:
            return

        OutputStream.print_indent(stream, new_line_indicator, base_indent)

        OutputStream.write(stream, string)
        if string == "\n":
            update_nli(True)
        else:
            update_nli(False)

    @staticmethod
    def print_indent(stream, new_line_indicator, base_indent):
        if new_line_indicator:
            OutputStream.write(stream, "".join(" " for i in range(base_indent)))

    def get_stream(self, stream_type):
        if stream_type == "h_file":
            return self._h_stream, self._h_is_newline, lambda value: setattr(self, "_h_is_newline", value)
        elif stream_type == "cpp_file":
            return self._cpp_stream, self._cpp_is_newline, lambda value: setattr(self, "_cpp_is_newline", value)
        return None, None, None

    @staticmethod
    def write(stream, string):
        if isinstance(string, Token):
            stream.write(string.image)
        elif isinstance(string, Literal):
            stream.write(string.value.image)
        else:
            stream.write(str(string))

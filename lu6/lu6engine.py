from .scanner import FileScanner, StringScanner
from .contexttable import Context, ContextEntry
from .outputstream import OutputStreamFactory
from .parserengine import CompilationUnitParser
from .exceptions import TemplateEngineException


class Lu6Engine(object):
    """
    Wrapper class taking care of all the work flow of the Lu6 TemplateEngine
    """

    FILE = "Lu6_Engine, Source=File"
    STRING = "Lu6_Engine, Source=String"

    OUTPUT_TO_STRING = "Lu6_Engine, Output=String"
    OUTPUT_TO_STDOUT = "Lu6_Engine, Output=StdOut"
    OUTPUT_TO_FILE   = "Lu6_Engine, Output=File"

    def __init__(self):
        self._source_type = None
        self._content = None
        self._external_content = Context()
        self._output_file = None
        self._output_type = None

    def set_source(self, source_type, content):
        if source_type not in ( Lu6Engine.FILE, Lu6Engine.STRING ):
            raise TemplateEngineException("Unrecognized source type was provided", -1)
        self._source_type = source_type
        self._content = content

    def set_output(self, output_type, output_file=None):
        if output_type not in (Lu6Engine.OUTPUT_TO_FILE, Lu6Engine.OUTPUT_TO_STDOUT, Lu6Engine.OUTPUT_TO_STRING):
            raise TemplateEngineException("Unrecognized output type was provided", -1)
        elif output_type == Lu6Engine.OUTPUT_TO_FILE and output_file is None:
            raise TemplateEngineException("No output file was specified", -1)

        self._output_type = output_type
        self._output_file = output_file

    def generate(self):
        if self._source_type == Lu6Engine.FILE:
            scanner = FileScanner()
            scanner.choose_file(self._content)

        elif self._source_type == Lu6Engine.STRING:
            scanner = StringScanner()
            scanner.set_source(self._content)
        else:
            raise TemplateEngineException("Lu6Engine is incorrectly configured. Generation is aborted.", -1)

        # Parsing
        parser = CompilationUnitParser(scanner)
        comp_unit = parser.parse_compilation_unit()

        comp_unit.analyse(self._external_content)

        # Code generation
        # TODO: customize output
        if self._output_type == Lu6Engine.OUTPUT_TO_STDOUT:
            stream = OutputStreamFactory.to_stdout()
        elif self._output_type == Lu6Engine.OUTPUT_TO_STRING:
            stream = OutputStreamFactory.to_string()
        else:
            stream = OutputStreamFactory.to_file(self._output_file)

        comp_unit.codegen(stream)
        if self._output_type == Lu6Engine.OUTPUT_TO_STRING:
            result_cpp, result_h = stream.cpp_stream.getvalue(), stream.h_stream.getvalue()
            OutputStreamFactory.cleanup()
            scanner.cleanup()
            return result_cpp, result_h

        OutputStreamFactory.cleanup()
        scanner.cleanup()

    def add_in_context(self, key, value):
        """
        Key must start with $
        """
        if not isinstance(key, str):
            raise TemplateEngineException("External content must have keys of type str")
        elif not key.startswith("$"):
            raise TemplateEngineException("External content must have keys of starting with \"$\"")
        else:
            self._external_content.add(ContextEntry(-1, key, value))

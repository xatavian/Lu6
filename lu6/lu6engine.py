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


    def __init__(self):
        self._source_type = None
        self._content = None
        self._external_content = Context()

    def set_source(self, source_type, content):
        if source_type not in ( Lu6Engine.FILE, Lu6Engine.STRING ):
            raise TemplateEngineException("Unrecognized source type was provided", -1)
        self._source_type = source_type
        self._content = content

    def generate(self):
        scanner = None
        if self._source_type == Lu6Engine.FILE:
            scanner = FileScanner()
            scanner.choose_file(self._content)

        elif self._source_type == Lu6Engine.STRING:
            scanner = StringScanner()
            scanner.set_source(self._content)
        else:
            raise TemplateEngineException("Lu6Engine is incorrectly configured. Generation is aborted.")

        # Parsing
        parser = CompilationUnitParser(scanner)
        comp_unit = parser.parse_compilation_unit()

        comp_unit.analyse(self._external_content)

        # Code generation
        # TODO: customize output
        stream = OutputStreamFactory.to_stdout()
        comp_unit.codegen(stream)

        OutputStreamFactory.cleanup()

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

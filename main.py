from outputstream import OutputStreamFactory
from scanner import FileScanner
from parserengine import CompilationUnitParser
from contexttable import Context, ContextEntry

if __name__ == "__main__":

    # Scanning
    scanner = FileScanner()
    scanner.choose_file("example/scan.txt")

    # Parsing
    parser = CompilationUnitParser(scanner)
    comp_unit = parser.parse_compilation_unit()

    context = Context()
    context.add(ContextEntry(0, "$test", "Plouf"))

    comp_unit.analyse(context)

    # Code generation
    stream = OutputStreamFactory.to_stdout()
    comp_unit.codegen(stream)

    OutputStreamFactory.cleanup()

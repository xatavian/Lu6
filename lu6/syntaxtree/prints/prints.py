from .abstractprintstatement import AbstractPrintStatement
# from scanner.scannerhelper import ScannerHelper


class PrintStatement(AbstractPrintStatement):
    def codegen(self, output_stream, base_indent):
        self.text.codegen(output_stream, base_indent)

class PrintlnStatement(AbstractPrintStatement):
    def codegen(self, output_stream, base_indent):
        self.text.codegen(output_stream, base_indent)
        output_stream.newline("h_file")

class InstructionStatement(AbstractPrintStatement):
    def codegen(self, output_stream, base_indent):
        self.text.codegen(output_stream, base_indent)
        output_stream.print(";", "h_file", base_indent)
        output_stream.newline("h_file")

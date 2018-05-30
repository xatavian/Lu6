from .literal import Literal


class StringLiteral(Literal):
    def codegen(self, output_stream, base_indent=0):
        output_stream.print(self.value.image.strip("\""), "h_file", base_indent)

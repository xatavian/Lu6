from .literal import Literal


class StringLiteral(Literal):
    def codegen(self, output_stream, base_indent=0):
        start_index = 1 if self.value.image[0] == "\"" else 0
        end_index   = -1 if self.value.image[-1] == "\"" else len(self.value.image)

        output_stream.print(self.value.image[start_index:end_index], "h_file", base_indent)

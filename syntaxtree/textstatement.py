from .astnode import ASTNode
from .general_interfaces import IGetValue, IValueHolder
from .variable import Variable
from tokens.tokens import Token
from scanner.scannerhelper import ScannerHelper


class TextStatement(ASTNode):
    def __init__(self, line, text = None):
        super().__init__(line)
        if text is None:
            self._text = []
        else:
            self._text = text

        self._words = []

    def codegen(self, output_stream, base_indent=0):
        self._text.codegen(output_stream, base_indent)
        # for word in self._words:
        #     if isinstance(word, IGetValue):
        #         output_stream.print(word.get_value(), "h_file", base_indent)
        #     elif isinstance(word, IValueHolder):
        #         output_stream.print(word.value, "h_file", base_indent)
        #     elif isinstance(word, Token):
        #         output_stream.print(word.image, "h_file", base_indent)
        #     else:
        #         output_stream.print(word, "h_file", base_indent)
        #
        #     # output_stream.newline("h_file")

    def analyse(self, context=None):
        self.context = context
        temp_string = ""
        scanning_ongoing = False
        scanning_type = 0 # 0 = normal string, 1 = var name
        i = 0
        self._text.analyse(self.context)

        # while i < len(self._text.image):
        #     char = self._text.image[i]
        #     if scanning_ongoing:
        #         if scanning_type == 0 and char == "$":
        #             self._words.append(temp_string)
        #             scanning_ongoing = False
        #         elif scanning_type == 1 and not ScannerHelper.is_identifier(char):
        #             w = Variable(self.line, temp_string)
        #             w.analyse(self.context)
        #
        #             self._words.append(w)
        #             scanning_ongoing = False
        #         else:
        #             temp_string += char
        #             i += 1
        #     else:
        #         scanning_ongoing = True
        #         if ScannerHelper.is_variable_identifier(char):
        #             temp_string = "$"
        #             scanning_type = 1
        #         else:
        #             temp_string = char
        #             scanning_type = 0
        #         i += 1
        #
        # if scanning_type == 0:
        #     self._words.append(temp_string)
        # else:
        #     w = Variable(self.line, temp_string)
        #     w.analyse(self.context)
        #
        #     self._words.append(w)

    def __str__(self):
        result = "TextStatement"
        return result.format()
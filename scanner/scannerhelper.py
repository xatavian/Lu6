import tokens.tokens as tokens
import re


class ScannerHelper(object):
    identifier_regexp = re.compile("\$?([A-Za-z]|_)([A-Za-z]|\d|_)*")
    string_literal_regexp = re.compile("^\"[^\"]*\"$")

    @staticmethod
    def is_instruction(char):
        return char.startswith("@")
        # return any(str(word.value.image).startswith(str(char)) for word in tokens.ReservedWordsTokens)

    @staticmethod
    def is_identifier(string):
        return ScannerHelper.identifier_regexp.fullmatch(string) is not None

    @staticmethod
    def is_variable_identifier(string):
        return ScannerHelper.is_identifier(string) and string.startswith("$")

    @staticmethod
    def is_literal(token):
        return ScannerHelper.is_number(token) or \
                ScannerHelper.is_string_literal(token)

    @staticmethod
    def is_number(string):
        # It's an integer everything is fine
        if string.isdigit():
            return True

        # Test for floating point values
        try:
            float(string)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_string_literal(string):
        return ScannerHelper.string_literal_regexp.fullmatch(string) is not None

    # def read_until_triple_quotes_string_end(self):
    #     result = ""
    #     temp = self.next_char()
    #     while (not temp == "\"\"\"") and ( not ScannerHelper.is_eof(temp)) :
    #         if len(temp) == 3:
    #             result += temp[0]
    #             temp = Char(temp[1:])
    #         temp += self.next_char()
    #
    #     return result
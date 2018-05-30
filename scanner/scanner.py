from exceptions import EOFException, InvalidLiteralException, UnrecognizedTokenException
from .scannerhelper import ScannerHelper
from tokens import tokens


class Scanner(object):
    def __init__(self):
        self._current_line = 0
        self._saved_char = []
        self._eof_reached = False

    @property
    def current_line(self):
        return self._current_line + 1

    def next_from_input_source(self):
        """
        Returns the next character from the input source. If EOF has been reached,
        None must be returned.
        """
        raise NotImplementedError()

    def next_char(self):
        if len(self._saved_char) > 0:
            return self._saved_char.pop()
        else:
            char = self.next_from_input_source()

        if char is None:
            raise EOFException(self.current_line, "EOF has been reached")

        if char == "\n":
            self.update_line()
        return char

    def next_token(self):
        # -- Skip whitespaces and comments
        while True:
            self.skip_whitespace()
            if not self.skip_comments():
                break

        try:
            char = self.next_char()
            self.save_char(char)
        except EOFException:
            return tokens.get_eof_token(self.current_line)

        try:
            # -- Match special tokens
            i = 2
            while i > 0:
                src_string = ""
                for j in range(i):
                    src_string += self.next_char()

                if tokens.SpecialTokens.has(src_string):
                    return tokens.get_special_token(self.current_line, src_string)
                else:
                    for c in reversed(src_string):
                        self.save_char(c)
                i -= 1

            # -- Match instructions keywords
            src_string = self.next_char()
            if src_string == "@":
                src_string += self.read_identifier()
                if tokens.ReservedWordsTokens.has(src_string):
                    return tokens.get_reserved_word_token(self.current_line, src_string)
                else:
                    raise UnrecognizedTokenException("{} is not a valid token".format(src_string), self.current_line)

            # -- Match string literal
            elif src_string == "\"":
                #  TODO: Match enhanced string literals
                self.save_char(src_string)
                src_string = self.read_string_literal()
                return tokens.get_literal(self.current_line, src_string)
            elif src_string.isdigit() or src_string == ".":
                self.save_char(src_string)
                src_string = self.read_number_literal()
                return tokens.get_literal(self.current_line, src_string)

            # -- Match non-instruction keywords or identifiers
            else:
                self.save_char(src_string)
                src_string = self.read_identifier()
                if tokens.ReservedWordsTokens.has(src_string):
                    return tokens.get_reserved_word_token(self.current_line, src_string)
                else:
                    return tokens.get_identifier_token(self.current_line, src_string)
        except EOFException:
            raise EOFException(self.current_line, "EOF was unexpectedly reached while scanning tokens")

    def skip_comments(self):
        """
        :return: True if a single line comment has been ignored, False otherwise
        """
        try:

            char = self.next_char()
            if char != "@":
                self.save_char(char)
                return False

            char += self.next_char() + self.next_char()
            if char == "@//":
                # Single line comment detected
                char = self.next_char()
                while char != "\n":
                    char = self.next_char()

            elif char == "@/*":
                # Multi line comment detected
                char = self.next_char() + self.next_char() + self.next_char()
                while char != "*/@":
                    char = char[1:] + self.next_char()
                return True

            else:  # It is not a comment, we save all the characters we have already consumed.
                for c in reversed(char):
                    self.save_char(c)
                return False

            return True

        except EOFException:
            return False

    def read_until_whitespace(self):
        result = ""
        temp = self.next_char()
        while not temp.isspace():
            result += str(temp)
            temp = self.next_char()

        self.save_char(temp)
        return result

    def read_identifier(self):
        result = self.next_char()
        if result == "$":
            result += self.next_char()

        while ScannerHelper.is_identifier(result):
            result += self.next_char()

        self.save_char(result[-1])
        return result[:-1]

    def read_number_literal(self):
        result = self.next_char()

        while ScannerHelper.is_number(result):
            temp = self.next_char()
            if not temp.isspace():
                result += temp
            else:
                self.save_char(temp)
                return result

        self.save_char(result[-1])
        return result[:-1]

    def read_string_literal(self):
        result = ""
        temp = self.next_char()

        if temp != "\"":
            raise InvalidLiteralException("Trying to tokenize a invalid string literal")

        while not ScannerHelper.is_string_literal(result):
            if temp.startswith("\\"):
                pass  # TODO: handle escaped characters
            else:
                result += temp
                temp = self.next_char()
        
        self.save_char(temp)
        return result

    def read_enhanced_string_literal(self):
        pass  # TODO: Tokenize Enhanced string literals

    def skip_whitespace(self):
        try:
            char = self.next_char()

            while char.isspace():
                char = self.next_char()
            self.save_char(char)
        except EOFException:
            pass

    def save_char(self, char):
        self._saved_char.append(char)

    def update_line(self):
        self._current_line += 1

    def reset(self):
        self.on_reset()
        self._eof_reached = False
        self._current_line = 0

    def on_reset(self):
        pass



import unittest

from lu6.scanner import StringScanner
from lu6.parserengine import ParserHelper, PrintParser
from lu6.syntaxtree.literals import StringLiteral
from lu6.syntaxtree.prints import PrintStatement, PrintlnStatement, InstructionStatement
from lu6.outputstream import OutputStreamFactory

class PrintTest(unittest.TestCase):
    def test_print_statement(self):
        scanner = StringScanner()
        scanner.set_source("@print \"hello\"")

        parser = PrintParser(ParserHelper(scanner))
        parser.get_next_token()

        ast = parser.parse_print_statement()

        self.assertIsInstance(ast, PrintStatement)
        self.assertIsInstance(ast.text, StringLiteral)

        output = OutputStreamFactory.to_string()
        ast.codegen(output, 0)

        self.assertEqual(output.h_stream.getvalue(), "hello")

    def test_println_statement(self):
        scanner = StringScanner()
        scanner.set_source("@println \"hello\"")

        parser = PrintParser(ParserHelper(scanner))
        parser.get_next_token()

        ast = parser.parse_println_statement()

        self.assertIsInstance(ast, PrintlnStatement)
        self.assertIsInstance(ast.text, StringLiteral)

        output = OutputStreamFactory.to_string()
        ast.codegen(output, 0)

        self.assertEqual(output.h_stream.getvalue(), "hello\n")

    def test_instruction_statement(self):
        scanner = StringScanner()
        scanner.set_source("@instruction \"hello\"")

        parser = PrintParser(ParserHelper(scanner))
        parser.get_next_token()

        ast = parser.parse_instruction_statement()

        self.assertIsInstance(ast, InstructionStatement)
        self.assertIsInstance(ast.text, StringLiteral)

        output = OutputStreamFactory.to_string()
        ast.codegen(output, 0)

        self.assertEqual(output.h_stream.getvalue(), "hello;\n")

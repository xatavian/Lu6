import unittest
from lu6 import Lu6Engine


class ExampleTest(unittest.TestCase):
    def test_example_file(self):
        engine = Lu6Engine()

        engine.set_source(Lu6Engine.FILE, "./test/example/scan.txt")
        engine.set_output(Lu6Engine.OUTPUT_TO_STRING)

        engine.add_in_context("$frame", {"name": "TestClass"})
        engine.generate()

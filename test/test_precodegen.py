import unittest
from lu6 import Lu6Engine


class PreCodegenTest(unittest.TestCase):
    def test_precodegen(self):
        template = """
        @class PreCodegenClass {
            @method:private void test();
            @method:public  void "hello" + $i + "test" ();
            
            @attribute std::string myAwesomeAttribute;
        };
        """

        engine = Lu6Engine()
        engine.set_source(Lu6Engine.STRING, template)
        engine.set_output(Lu6Engine.OUTPUT_TO_STDOUT)
        engine.add_in_context("$i", 0)
        engine.generate()


import context
import unittest

from example import ExampleTest

if __name__ == "__main__":
    suite = unittest.TestSuiet()
    suite.addTest(ExampleTest())
    unittest.TextTestRunner().run(suite)

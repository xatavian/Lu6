import sys
sys.path.append("..")

from scanner import StringScanner
from test.statements import StatementTester

if __name__ == "__main__":
    scanner = StringScanner()
    scanner.set_source("2 + 2")
    StatementTester(scanner).start()

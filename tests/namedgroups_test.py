"""
Testing some aspects of named groups
"""

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import re2 as re
import unittest

class NamedGroupTests(unittest.TestCase):

    def test_basic(self):
        m = re.match(r"(?P<first_name>\w+) (?P<last_name>\w+)", "Malcolm Reynolds")
        self.assertEqual(m.start("first_name"), 0)
        self.assertEqual(m.start("last_name"), 8)

        self.assertEqual(m.span("last_name"), (8, 16))
        self.assertEqual(m.regs, ((0, 16), (0, 7), (8, 16)))

    def test_positions(self):
        # Make sure positions are converted properly for unicode 

        m = re.match(r"(?P<first_name>\w+) (?P<last_name>\w+)",
            '\u05d9\u05e9\u05e8\u05d0\u05dc \u05e6\u05d3\u05d5\u05e7',
            re.UNICODE)
        self.assertEqual(m.start("first_name"), 0)
        self.assertEqual(m.start("last_name"), 6)
        self.assertEqual(m.end("last_name"), 10)
        self.assertEqual(m.regs, ((0, 10), (0, 5), (6, 10)))
        self.assertEqual(m.span(2), (6, 10))
        self.assertEqual(m.span("last_name"), (6, 10))


if __name__ == "__main__":
    unittest.main(verbosity=2)

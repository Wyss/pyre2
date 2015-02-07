
"""
Match Expand Tests

Match objects have an .expand() method which allows them to
expand templates as if the .sub() method was called on the pattern.
"""

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import re2 as re
import unittest

class MatchExpandTests(unittest.TestCase):

    def test_basic(self):
        m = re.match(r"(\w+) (\w+)\W+(?P<title>\w+)", "Isaac Newton, physicist")
        self.assertEqual(m.expand(r"\2, \1"), 'Newton, Isaac')
        self.assertEqual(m.expand(r"\1 \g<title>"), 'Isaac physicist')
        self.assertEqual(m.expand(r"\0 \1 \2"), '\x00 Isaac Newton')
        self.assertEqual(m.expand(r"\3"), 'physicist')

if __name__ == "__main__":
    unittest.main(verbosity=2)

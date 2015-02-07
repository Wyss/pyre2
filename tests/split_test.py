"""
Split tests

This one tests to make sure that utf8 data is parsed correctly.
"""

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import re2 as re
import unittest

class SplitTests(unittest.TestCase):

    def test_basic(self):
        a = '我很好, 你呢?'
        self.assertEqual(re.split(' ', a),
            ['\u6211\u5f88\u597d,', '\u4f60\u5462?'])


if __name__ == "__main__":
    unittest.main(verbosity=2)


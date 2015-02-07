"""
Here are some tests to make sure that utf-8 works
"""

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import re2 as re
import unittest

class UnicodeTests(unittest.TestCase):

    def test_basic(self):
        a = '\u6211\u5f88\u597d'
        c = re.compile(a[0], re.UNICODE)
        self.assertEqual(c.search(a).group(), '\u6211')

    def test_stickyness(self):
        # Test unicode stickyness
        self.assertEqual(re.sub('x', 'y', 'x'), 'y')
        self.assertEqual(re.findall('.', 'x'), ['x'])
        self.assertEqual(re.split(',', '1,2,3'), ['1', '2', '3'])
        self.assertEqual(re.search(u'(\\d)', '1').group(1), '1')
        self.assertEqual(re.search(u'(\\d)', '1').group(1), '1')

    def test_groups(self):
        # Test unicode character groups
        self.assertEqual(re.search(r'\d', '\u0661', re.UNICODE).group(0),
            '\u0661')
        self.assertEqual(int(re.search(r'\d', '\u0661', re.UNICODE).group(0)),
            1)
        self.assertEqual(re.search(r'\w', '\u0401'),
            None)
        self.assertEqual(re.search(r'\w', '\u0401', re.UNICODE).group(0),
            '\u0401')
        self.assertEqual(re.search(r'\s', '\u1680', re.UNICODE).group(0),
            '\u1680')
        self.assertEqual(re.findall(r'[\s\d\w]', 'hey 123', re.UNICODE),
            ['h', 'e', 'y', ' ', '1', '2', '3'])
        self.assertEqual(re.search(r'\D', '\u0661x', re.UNICODE).group(0),
            'x')
        self.assertEqual(re.search(r'\W', '\u0401!', re.UNICODE).group(0),
            '!')
        self.assertEqual(re.search(r'\S', '\u1680x', re.UNICODE).group(0),
            'x')
        self.assertEqual(re.search(r'[\D]', '\u0661x', re.UNICODE).group(0),
            'x')
        self.assertEqual(re.search(r'[\W]', '\u0401!', re.UNICODE).group(0),
            '!')
        self.assertEqual(re.search(r'[\S]', '\u1680x', re.UNICODE).group(0),
            'x')


    def test_positions(self):
        # Group positions need to be fixed with unicode (This works as is now below)
        self.assertEqual(re.search(r' (.)', '\U0001d200xxx\u1234 x', re.UNICODE).span(1), 
            (6, 7))
        self.assertEqual(re.search(r' (.)'.encode('utf-8'),
            '\U0001d200xxx\u1234 x'.encode('utf-8')).span(1),
                (11, 12))

        # Pos and endpos also need to be corrected (This now works)
        self.assertEqual(re.compile(r'x', re.UNICODE).findall('\u1234x', 1, 2),
            ['x'])
  

if __name__ == "__main__":
    unittest.main(verbosity=2)

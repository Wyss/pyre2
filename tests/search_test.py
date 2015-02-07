"""
These are simple tests of the ``search`` function
"""

import sys, os
LOCAL_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.abspath(os.path.join(LOCAL_DIR, '..')))

import re2 as re
import unittest

mpath = os.path.join(LOCAL_DIR, 're2_testfiles', 'cnn_homepage.dat')
class SearchTests(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(re.search("((?:[01]?\d{1,2}|2[0-4]\d|25[0-5])\.){3}(?:[01]?\d{1,2}|2[0-4]\d|25[0-5])",
            "hello 28.224.2.1 test").group(),
            '28.224.2.1')

        self.assertEqual(re.search("(\d{3})\D?(\d{3})\D?(\d{4})",
                                    "800-555-1212").groups(),
            ('800', '555', '1212') )

        input = 'a' * 999
        self.assertEqual(len(re.search('(?:a{1000})?a{999}', input).group()),
            999)

        with open(mpath) as fd:
            contents = fd.read()

        self.assertEqual(re.search(r'\n#hdr-editions(.*?)\n', contents).groups(),
                        (' a { text-decoration:none; }',) )

    def test_sanity(self):
        """Verify some sanity checks
        """
        self.assertEqual(re.compile(r'x').search('x', 2000), None)
        self.assertEqual(re.compile(r'x').search('x', 1, -300), None)

    def test_finditer(self):
        """
        Simple tests for the ``finditer`` function.
        """
        with open(mpath) as fd:
            contents = fd.read()

        self.assertEqual(len(list(re.finditer(r'\w+', contents))), 
                            14230)

        self.assertEqual([m.group(1) for m in re.finditer(r'\n#hdr-editions(.*?)\n', contents)],
            [' a { text-decoration:none; }', ' li { padding:0 10px; }', ' ul li.no-pad-left span { font-size:12px; }'])

        self.assertEqual([m.group(1) for m in re.finditer(r'^#hdr-editions(.*?)$', contents, re.M)],
            [' a { text-decoration:none; }', ' li { padding:0 10px; }', ' ul li.no-pad-left span { font-size:12px; }'])

    def test_findall(self):
        # This one is from http://docs.python.org/library/re.html?#finding-all-adverbs:
        self.assertEqual(re.findall(r"\w+ly", "He was carefully disguised but captured quickly by police."),
            ['carefully', 'quickly'])

        # This one makes sure all groups are found:
        self.assertEqual(re.findall(r"(\w+)=(\d+)", "foo=1,foo=2"),
            [('foo', '1'), ('foo', '2')])

        # When there's only one matched group, it should not be returned in a tuple:
        self.assertEqual(re.findall(r"(\w)\w", "fx"), ['f'])

        # Zero matches is an empty list:
        self.assertEqual(re.findall("(f)", "gggg"), [])

        # If pattern matches an empty string, do it only once at the end:
        self.assertEqual(re.findall(".*", "foo"), ['foo', ''])

        self.assertEqual(re.findall("", "foo"), ['', '', '', ''])

    def test_issue4(self):
        TERM_SPEC2 = re.compile('([\W\d_]*)(([^\W\d_]*[-\.]*)*[^\W\d_])([\W\d_]*[^\W\d_]*)')
        self.assertEqual(TERM_SPEC2.search("a").groups(), ('', 'a', None, ''))


        # Still broken because of unicode:
        self.assertEqual(TERM_SPEC2.search("Hello").groups(),
            ('', 'Hello', 'Hell', ''))

    def test_sub(self):
        import hashlib
        import gzip
        path = os.path.join(LOCAL_DIR, 're2_testfiles', 'wikipages.xml.gz')
        with gzip.open(path) as fd:
            data = fd.read()
        res = hashlib.md5(re.sub('\(.*?\)', '', data).encode('utf-8')).hexdigest()
        self.assertEqual(res, 'b7a469f55ab76cd5887c81dbb0cfe6d3')

    def test_pattern(self):
        # We should be able to get back what we put in.
        self.assertEqual(re.compile("(foo|b[a]r?)").pattern, b'(foo|b[a]r?)')


if __name__ == "__main__":
    unittest.main(verbosity=2)

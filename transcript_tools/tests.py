#!/usr/bin/python3

import unittest
from transcript_helper import (munge_code, emdashify, reflow, split_paragraphs,
    style_names, front_matter_check, split_front_matter)

class Tests(unittest.TestCase):
    def test_front_split(self):
        sample = '---\ntitle: Foo\nfile: bar\n---\n\nBody\nhere.\n'
        cuts = split_front_matter(sample)
        self.assertEqual(cuts, ('---\ntitle: Foo\nfile: bar\n---\n', '\nBody\nhere.\n'))

    def test_front_matter(self):
        sample = '---\ntitle: "A Title"\nfile: http://example/url\n---\n'
        errors = front_matter_check(sample)
        self.assertEqual(errors, [])

    def test_split_para(self):
        sample = 'Lorem ipsum\n  dolor sit amet.\n\nConsectetur adipiscing\nelit\n'
        spl = split_paragraphs(sample)
        expected = ['Lorem ipsum dolor sit amet.', 'Consectetur adipiscing elit']
        self.assertEqual(spl, expected)

    def test_munge(self):
        sample = 'This is `A<(B, C)>` a test.'
        out = munge_code(sample, ' ', '␣')
        expected = 'This is `A<(B,␣C)>` a test.'
        self.assertEqual(out, expected)

    def test_emdash(self):
        sample = 'A test-- run `ls --all`'
        out = emdashify(sample)
        expected = 'A test— run `ls --all`'
        self.assertEqual(out, expected)

    def test_style_names(self):
        sample = 'Test: This is a\ntest: not\n'
        out = style_names(sample)
        expected = '__Test__: This is a\ntest: not\n'
        self.assertEqual(out, expected)

    def test_reflow(self):
        sample = '''---\nfront matter\n---\n
            This is a multiline test input,
            with some `code` blocks   \n\n
            and some really `long code blocks`\n\n\n'''
        out = reflow(sample, width=30)
        expected = ('---\nfront matter\n---\n\n'
                    'This is a multiline test\n'
                    'input, with some `code` blocks\n\n'
                    'and some really\n'
                    '`long code blocks`\n')
        self.assertEqual(out, expected)


if __name__ == '__main__':
    unittest.main()

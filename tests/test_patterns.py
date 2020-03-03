# -*coding: utf-8 -*-
from unittest import TestCase
import re
from easy_tokenizer.patterns import Patterns


class PatternsTestCases(TestCase):

    def test_abbrev(self):
        text = ['Feb.', 'FEB.', 'feb.', 'me.', '2002.',
                'end.', 'B.V.', 'b.c.', 'm.s.c.']
        expected_results = [True, True, True, False,
                            False, False, True, True, True]
        for index in range(len(text)):
            self.assertEqual(
                Patterns.abbreviation(text[index]),
                expected_results[index]
            )

    def test_digits_regexp(self):
        text = ['123.21', '176#21', '111,10', '#$@#',
                '123ab', 'v1.0.0.1', '98.01%']
        expected_results = ['123.21', '176#21', '111,10', '', '', '', '98.01%']
        for index in range(len(text)):
            matched = Patterns.DIGITS_RE.fullmatch(text[index])
            matched_text = matched.group() if matched else ''
            self.assertEqual(
                matched_text,
                expected_results[index]
            )

    def test_word_boundary_regexp(self):
        text = ['abc"d', 'abc/d', 'abc\\d', 'abc[d',
                'abc(d', 'abc!d', 'abc#d', 'abc*d',
                'informatici•Ambizione', 'propria•Buone',
                '•Buone', '▸Buone']
        expected_results = [
            ['abc', '"', 'd'],
            ['abc', '/', 'd'],
            ['abc', '\\', 'd'],
            ['abc', '[', 'd'],
            ['abc', '(', 'd'],
            ['abc', '!', 'd'],
            ['abc#d'],
            ['abc', '*', 'd'],
            ['informatici', '•', 'Ambizione'],
            ['propria', '•', 'Buone'],
            ['•', 'Buone'],
            ['▸', 'Buone']
        ]
        for index in range(len(text)):
            matched_text = [
                    substr
                    for substr in re.split(Patterns.WORD_BF_CAPTURED_RE,
                                           text[index])
                    if substr != '']
            self.assertEqual(
                matched_text,
                expected_results[index])

    def test_url_regexp(self):
        text = ['foo http://www.erdfdistribution.fr, bar',
                'foo http://www.edf-bleuciel.fr" bar',
                'foo idnight.idtgv.com, bar',
                'foo http://www.fondation-jeanluclagardere.com bar',
                'foo https://www.blog-des-astucieuses.fr www.foo.bar',
                'foo cecile.nguyen.site.voila.fr/ www.foo.bar',
                'foo http://www.gemo.tm.fr/recrutement/formulaire bar',
                'foo http://www.01podcast.com www.for.bar/foo/bar',
                'foo http://bit.ly/j2JoOL bar',
                'foo http://caroline-podevin.com/ www.foo.bar/bar/',
                'foo (http://www.3ds.com/customer-stories/) bar',
                'foo http://www.4D.fr. bar',
                'foo no url bar'
                ]
        pattern = Patterns.ALL_WEB_CAPTURED_RE
        expected_tokens = [
            ['http://www.erdfdistribution.fr'],
            ['http://www.edf-bleuciel.fr'],
            ['idnight.idtgv.com'],
            ['http://www.fondation-jeanluclagardere.com'],
            ['https://www.blog-des-astucieuses.fr', 'www.foo.bar'],
            ['cecile.nguyen.site.voila.fr/', 'www.foo.bar'],
            ['http://www.gemo.tm.fr/recrutement/formulaire'],
            ['http://www.01podcast.com', 'www.for.bar/foo/bar'],
            ['http://bit.ly/j2JoOL'],
            ['http://caroline-podevin.com/', 'www.foo.bar/bar/'],
            ['http://www.3ds.com/customer-stories/'],
            ['http://www.4D.fr.'],
            []
        ]
        for index in range(len(expected_tokens)):
            tokens = [token.group()
                      for token in re.finditer(pattern, text[index])
                      if token]

            self.assertEqual(
                tokens,
                expected_tokens[index]
            )

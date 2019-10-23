# -*coding: utf-8 -*-
from unittest import TestCase
import re
from easy_tokenizer.patterns import Patterns


class PatternsTestCases(TestCase):

    def test_abbrev(self):
        text = ['Feb.', 'FEB.', 'feb.', 'me.', '2002.', 'end.', 'B.V.', 'b.c.', 'm.s.c.']
        expected_results  = [True, True, True, False, False, False, True, True, True]
        for index in range(len(text)):
            self.assertEqual(
                Patterns.abbreviation(text[index]),
                expected_results[index]
            )

    def test_digits_regexp(self):
        text = ['123.21', '176#21', '111,10', '#$@#', '123ab', 'v1.0.0.1', '98.01%']
        expected_results = ['123.21', '176#21', '111,10', '', '', '', '98.01%']
        for index in range(len(text)):
            matched = Patterns.DIGITS_RE.fullmatch(text[index])
            matched_text = matched.group() if matched else ''
            self.assertEqual(
                matched_text,
                expected_results[index]
            )

    def test_url_regexp(self):
        text = ['http://www.erdfdistribution.fr',
                'http://www.edf-bleuciel.fr',
                'idnight.idtgv.com',
                'http://www.fondation-jeanluclagardere.com',
                'https://www.blog-des-astucieuses.fr',
                'cecile.nguyen.site.voila.fr/',
                'http://www.gemo.tm.fr/recrutement/formulaire',
                'http://www.01podcast.com',
                'http://bit.ly/j2JoOL',
                'http://caroline-podevin.com/',
                '(http://www.3ds.com/customer-stories/)',
                'http://www.4D.fr.'
        ]
        pattern = Patterns.ALL_WEB_CAPTURED_RE
        expected_tokens = [
            ['http://www.erdfdistribution.fr'],
            ['http://www.edf-bleuciel.fr'],
            ['idnight.idtgv.com'],
            ['http://www.fondation-jeanluclagardere.com'],
            ['https://www.blog-des-astucieuses.fr'],
            ['cecile.nguyen.site.voila.fr/'],
            ['http://www.gemo.tm.fr/recrutement/formulaire'],
            ['http://www.01podcast.com'],
            ['http://bit.ly/j2JoOL'],
            ['http://caroline-podevin.com/'],
            ['(', 'http://www.3ds.com/customer-stories/', ')'],
            ['http://www.4D.fr', '.']
        ]
        for index in range(len(expected_tokens)):
            tokens = list(token for token in re.split(pattern, text[index]) if token)

            self.assertEqual(
                tokens,
                expected_tokens[index]
            )

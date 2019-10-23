# -*coding: utf-8 -*-
from unittest import TestCase
import re
import logging
from easy_tokenizer.tokenizer import Tokenizer
from easy_tokenizer import LOGGER

#LOGGER.setLevel(logging.DEBUG)

class TokenizerTestCases(TestCase):
    def setUp(self):
        self.tokenizer = Tokenizer()

    def test_simple_sentence(self):
        text = [
            'this is a normal sentence',
            'this is a normal-sentence'
        ]
        expected_tokens = [
            ['this', 'is', 'a', 'normal', 'sentence'],
            ['this', 'is', 'a', 'normal', '-', 'sentence']
        ]
        for index in range(len(text)):
            self.assertEqual(
                list(self.tokenizer.tokenize(text[index])),
                expected_tokens[index]
            )

    def test_char_with_hat(self):
        text = [
            'Alp NADİ\nCoordination potential bidders.',
            'Hurmoğlu, Botaş BTC, 2002\nCoordination of packages.'
        ]
        expected_tokens = [
            ['Alp', 'NADİ', 'Coordination', 'potential', 'bidders', '.'],
            ['Hurmoğlu', ',', 'Botaş', 'BTC', ',', '2002', 'Coordination', 'of', 'packages', '.']

        ]
        for index in range(len(text)):
            self.assertEqual(
                list(self.tokenizer.tokenize(text[index])),
                expected_tokens[index]
            )


    def test_tokenize_hyphen(self):
        text=[
            'this is a normal-sentence',
            'he is my ex-boyfriend',
            'Sociale Option PME-PMI'
            ]
        expected_tokens = [['this', 'is', 'a', 'normal', '-', 'sentence'],
                           ['he', 'is', 'my', 'ex-boyfriend'],
                           ['Sociale', 'Option', 'PME', '-', 'PMI']
                          ]

        for index in range(len(text)):
            self.assertEqual(
                list(self.tokenizer.tokenize(text[index])),
                expected_tokens[index]
            )

    def test_tokenize_slash(self):
        text = [
            'Programmation C/C++/Java/PHP/Perl/JSP.'
        ]
        expected_tokens = [
            ['Programmation', 'C', '/', 'C++', '/', 'Java', '/', 'PHP', '/', 'Perl', '/', 'JSP', '.']
        ]
        for index in range(len(expected_tokens)):
            tokens = list(self.tokenizer.tokenize(text[index]))
            self.assertEqual(tokens, expected_tokens[index])

    def test_tokenize_phrase(self):
        text=[
            'office(XP)',
            '(ex)girlfriend',
            'Happy(12)Birthday',
            'een#exception',
            'AS/400'
            ]
        expected_tokens = [["office", "(", "XP", ")"],
                           ["(", "ex", ")", "girlfriend"],
                           ["Happy", "(", "12", ")", "Birthday"],
                           ['een#exception'],['AS', '/', '400']
                          ]

        for index in range(len(expected_tokens)):
            self.assertEqual(
                list(self.tokenizer.tokenize(text[index])),
                expected_tokens[index])

    def test_old_tokenizer_cases(self):
        text = ["een mooie test zin.",
                "foo...",
                "foo...bar",
                "l'agence",
                "d'origine",
                "foo,bar",
                "foo.bar",
                "Aug. foo.",
                'foo@bar.com aap.noot@mies.wim aap5@noot.mies',
                'http://www.viadeo.com/profile/34mies',
                '.... ----',
                '.net c++ F#',
                '$100,000.99 10.12 10,12 10.123 10,123 10.000,12',
                '1st',
                'S.I.M.    S I M    S. I. M.    SIM.',
                'end of "phrase".'
        ]
        expected_tokens = [
            ['een', 'mooie', 'test', 'zin', '.'],
            ['foo...'],
            ['foo...bar'],
            ["l", "'", "agence"],
            ["d", "'", "origine"],
            ['foo', ',', 'bar'],
            ['foo.bar'],
            ['Aug.', 'foo', '.'],
            ['foo@bar.com', 'aap.noot@mies.wim', 'aap5@noot.mies'],
            ['http://www.viadeo.com/profile/34mies'],
            ['....', '----'],
            ['.net', 'c++', 'F#'],
            ['$', '100,000.99', '10.12', '10,12', '10.123', '10,123', '10.000,12'],
            ['1st'],
            ['S.I.M.', 'S', 'I', 'M', 'S.', 'I.', 'M.', 'SIM.'],
            ['end', 'of', '"', 'phrase', '"', '.']
        ]
        for index in range(len(text)):
            self.assertEqual(
                list(self.tokenizer.tokenize(text[index])),
                expected_tokens[index]
            )

    def test_digits_extraction(self):
        text = ['BSS (S4d0, S4D1), VOIP']
        expected_tokens = [[ 'BSS', '(', 'S4d0', ',', 'S4D1', ')', ',', 'VOIP']]
        for index in range(len(text)):
            self.assertEqual(
                list(self.tokenizer.tokenize(text[index])),
                expected_tokens[index]
            )

    def test_dot_comman_extraction(self):
        text = ['2000 a dec.01', 'HP-UX, C++, BASIC', 'java, c++, python']
        expected_tokens = [
            [ '2000', 'a', 'dec.', '01'],
            ['HP-UX', ',', 'C++', ',', 'BASIC'],
            [ 'java', ',', 'c++', ',', 'python']
        ]
        for index in range(len(text)):
            self.assertEqual(
                list(self.tokenizer.tokenize(text[index])),
                expected_tokens[index]
            )


    def test_url_email(self):
        text = '''http://live.textkernel.nl", lichao@google.com and this is
another one, here https://www.damienpontifex.com/ch/05/06/image-classifier/ or
try this one https://docs.google.com/document/d/1pd/edit?ts=5da580bc'''
        self.assertEqual(
            self.tokenizer.tokenize(text),
            [
                'http://live.textkernel.nl',
                '"',
                ',',
                'lichao@google.com',
                'and',
                'this',
                'is',
                'another',
                'one',
                ',',
                'here',
                'https://www.damienpontifex.com/ch/05/06/image-classifier/',
                'or',
                'try',
                'this',
                'one',
                'https://docs.google.com/document/d/1pd/edit?ts=5da580bc'])


    def test_email(self):
        text = ["e-mail : dimitri.fotiadis@laposte.net\ngsm"]
        self.assertEqual(
            [self.tokenizer.tokenize(phrase) for phrase in text],
            [
                [ 'e-mail', ':', 'dimitri.fotiadis@laposte.net', 'gsm']
            ]
        )

    def test_url_extraction(self):
        text = self.get_url_text()
        expected_tokens = [
            ['REFERENCES',
             'http://www.erdfdistribution.fr',
             'http://www.idtgv.com',
             'http://www.edf-bleuciel.fr',
             'idnight.idtgv.com',
             'http://investisseurs.edf.com',
             'http://www.metaxa.com',
             'ina.edf.com',
             'http://www.hutchinson.fr',
             'http://www.lagardere.com',
             'http://www.direxi.fr',
             'http://www.fondation-jeanluclagardere.com',
             'http://www.blog-des-astucieuses.fr',
             'http://www.investir.fr',
             'http://www.clubnewsparis.com',
             'http://www.cointreau.fr'],
            ['1', '/', '2', 'Cecile', 'NGUYEN', 'http://cecile.nguyen.site.voila.fr/', '7'],
            ['lien', 'suivant', 'http://www.gemo.tm.fr/recrutement/formulaire', 'Gemo'],
            ['http://www.01podcast.com', '-'],
            ['http://bit.ly/j2JoOL'],
            ['2', 'ENFANTS', '-', 'http://caroline-podevin.com/'],
            ['(', 'http://www.3ds.com/customer-stories/', ')'],
            ['4D', 'S.A', 'http://www.4D.fr', '.', 'ITK', 'http://www.internet-toolkit.com', '(', 'outil', 'TCP', '/', 'IP'],
            ['this', 'is', 'a', 'url', ':', 'http://live.textkernel.nl', ',',
              'and', 'you', 'can', 'chat', 'with', 'it']
        ]
        for index in range(len(expected_tokens)):
            tokens = list(self.tokenizer.tokenize(text[index]))
            self.assertEqual(tokens, expected_tokens[index])

    @staticmethod
    def get_url_text():
        text = ['''REFERENCES http://www.erdfdistribution.fr
http://www.idtgv.com http://www.edf-bleuciel.fr
idnight.idtgv.com http://investisseurs.edf.com
http://www.metaxa.com ina.edf.com http://www.hutchinson.fr
http://www.lagardere.com http://www.direxi.fr
http://www.fondation-jeanluclagardere.com http://www.blog-des-astucieuses.fr
http://www.investir.fr http://www.clubnewsparis.com http://www.cointreau.fr''',
            '1 / 2 Cecile NGUYEN http://cecile.nguyen.site.voila.fr/ 7',
            'lien suivant http://www.gemo.tm.fr/recrutement/formulaire Gemo',
            'http://www.01podcast.com  -',
            'http://bit.ly/j2JoOL',
            '2 ENFANTS - http://caroline-podevin.com/',
            '(http://www.3ds.com/customer-stories/)',
            '4D S.A\n    http://www.4D.fr.\n     ITK http://www.internet-toolkit.com (outil TCP/IP',
            '''this is   a url: http://live.textkernel.nl,
and you can chat with it'''
        ]
        return text

'''Tokenizer Class'''
# -*- encoding: utf-8 -*-
import re
from .token_with_pos import TokenWithPos
from .patterns import Patterns


class Tokenizer():
    '''
    A basic Tokenizer class to tokenize strings and patterns

    Parameters:
        - regexp: regexp used to tokenize the string
    '''
    def __init__(self, regexp=None):
        if regexp is not None:
            self.regexp = regexp
        else:
            self.regexp = re.compile(r'[^\s]+|\s+')
        self.space_regexp = re.compile(r'\s')

    def _tokenize(self, text):
        for match in self.regexp.finditer(text):
            phrase = match.group()
            if self.space_regexp.search(phrase):
                continue
            if self._phrase_full_match(phrase) is not None:
                for adjusted_token in self._adjust_on_punc(
                        TokenWithPos(phrase, match.start(), match.end())):
                    yield adjusted_token
            else:
                for token in self._top_down_tokenize(phrase,
                                                     match.start()):
                    for adjusted_token in self._adjust_on_punc(token):
                        yield adjusted_token

    def _adjust_on_punc(self, token):
        if Patterns.PUNCT_SEQ_RE.fullmatch(token.text) and \
                Patterns.PARA_SEP_RE.fullmatch(token.text) is None:
            # a string of punc, very likely .. or ...
            for shift, single_char in enumerate(token.text):
                start_pos = token.start + shift
                yield TokenWithPos(single_char,
                                   start_pos,
                                   start_pos + 1)

        elif self._has_end_of_phrase_punc(token.text) and \
                self._phrase_full_match(token.text) in [None, 'url/email']:
            end_pos = token.end - 1
            for splitted_token in [
                    TokenWithPos(token.text[:-1],
                                 token.start,
                                 end_pos),
                    TokenWithPos(token.text[-1],
                                 end_pos,
                                 token.end)
            ]:
                yield splitted_token
        else:
            yield token

    def _top_down_tokenize(self, phrase, offset=0):
        # first get the web url and emails out
        for token in self._top_down_level_1(phrase, offset):
            yield token

    def _top_down_level_1(self, phrase, offset=0):
        '''
        level 1: split on url, emails
        '''
        for sub_phrase in re.split(Patterns.ALL_WEB_CAPTURED_RE, phrase):
            if sub_phrase == '':
                continue

            length_sub_phrase = len(sub_phrase)
            if self._phrase_full_match(sub_phrase) is not None:
                yield TokenWithPos(sub_phrase,
                                   offset,
                                   offset + length_sub_phrase)

            else:
                for token in self._top_down_level_2(sub_phrase, offset):
                    yield token
            offset += length_sub_phrase

    def _top_down_level_2(self, phrase, offset=0):
        '''
        level 2: split on number phrases
        '''
        for sub_phrase in re.split(Patterns.DIGITS_CAPTURED_RE, phrase):
            if sub_phrase == '':
                continue

            length_sub_phrase = len(sub_phrase)
            if self._phrase_full_match(sub_phrase) is not None:
                yield TokenWithPos(sub_phrase,
                                   offset,
                                   offset + length_sub_phrase)
            else:
                for token in self._top_down_level_3(sub_phrase, offset):
                    yield token
            offset += length_sub_phrase

    def _top_down_level_3(self, phrase, offset=0):
        '''
        level 3: split on normal word boundaries
        '''
        for sub_phrase in re.split(Patterns.WORD_BF_CAPTURED_RE, phrase):
            if sub_phrase == '':
                continue

            length_sub_phrase = len(sub_phrase)
            if self._phrase_full_match(sub_phrase) is not None:
                yield TokenWithPos(sub_phrase,
                                   offset,
                                   offset + length_sub_phrase)
            else:
                for token in self._top_down_level_4(sub_phrase, offset):
                    yield token
            offset += length_sub_phrase

    def _top_down_level_4(self, phrase, offset):
        '''
        level 4: here we handle special cases
        '''

        splitted = False
        parts = []
        # - split on hyphen #
        if Patterns.HYPHEN_RE.search(phrase):
            splitted = True
            parts = [
                part
                for part in Patterns.HYPHEN_CAPTURED_RE.split(phrase)
                if part != ''
            ]
            if len(parts) == 3:
                if parts[0].lower() in Patterns.COMMON_HYPHEN_START:
                    splitted = False
                elif len(parts[0]) < 4 and len(parts[2]) < 4 \
                        and len(parts[0]) + len(parts[2]) < 6:
                    # mx-doc, tcp-ip, e-mail, hp-ux etc. #
                    splitted = False

        if splitted:
            for part in parts:
                new_offset = offset + len(part)
                yield TokenWithPos(part, offset, new_offset)
                offset = new_offset
        else:
            # pick up what ever left as a token #
            yield TokenWithPos(phrase, offset, offset + len(phrase))

    def _has_end_of_phrase_punc(self, phrase):
        end_char_is_punc = False
        if phrase[-1] in Patterns.PUNCT_END_PHRASE:
            end_char_is_punc = True
            if Patterns.ABBREV_RE.fullmatch(phrase):
                end_char_is_punc = False
        return end_char_is_punc

    def _phrase_full_match(self, phrase):
        matched_type = None
        if len(phrase) == 1:
            matched_type = 'single_char'
        elif phrase.isalpha():
            matched_type = 'word'
        elif phrase in Patterns.si_units:
            matched_type = 'unit'
        elif Patterns.DIGITS_RE.fullmatch(phrase):
            matched_type = 'digit'
        elif Patterns.PARA_SEP_RE.fullmatch(phrase):
            matched_type = 'punctuation_seq'
        elif Patterns.abbreviation(phrase):
            matched_type = 'abbreviation'
        elif Patterns.ALL_WEB_RE.fullmatch(phrase):
            matched_type = 'url/email'
        return matched_type

    def tokenize(self, text):
        '''
        tokenize

        params:
            - text: string
            - pos_info: also output the position information when tokenizing
        output: tokens (with position info)
        '''
        return [token.text for token in self._tokenize(text)]

    def tokenize_with_pos_info(self, text):
        '''
        tokenize

        params:
            - text: string
        output:
            - a list of Token object
        '''
        return list(self._tokenize(text))

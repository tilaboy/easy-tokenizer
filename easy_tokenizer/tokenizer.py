'''Tokenizer Class'''
# -*- encoding: utf-8 -*-
import re
from . import LOGGER
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
            LOGGER.debug('check: [{}]'.format(phrase))
            if self.space_regexp.search(phrase):
                continue

            if self._phrase_full_match(phrase) is not None:
                LOGGER.debug('match: [{}], {}, {}'.format(phrase,
                                                          match.start(),
                                                          match.end()))
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
            LOGGER.debug('split punc strings [{}]'.format(
                token.text))
            # a string of punc, very likely .. or ...
            for shift, single_char in enumerate(token.text):
                LOGGER.debug('punc seq[{}]: {}, {} -> {}'.format(
                             shift, single_char, token.start+shift,
                             token.start+shift+1))
                yield TokenWithPos(single_char,
                                   token.start+shift,
                                   token.start+shift+1)

        elif self._has_end_of_phrase_punc(token.text) and \
                self._phrase_full_match(token.text) in [None, 'url/email']:
            LOGGER.debug('split_last : [{}], {}, {}'.format(
                token.text, token.start, token.end))
            for splitted_token in [
                    TokenWithPos(token.text[:-1],
                                 token.start,
                                 token.end - 1),
                    TokenWithPos(token.text[-1],
                                 token.end - 1,
                                 token.end)
            ]:
                yield splitted_token
        else:
            LOGGER.debug('  output: [{}], {}, {}'.
                         format(token.text,
                                token.start,
                                token.end))
            yield token

    def _top_down_tokenize(self, phrase, offset=0):
        # first get the web url and emails out
        LOGGER.debug('l1_start: [{}], {}, {}'.format(phrase,
                                                     offset,
                                                     offset + len(phrase)))

        for token in self._top_down_level_1(phrase, offset):
            yield token

    def _top_down_level_1(self, phrase, offset=0):
        '''
        level 1: split on url, emails
        '''
        for sub_phrase in re.split(Patterns.ALL_WEB_CAPTURED_RE, phrase):
            if sub_phrase == '':
                continue
            if self._phrase_full_match(sub_phrase) is not None:
                LOGGER.debug('l1_match: [{}], {}, {}'.format(sub_phrase,
                             offset,
                             offset + len(sub_phrase)))
                yield TokenWithPos(sub_phrase,
                                   offset,
                                   offset + len(sub_phrase))

            else:
                LOGGER.debug('l2_start: [{}], {}, {}'.format(sub_phrase,
                             offset,
                             offset + len(sub_phrase)))
                for token in self._top_down_level_2(sub_phrase, offset):
                    yield token
            offset += len(sub_phrase)

    def _top_down_level_2(self, phrase, offset=0):
        '''
        level 2: split on number phrases
        '''
        for sub_phrase in re.split(Patterns.DIGITS_CAPTURED_RE, phrase):
            if sub_phrase == '':
                continue
            if self._phrase_full_match(sub_phrase) is not None:
                LOGGER.debug('l2_match: [{}], {}, {}'.format(sub_phrase,
                             offset,
                             offset + len(sub_phrase)))
                yield TokenWithPos(sub_phrase,
                                   offset,
                                   offset + len(sub_phrase))
            else:
                LOGGER.debug('l3_start: [{}], {}, {}'.format(sub_phrase,
                             offset,
                             offset + len(sub_phrase)))
                for token in self._top_down_level_3(sub_phrase, offset):
                    yield token
            offset = offset + len(sub_phrase)

    def _top_down_level_3(self, phrase, offset=0):
        '''
        level 3: split on normal word boundaries
        '''
        for sub_phrase in re.split(Patterns.WORD_BF_CAPTURED_RE, phrase):
            if sub_phrase == '':
                continue
            if self._phrase_full_match(sub_phrase) is not None:
                LOGGER.debug('l3_match: [{}], {}, {}'.format(sub_phrase,
                             offset,
                             offset + len(sub_phrase)))
                yield TokenWithPos(sub_phrase,
                                   offset,
                                   offset + len(sub_phrase))
            else:
                LOGGER.debug('l4_start: [{}], {}, {}'.format(sub_phrase,
                             offset,
                             offset + len(sub_phrase)))
                for token in self._top_down_level_4(sub_phrase, offset):
                    yield token
            offset = offset + len(sub_phrase)

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

        LOGGER.debug('split phrase: [{}] is {}'.format(phrase, splitted))
        if splitted:
            for part in parts:
                yield TokenWithPos(part, offset, offset + len(part))
                offset += len(part)
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
        elif phrase.isalpha() or phrase in Patterns.si_units:
            matched_type = 'word'
        elif Patterns.ALL_WEB_RE.fullmatch(phrase):
            matched_type = 'url/email'
        elif Patterns.DIGITS_RE.fullmatch(phrase):
            matched_type = 'digit'
        elif Patterns.abbreviation(phrase):
            matched_type = 'abbreviation'
        elif Patterns.PARA_SEP_RE.fullmatch(phrase):
            matched_type = 'punctuation_seq'

        LOGGER.debug('matched type: [{}]'.format(matched_type))
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
        tokens = []
        for token in self._tokenize(text):
            tokens.append(token)
        return tokens

'''Normalizer Functions'''

import unicodedata


def normalize_chars(text):
    "Decompose the unicode string s and remove non-spacing marks."
    return ''.join(char for char in unicodedata.normalize('NFKD', text)
                   if unicodedata.category(char) != 'Mn')

'''class to store knowledges used for tokenization'''
# -*- encoding: utf-8 -*-
import re


def _captured_pattern(pattern):
    return r'(' + pattern + r')'


class Patterns:
    '''
    Contains a set of special chars could be used for tokenization'
    '''

    # phrase boundary
    ##################################

    PUNCT_END_PHRASE = frozenset(
        [")", "]", "“", "'", "»", "”", "’", '"', "[…]",
         ".", ";", ":", ",", "?", "!", ","]
    )

    # digit, unit
    ###################################

    # Derived unit : (base SI unit)
    si_units = [
        "m²", "fm", "cm²", "m³", "cm³", "l", "ltr", "dl", "cl", "ml",
        "°C", "°F", "K", "g", "gr", "kg", "t", "mg", "μg", "m", "km",
        "mm", "μm", "cm", "sm", "s", "ms", "μs", "Nm", "klst", "min",
        "W", "mW", "kW", "MW", "GW", "TW", "J", "kJ", "MJ", "GJ", "TJ",
        "kWh", "MWh", "kWst", "MWst", "kcal", "cal", "N", "kN", "V", "v",
        "mV", "kV", "A", "mA", "Hz", "kHz", "MHz", "GHz", "Pa", "hPa",
        "°", "°c", "°f"
    ]

    digits_pn = r'(?:\b|^)[-+±~]?(?:\d[-.,0-9\/#]*\d|'\
                r'\d+(?:st|nd|rd|th|[dD])?)'\
                r'[%]?(?:\b|$)'
    digits_captured_pn = _captured_pattern(digits_pn)

    DIGIT_RE = re.compile(r'\d')
    DIGITS_RE = re.compile(digits_pn)
    DIGITS_CAPTURED_RE = re.compile(digits_captured_pn)
    YEAR_RE = re.compile(r'(?:\b|^)(?:19|20)\d\d(?:\b|$)')

    # url, email
    ##################################
    url_pn = r"(?:[0-9a-zA-Z][-\w_]+)" \
             r"(?:\.[0-9a-zA-Z][-\w_]+){2,5}" \
             r"(?:(?:\/(?:[0-9a-zA-Z]|[-_?.#=:&%])+)+)?\/?"

    url_strict_pn = r'(?:(?:http[s]?|ftp)://|wwww?[.])' \
                    r'(?:[a-zA-Z]|[0-9]|[-_:\/?@.&+=]|' \
                    r'(?:%[0-9a-fA-F][0-9a-fA-F]))+'

    email_pn = r"\S+[@]\S+[.]\S+"
    domain_pn = r"[@]\S+[.]\S+"
    all_web_pn = "|".join([url_strict_pn, url_pn, email_pn, domain_pn])
    all_web_captured_pn = _captured_pattern(all_web_pn)

    URL_RE = re.compile("|".join([url_pn, url_strict_pn]))
    EMAIL_RE = re.compile(email_pn)
    DOMAIN_RE = re.compile(domain_pn)

    ALL_WEB_RE = re.compile(all_web_pn)
    ALL_WEB_CAPTURED_RE = re.compile(all_web_captured_pn)

    # word bourdary
    ##################################

    word_bf_pn = r'[()\[\]{}"“”\'`»:;,/\\*?!…<=>@^$\|~%]|' \
                 r'[\u2022\u2751\uF000\uF0FF]|' \
                 r'[\u25A0-\u25FF]|' \
                 r'\.{2,}'
    word_bf_captured_pn = _captured_pattern(word_bf_pn)
    WORD_BF_CAPTURED_RE = re.compile(word_bf_captured_pn)

    # looks the same, but actually different hyphens
    hyphen_pn = r'[\-\–\—]'
    HYPHEN_RE = re.compile(hyphen_pn)
    HYPHEN_CAPTURED_RE = re.compile(_captured_pattern(hyphen_pn))

    COMMON_HYPHEN_START = ['e', 'i', 're', 'ex', 'self',
                           'fore', 'all', 'low', 'high']

    # abbrev
    ##################################
    months = ['jan', 'feb', 'mar', 'apr', 'jun',
              'jul', 'aug', 'sep', 'Sept',
              'sept', 'SEPT', 'oct', 'nov', 'dec']

    repeat_abbrev_pn = r'(\w\.){2,}'
    known_month_pn = r"(?:" + r"|".join(months) + r")\."
    ABBREV_RE = re.compile(repeat_abbrev_pn + r'|' + known_month_pn)

    PUNCT_SEQ_RE = re.compile(r'[-!\'#%&`()\[\]*+,.\\/:;<=>?@^$_{|}~]+')
    PARA_SEP_RE = re.compile(r'(\W|\+\-)\1{4,}')

    @staticmethod
    def abbreviation(phrase):
        is_abbrev = False
        if phrase[-1] == '.':
            if phrase[0].isupper() and phrase[:-1].isalpha() and \
                    len(phrase[:-1]) < 4:
                is_abbrev = True
            elif Patterns.ABBREV_RE.fullmatch(phrase):
                is_abbrev = True
        return is_abbrev

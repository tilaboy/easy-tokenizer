'''Class for tokens with position information'''


class TokenWithPos:
    '''
    TokenWithPos: token with start and end position in the text
        attributes:
        - text: text in the normalized form
        - start: start position
        - end: end position
    '''
    def __init__(self, text, start, end):
        self.text = text
        self.start = start
        self.end = end

    def __repr__(self):
        return "{} [{}:{}]".format(self.text, self.start, self.end)

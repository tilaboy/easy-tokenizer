'''
taxonomy_match: script to load a taxonomy, and find all matches from input
'''
from argparse import ArgumentParser
from . import LOGGER
from .tokenizer import Tokenizer


def get_args():
    '''get arguments'''
    parser = ArgumentParser(description='tokenize text', prog='PROG')
    input_args = parser.add_mutually_exclusive_group(required=True)
    input_args.add_argument('-s',
                            '--string',
                            help='input file with text',
                            type=str)

    input_args.add_argument('-f',
                            '--filename',
                            help='input file with text',
                            type=str)

    parser.add_argument('-o', '--output', help='output file', type=str)

    return parser.parse_args()


def main():
    '''
    tokenzier

    params:

    - input_file: text document to tokenize

    - string: string to tokenize

    - output: output file, default as STDOUT
    '''
    args = get_args()

    result = ''
    tokenizer = Tokenizer()
    if args.filename:
        LOGGER.info('tokenize text file {}'.format(args.filename))
        with open(args.filename, "r", encoding="utf-8") as input_f:
            input_text = input_f.read()
        result = tokenizer.tokenize(input_text)
    elif args.string:
        LOGGER.info('tokenize input string')
        result = tokenizer.tokenize(args.string)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as output_f:
            output_f.write(" ".join(result))
    else:
        print(" ".join(result))

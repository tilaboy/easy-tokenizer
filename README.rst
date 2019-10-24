Easy-Tokenizer
==================

Description
-----------

Most tokenizers are eithor too cumbersom (Neural Network based), or too simple.
This simple rule based tokenizer is type, small, and sufficient good. Specially,
it handles long strings very often parsed wrong by some simple tokenizers, deal
url, email, long digits rather well.


Try with the following script:

``easy_tokenizer -s input_text``

or

``easy_tokenizer -f input_file``


CI Status
------------

.. image:: https://travis-ci.org/tilaboy/easy-tokenizer.svg?branch=master
    :target: https://travis-ci.org/tilaboy/easy-tokenizer

.. image:: https://readthedocs.org/projects/easy-tokenizer/badge/?version=latest
    :target: https://easy-tokenizer.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status


.. image:: https://pyup.io/repos/github/tilaboy/easy-tokenizer/shield.svg
    :target: https://pyup.io/repos/github/tilaboy/easy-tokenizer/
    :alt: Updates

Requirements
------------

Python 3.6+

Installation
------------

::

    pip install easy-tokenizer


Usage
-----

-  easy-tokenizer:

   input:

      - string: input string to tokenize

      - filename: input text file to tokenize

      - output: output filename, optional. print out to STDOUT when not set

   output:

   - a sequence of space separated tokens

examples:
^^^^^^^^^

::

    # string input
    easy-tokenizer -s "this is   a simple test."

    easy-tokenizer -f foo.txt
    easy-tokenizer -f foo.txt -o bar.txt

output will be "this is a simple test ."

Development
-----------

To install package and its dependencies, run the following from project
root directory:

::

    python setup.py install

To work the code and develop the package, run the following from project
root directory:

::

    python setup.py develop

To run unit tests, execute the following from the project root
directory:

::

    python setup.py test

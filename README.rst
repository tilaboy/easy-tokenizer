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


Status
------------

::

    todo

Requirements
------------

Python 3.6+

Installation
------------

::

    pip install easy-tokenizer


Usage
-----

::

    todo

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

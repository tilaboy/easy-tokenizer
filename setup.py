import os
from setuptools import setup, find_packages

NAME = "easy_tokenizer"
VERSION = os.environ.get("EASY_TOKENIZER_VERSION", '0.0.7')

with open('README.rst', "r") as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst', "r") as history_file:
    history = history_file.read()

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    name=NAME,
    version=VERSION,
    keywords='tokenizer',
    url='https://github.com/tilaboy/easy-tokenizer',
    description="tokenizer tool",
    author="Chao Li",
    author_email="chaoli.job@gmail.com",
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    long_description=readme + '\n\n' + history,
    test_suite="tests",
    setup_requires=setup_requirements,
    tests_require=test_requirements,
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "easy-tokenizer=easy_tokenizer.__main__:main"
        ],
    },
    license="MIT license",
    zip_safe=False
)

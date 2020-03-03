# -*- coding: utf-8 -*-
"""
Top-level package for easy-tokenizer
"""
import sys
import logging

__author__ = """Chao Li"""
__email__ = 'chaoli.job@google.com'
__version__ = '0.0.10'
name = "easy-tokenizer"


def define_logger(mod_name):
    """Set the default logging configuration"""
    logger = logging.getLogger(mod_name)
    if not logger.handlers:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(logging.Formatter(
            '%(levelname).1s [%(asctime)s] [%(name)s] %(message)s'))
        logger.addHandler(console_handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False
    return logger


def set_logging_level(level=logging.WARN):
    """Change logging level"""
    LOGGER.setLevel(level)


LOGGER = define_logger(__name__)

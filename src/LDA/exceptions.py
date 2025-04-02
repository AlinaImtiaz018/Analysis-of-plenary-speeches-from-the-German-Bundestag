"""
Title: exceptions.py

Description:
    This file contains custom exceptions
    for the LDA model.

Author:
    Konrad Brüggemann,
    Universität Potsdam,
    brueggemann4@uni-potsdam.de

Date:
    05.07.2024
"""


class EmptyCorpusError(Exception):
    """
    Raised if Gensim couldn't generate 
    a corpus for a dataset.
    """
    pass


class MissingVectorError(Exception):
    """
    Raised when a vector is missing in a dataset or model.
    """
    pass


class NoTopicsFoundError(Exception):
    """
    Raised when no topics are found in a topic modeling process.
    """
    pass

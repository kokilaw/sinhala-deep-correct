from __future__ import unicode_literals, print_function, division
from io import open
import re

MAX_LENGTH = 200
MIN_WORD_COUNT = 3
MAX_WORD_COUNT = 8


def normalize_string(s):
    s = re.sub(r"([.!?])", r" \1", s)
    return s


def filter_pair(p, ignore_list=[]):
    return MAX_WORD_COUNT >= len(p[0].split(' ')) >= MIN_WORD_COUNT and \
        len(p[0]) <= MAX_LENGTH and \
        not p[0] in ignore_list


def filter_pairs(pairs, ignore_list=[]):
    return [pair for pair in pairs if filter_pair(pair, ignore_list)]


def read_from_file(path):
    print("Reading lines...")

    # Read the file and split into lines
    lines = open(path, encoding='utf-16'). \
        read().strip().split('\n')

    # Split every line into data and normalize
    pairs = [[normalize_string(s) for s in l.split('\t')] for l in lines]

    return pairs


def prepare_data(path, ignore_list=[]):
    pairs = read_from_file(path)
    print("Read %s sentence pairs" % len(pairs))
    pairs = filter_pairs(pairs, ignore_list)
    print("Trimmed to %s sentence pairs" % len(pairs))
    return pairs

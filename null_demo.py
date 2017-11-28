#!/usr/bin/python

import re
import clib as cl
from pprint import pprint as pp
from sys import exit, stdout

o = (
    'THERE IS NOTHING. TO SEE. HERE IN THIS CIPHER.'
)

# Create sanitized cipher
c = re.sub(r'\.', '', o)
pp(c)

# Create phrase list
ph = list(filter(None, map(lambda x: x.lstrip(), o.split('.'))))
pp(ph)

print("# Use this to help find the crib")
cl.makephgrep(ph)
cl.makephrgrep(ph)

print("# Word Slices")
cl.common_word_slice(c.split(' '))

print("# Letter Slices")
cl.common_letter_slice(c.split(' '))

cl.common_phrase_slice(ph)

print("# Searching for matching of Conway's Constant")
patt = [1, 1, 1, 3, 2, 1, 3, 2, 1, 1]
for p in ph:
    ps = p.split(' ')
    wdic = cl.find_dict(ps)
    cl.find_in_pattern(wdic, cl.get_possibs(ps), patt)

# Try out patterns that repeat at the start of each "phrase"
for j, k in enumerate([
    [2, 4, 5],
    [1, 5, 2],
    [1, 7, 3],
    [4, 3, 2],
]):
    print("# Pattern %s (resets): %s" % (j, k))
    cl.letter_out(k, ph)

# Try out patterns that continue for the whole cipher
for j, k in enumerate([
    [2, 2, 3, 2, 2, 2, 3, 2],
    [1, 1, 2, 1, 1, 1, 2 ,1],
    [4, 3, 2, 3, 4, 3, 2, 3],
]):
    print("# Pattern %s (no reset): %s" % (j, k))
    cl.phrase_out(k, ph)

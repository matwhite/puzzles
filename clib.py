from pprint import pprint as pp
from sys import stdout
from nltk.corpus import stopwords
from subprocess import check_output
from collections import defaultdict


# Make grep statements for matching words
def makegrep(l, ret=0):
    res = "egrep -i '^"
    for w in l:
        res += ("[%s]" % ''.join(w))
    res += ("$' /usr/share/dict/words | tr 'A-Z' 'a-z' | sort | uniq")
    if ret:
        return res
    else:
        print(res)


# Make grep statements for matching words in reverse order
def makergrep(l):
    makegrep(reversed(l))


# Make system grep for whole cryptograms
def makephgrep(ph):
    print("(")
    for p in ph:
        makegrep(p.split(' '))
        print("echo")
    print(") | less")


# Make system grep for whole cryptograms with words in reverse order
def makephrgrep(ph):
    print("(")
    for p in ph:
        makergrep(p.split(' '))
        print("echo")
    print(") | less")


# Find positional letters with pattern starting over with each new phrase
def letter_out(k, phrases, r=0):
    if r:
        k = reversed(k)
    for p in phrases:
        for i, w in enumerate(p.split(' ')):
            try:
                stdout.write(w[k[i]-1])
            except IndexError:
                stdout.write('?')
        print


# Find positional letters with pattern running on whole phrase
def phrase_out(k, phrases):
    i = 0
    for p in phrases:
        for w in p.split(' '):
            try:
                stdout.write(w[k[i]-1])
            except IndexError:
                stdout.write('?')
            i += 1
        print


# Filter stopwords
def killstop(words):
    return(
        [x for x in words if not x.lower() in set(stopwords.words('english'))]
    )


# Common word slices
def common_word_slice(words):
    print("# Every other word, starting at 0")
    pp(words[::2])
    print("# Every other word, starting at 1")
    pp(words[1::2])
    print("# Every third word, starting at 0")
    pp(words[::3])
    print("# Every third word, starting at 1")
    pp(words[1::3])
    print("# Every third word, starting at 2")
    pp(words[2::3])


# Common letter slices
def common_letter_slice(words):
    z = defaultdict(list)
    for w in words:
        for i in range(-4, 3):
            try:
                z[i].append(w[i])
            except IndexError:
                z[i].append('?')

    for i in range(-4, 3):
        print("# Common letter slices: %s" % i)
        print('   %s' % ''.join(z[i]))


# Common phrase slices
def common_phrase_slice(phrase):
    fs = []
    fe = []
    for p in phrase:
        for i, j in enumerate(p.split(' ')):
            ind = len(j) - (i + 1)
            fs.append(i + 1)
            fe.append(ind + 1)

    print("# Incremental Pattern From Start")
    phrase_out(fs, phrase)

    print("# Incremental Pattern From End")
    phrase_out(fe, phrase)


# Find dictionary of letters for a word
def find_dict(words):
    print(' '.join(words))
    word_dict = []

    # Locate all positions of each letter within a word
    for word in words:
        slots = defaultdict(list)
        for i, l in enumerate(word):
            slots[l].append(i)
        word_dict.append(slots)

    # Output warnings about multiple instances of a letter within a word
    for i, w in enumerate(word_dict):
        for k in w.keys():
            if len(w[k]) > 1:
                print(
                    "Warning: w %s letter %s pos %s has multiples"
                    % (i, k, w[k])
                )

    return word_dict


# Recursively find all permutations of letter position combos
# Also finds places where a letter occurs in more than one position in a word
def word_dict_recurse(ary, stor, register=[], slot=0):
    # Prepare register to be set
    if len(register) <= slot:
        register.append('')
    # Loop through each possibility for this slot
    for possib in ary[0]:
        # Set the slot for this possibility
        register[slot] = possib

        # If we are on the last place in the list, store the results
        if len(ary) == 1:
            z = [x for x in register]   # deep copy
            stor.append(z)
        # Otherwise, stack on the next position
        else:
            word_dict_recurse(ary[1:len(ary)], stor, register, slot + 1)


# See if a list of digits matches something in a larger list of digits
def lookfor_pattern(srch, patt):
    found = 0
    for i, z in enumerate(patt):
        if i > len(patt) - len(srch):
            break
        if srch[0] == z:
            found = 0
            for ii, f in enumerate(srch):
                if patt[i + ii] == f:
                    found += 1
            if found == len(srch):
                return 1
    return 0


# Find numbers in number pattern (e.g., part of sequential digits of pi or e)
def find_in_pattern(word_dict, words, patt):
    # For each word, build the list of possible digits
    for w in words:
        seq = []
        for i, wl in enumerate(w.upper()):
            seq.append(word_dict[i][wl])
        allpatts = []
        word_dict_recurse(seq, allpatts, [])
        for s in allpatts:
            g = [x + 1 for x in s]  # convert from list index to pattern num
            lk = lookfor_pattern(g, patt)
            if lk:
                print("== %s %s" % (w, ','.join(map(str, g))))
            else:
                print(" - %s %s" % (w, ','.join(map(str, g))))


# Get word possibilities from makegrep
def get_possibs(words):
    cmd = makegrep(words, ret=1)
    out = check_output(cmd, shell=True)
    return([s.strip() for s in out.splitlines()])

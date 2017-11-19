#!/usr/bin/python

from pprint import pprint as pp
import string
import sys


# Find places where there are inconsistencies in mappings
def countem(la, lb):
    store = {}
    # Step through each letter in each same-length word
    for i in range(len(la)):
        a = la[i]
        b = lb[i]
        # Vivify the data structure
        if a not in store:
            store[a] = {}
        if b not in store[a]:
            store[a][b] = 1
        else:
            store[a][b] += 1
        # If same letter has more than one key (a and b),
        # then we failed the internal consistency check
        # (Check for failure often to exit loop efficiently)
        if len(store[a].keys()) > 1:
            return(1)
    return(0)


# Find matches with 'space' counting as a wildcard
def matchem(la, lb):
    for i in range(len(la)):
        a = la[i]
        b = lb[i]
        if a != ' ' and b != ' ' and a != b:
            return 0
    return 1


# Output grep statements to facilitate guesses
def makegrep(a, b):

    def getem(l):
        return ''.join(possibs.get(l))

    print(
        "grep -i '^[%s][%s][%s][%s]$' /usr/share/dict/words"
        % tuple(map(getem, letts[a:b]))
    )


# Letter rules
rules = {
    'A': 'aaaaa', 'B': 'aaaab', 'C': 'aaaba', 'D': 'aaabb', 'E': 'aabaa',
    'F': 'aabab', 'G': 'aabba', 'H': 'aabbb', 'I': 'abaaa', 'K': 'abaab',
    'L': 'ababa', 'M': 'ababb', 'N': 'abbaa', 'O': 'abbab', 'P': 'abbba',
    'Q': 'abbbb', 'R': 'baaaa', 'S': 'baaab', 'T': 'baaba', 'U': 'baabb',
    'W': 'babaa', 'X': 'babab', 'Y': 'babba', 'Z': 'babbb'
}
rules['J'] = rules['I']
rules['V'] = rules['U']

# The sentence
letts = (
    'CRUEL DEEDS SCARE CABIN CLUNK ASPIC CLASH PLUGS APTLY JEWEL PAIRS '
    'DEVIL WREAK DARED CLANG MAGIC LAPIN OPERA CHORD UNTIL QUAIL TACOS CLUNG '
    'ASPIC MOCHA OFTEN SOOTY FORTH MUSTY GRUEL CLEAN BLOCS'
).split(' ')

# Known letter mappings
store = {
    'A': 'a', 'C': 'a', 'H': 'b', 'I': 'a', 'K': 'a', 'L': 'a', 'N': 'a',
    'O': 'a', 'P': 'b', 'S': 'b', 'U': 'a'
}

# Dictionary of most common letters (to ease guessing)
# https://en.wikipedia.org/wiki/Letter_frequency
sortlet = {}
for i, l in enumerate('ETAOINSHRDLCUMWFGYPBVKJXQZ'):
    sortlet[l] = i

# The crib helper
crib = 'aaaaa abbaa aaabb'.split(' ')

# Build the full dictionary
for a in string.ascii_uppercase:
    if a not in store:
        store[a] = ' '

# Build candidate helpers based on the crib
candidates = []
for i, l in enumerate(letts):
    # Stop before we reach the end of the sentence
    if i == len(letts) - 2:
        break

    # Combine the next three letters to examine consistency
    longlett = ''.join(letts[i:i + 3])
    longcode = ''.join(crib)
    if countem(longlett, longcode):
        continue

    candidates.append(letts[i:i + 3])

print('Crib Candidates')
for c in candidates:
    print('  %s' % c)

chosen = 0

print("\nChosen Candidate: %s\n" % candidates[chosen])

# Assign values to the store based on the chosen crib candidate
for i in range(len(crib)):
    for j in range(len(candidates[chosen][i])):
        a = candidates[chosen][i][j]
        b = crib[i][j]
        store[a] = b

# Build map of possible letters
possmap = {}
for l in letts:
    poss = []
    for j in l:
        poss.append(store[j])
    possmap[l] = ''.join(poss)

possibs = {}
for i, l in enumerate(letts):
    possibs[l] = []
    for let in rules:
        c = matchem(possmap[l], rules[let])
        if c:
            possibs[l].append(let)

# Output report to facilitate guesses

# Letters
print(' '.join(letts))

# Mappings
print(' '.join(possmap[l] for l in letts))

# Possible Letters
maxletts = max(len(ll) for ll in possibs.values())
for x in range(maxletts):
    # Output letter, with blank if we ran out for this row
    for i, l in enumerate(letts):
        # Order possible letters by those most common in the English lexicon
        slet = []
        for w in sorted(sortlet, key=sortlet.get):
            if w in possibs[l]:
                slet.append(w)
        if len(slet) > x:
            sys.stdout.write('  %s   ' % slet[x])
        else:
            sys.stdout.write('      ')
    print
print

# Output grep statement for four letters before and after 'and' crib
makegrep(0, 4)
makegrep(7, 11)

'''
# Look for ways to limit letters
for l in letts:
    for p in possibs[l]:
        rule = rules[p]
        blanks = {}
        for i, let in enumerate(l):
            if store[let] == ' ':
                blanks[let] = rule[i]
'''

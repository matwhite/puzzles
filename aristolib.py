from pprint import pprint as pp
from random import shuffle
from collections import defaultdict
from subprocess import check_output, CalledProcessError
import re
import sys

'''
Synopsis:

    from aristolib import Aristo

    a = Aristo('HI THERE')
    a.stor = {'A': 'B', 'B': 'C'}
    a.repl()
'''

helptext = '''
REPL:

    show: show how the current dictionary looks mapped against the cryptogram

    set A=B: set a letter in the dictonary;
        format is crypto-letter=decrypted-letter

    unset A: unset a crypted letter

    dict: dump out the current dictionary (do this to save your work later)

    grep: print out grep commands to be used for searching
        (but see "find" below)

    popular: fill-in the dictionary by most popular letters in order of most
        popular letters in the cryptogram

    reset: unset the dictionary to start over

    find CRYPTOWORD: uses the dictonary and the patterns in the crytpo word
        to look for words that match (i.e., word length, repeating letters,
        and letters that do not match). Auto-sets the dictionary if only one
        word is found

    setword CRYPT=FOUND: set a crypto word to a given set of letters;
        useful when "find" finds a few words and you want to try them out

    brute: present a list of brute-forced solutions

    to exit: ctrl+d
'''


class Aristo(object):

    stor = {}
    c = ''
    ph = ''
    letts = ''
    lettcount = 0

    def __init__(self, c):
        self.c = c
        self.ph = re.sub(r'[^A-Z\s]', '', c)
        self.ph = re.sub(r'\s+', ' ', self.ph)
        self.letts = re.sub(r'\s', '', self.ph)
        self.lettcount = len(set(self.letts))

    def score(self):
        return(self.lettcount - len(self.stor.keys()))

    def repout(self):
        d = []
        for l in self.c:
            if l in self.stor:
                d.append(self.stor[l])
            else:
                d.append(' ')

        print('%s Score: %s' % (self.c, self.score()))
        print(''.join(d))

    def grepout(self):
        for w in self.ph.split(' '):
            print("# %s" % w)
            gr = "grep '^"
            for l in w:
                if l in self.stor:
                    gr += self.stor[l].lower()
                else:
                    gr += '[a-z]'
            print("%s$' /usr/share/dict/words" % gr)

    def apply_popular(self):
        sortlet = {}
        popular = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'
        for i, l in enumerate('ETAOINSHRDLCUMWFGYPBVKJXQZ'):
            sortlet[l] = i

        qty = defaultdict(int)
        for l in self.letts:
            qty[l] += 1
        pp(qty)

        i = 0
        for l in sorted(qty, key=qty.get, reverse=True):
            self.stor[l] = popular[i]
            i += 1

    def is_bad_candidate(self, word):
        try:
            check_output(
                ("grep -i '^%s$' /usr/share/dict/words" % word),
                shell=True
            )
        except CalledProcessError:
            return 1
        return 0

    def find_candidates(self, word):
        maps = defaultdict(list)
        for i, l in enumerate(word):
            maps[l].append(i)
        for l in list(maps.keys()):
            if len(maps[l]) < 2:
                del maps[l]

        gr = "grep -i '^"
        for l in word:
            if l in self.stor:
                gr += self.stor[l].lower()
            else:
                gr += '[a-z]'
        try:
            out = check_output(
                ("%s$' /usr/share/dict/words | tr A-Z a-z | uniq" % gr),
                shell=True
            )
        except CalledProcessError:
            return []

        wlist = [s.strip().decode('ascii') for s in out.splitlines()]

        # Strip words where non-matching or matching letter rules fail
        proper = []

        for ck in wlist:
            passes = 1
            z = list(zip(word, ck))
            for i, l in enumerate(z):
                if passes == 0:
                    break
                for j, k in enumerate(z):
                    if i == j:
                        continue
                    if z[i][0] != z[j][0] and z[i][1] != z[j][1]:
                        continue
                    elif z[i][0] == z[j][0] and z[i][1] == z[j][1]:
                        continue
                    else:
                        passes = 0
                        break

            if passes:
                proper.append(ck)

        return proper

    def setword(self, cw, dw):
        for i, l in enumerate(cw):
            self.stor[l.upper()] = dw[i].upper()

    # See if setting this word makes any other crypts fail to find a match
    def _trylist(self, sary):
        for ww in sary:
            swords = self.find_candidates(ww)
            # If we break matching, bail out and undo word
            if len(swords) == 0:
                return(0)
        return(1)

    # See if setting this word makes any other crypts fail to be words
    def _trybad(self):
        for w in self.ph.split(' '):
            word = ''
            for l in w:
                if l in self.stor:
                    word += self.stor[l].lower()
                else:
                    word += '.'
            res = self.is_bad_candidate(word)
            if res == 1:
                return(0)
        return(1)

    # Order list for bruteforce
    def pre_bf(self):
        return sorted(self.ph.split(' '), key=len, reverse=True)

    def bruteforce(self, ary):
        if len(ary) == 0:
            return

        erst = [l for l in set(ary[0]) if l not in self.stor.keys()]

        if len(erst) == 0:
            return self.bruteforce(ary[1:len(ary)])

        # Find list of words for next item in array
        words = self.find_candidates(ary[0])
        shuffle(words)
        for w in words:
            self.setword(ary[0], w)

            res = self._trylist(ary[1:len(ary)])
            if res != 1:
                for l in erst:
                    self.stor.pop(l)
                continue

            res = self._trybad()
            if res != 1:
                for l in erst:
                    self.stor.pop(l)
                continue
            else:
                break

        self.bruteforce(ary[1:len(ary)])

    def repl(self):
        self.repout()
        getin = None
        try:
            assert sys.version_info >= (3, 0)
            getin = input
        except:
            getin = raw_input

        while True:
            try:
                line = getin()
            except:
                break

            line.strip()
            if re.match(r'^show', line):
                self.repout()
            elif re.match(r'^set (.*)', line):
                let, to = re.match(r'^set (.*)', line).group(1).split('=')
                self.stor[let] = to
                self.repout()
            elif re.match(r'^unset (.*)', line):
                let = re.match(r'^unset (.*)', line).group(1)
                self.stor.pop(let)
                self.repout()
            elif re.match(r'^dict', line):
                pp(self.stor)
            elif re.match(r'^grep', line):
                self.grepout()
            elif re.match(r'^popular', line):
                self.apply_popular()
                self.repout()
            elif re.match(r'^reset', line):
                self.stor = {}
                self.repout()
            elif re.match(r'^find', line):
                ww = re.match(r'^find (.*)', line).group(1)
                cs = self.find_candidates(ww)
                if len(cs) == 1:
                    self.setword(ww, cs[0])
                    self.repout()
                else:
                    pp(cs)
            elif re.match(r'^setword', line):
                res = re.match(r'^setword (.*)=(.*)', line)
                self.setword(res.group(1), res.group(2))
                self.repout()
            elif re.match(r'^help', line):
                print(helptext)
                self.repout()
            elif re.match(r'^brute', line):
                words = self.pre_bf()
                self.bruteforce(words)
                self.repout()
                for _ in range(1, 5):
                    self.stor = {}
                    print(' ')
                    self.bruteforce(words)
                    self.repout()
                print('Done')
            else:
                print("Buh?")

#!/usr/bin/python

from pprint import pprint as pp
from nltk.corpus import stopwords

c = (
    'DAYDREAMING OF ESCAPING TO AN AWESOME PATH OF LAVISHLY BLANKETED '
    'VIRGIN MANTLE OF LIGHT IVORY, AGLOW. NATURE\'S BRIGHT LIGHT LUSTERS '
    'NIGHT. CINEMATIC PRISM OPENS HALOGENIC GLOW.'
)

pp(c)

w = c.split(' ')
pp(w)
eow = w[::2]
pp(eow)
eow = w[1::2]
pp(eow)
eow = w[::3]
pp(eow)
eow = w[1::3]
pp(eow)
eow = w[2::3]
pp(eow)

nostop = [x for x in w if not x.lower() in set(stopwords.words('english'))]
pp(nostop)

z = [[], [], [], []]
for x in nostop:
    for i in range(4):
        z[i].append(x[i])

pp(z)

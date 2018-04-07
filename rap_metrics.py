import nltk
from collections import Counter
from matplotlib import pyplot as plt
import numpy as np

hamiltons = ["""How does a bastard, orphan, son of a whore and a
Scotsman, dropped in the middle of a forgotten
Spot in the Caribbean by providence, impoverished, in squalor
Grow up to be a hero and a scholar?

The ten-dollar Founding Father without a father
Got a lot farther by working a lot harder
By being a lot smarter
By being a self-starter
By fourteen, they placed him in charge of a trading charter.

And every day while slaves were being slaughtered and carted
Away across the waves, he struggled and kept his guard up
Inside, he was longing for something to be a part of
The brother was ready to beg, steal, borrow, or barter

Then a hurricane came, and devastation reigned
Our man saw his future drip, dripping down the drain
Put a pencil to his temple, connected it to his brain
And he wrote his first refrain, a testament to his pain""",
"""Well, the word got around, they said, This kid is insane, man
Took up a collection just to send him to the mainland
Get your education, don't forget from whence you came, and
The world is gonna know your name. What's your name, man?
Alexander Hamilton
My name is Alexander Hamilton
And there's a million things I haven't done
But just you wait, just you wait
When he was ten his father split, full of it, debt-ridden
Two years later, see Alex and his mother bed-ridden
Half-dead sittin' in their own sick, the scent thick
And Alex got better but his mother went quick
Moved in with a cousin, the cousin committed suicide
Left him with nothing but ruined pride, something new inside
A voice saying
You gotta fend for yourself.
Alex, you gotta fend for yourself.
He started retreating and reading every treatise on the shelf"""]

stackoverflow = """The best package I've seen for this is Gensim,
 found at the Gensim Homepage. I've used it many times, and 
overall been very happy with it's ease of use; it is written
in Python, and has an easy to follow tutorial to get you 
started, which compares 9 strings. It can be installed via 
pip, so you won't have a lot of hassle getting it installed
I hope.

Which scoring algorithm you use depends heavily on the context 
of your problem, but I'd suggest starting of with the LSI 
functionality if you want something basic. (That's what the tutorial
walks you through.)

If you go through the tutorial for gensim, it will walk you through
comparing two strings, using the Similarities function. This will
allow you to see how your stings compare to each other, or to some
other sting, on the basis of the text they contain.

If you're interested in the science behind how it works, check out
this paper."""

nyt = """Zach Emig has arrived so early to pick up his children at
their Brooklyn elementary school that he has turned the cafeteria
into his ad hoc congressional campaign office, working on speeches
until school lets out.

Christina Hart spent so many bitter mornings waiting in the cold for
the bakery in Manhattan where she works to open that the entire crew 
now gets there early, a solution the owner cooked up so she wouldn't
quit.

And Matt Apter, a tour guide, has had to find refuge from inclement
weather in churches around Times Square because he arrives well before
his customers.

All three have this in common: They all use the New York City subway
to get where they need to be. Yes, the same subway that has become
the target of expletive-filled social media rants for its dependably
woeful performance. The same subway with an on-time rate that has
plunged to levels never before seen.

But the system's descent into chronic unreliability has become so
embedded in the psyches of riders that many are overcompensating,
adding extra time to their trips. In one of the more counterintuitive
conundrums to emerge from this confounding city, the subway has been
making people early."""

arpabet = nltk.corpus.cmudict.dict()

def extract_words(query):
    query = query.replace("\n", " ")
    query = query.split(" ")
    query = [''.join([c.lower() for c in word if c.isalpha()]).lower() for word in query]
    return query

def grouper(input_list, n = 2):
    for i in xrange(len(input_list) - (n - 1)):
        yield input_list[i:i+n]

def fibonacci_scaling_upto(cap):
    old = 1
    new = 1
    while True:
        old = new + old
        new, old = old, new
        if new <= cap:
            yield new
        else:
            break

def clusterability(vowels):
    """ Given a list of vowels, compute some measure of consistency."""
    vowel_total = float(len(vowels))
    vowel_counts = Counter(vowels)
    return sum([(vowel_counts[key] / vowel_total)**2 for key in vowel_counts])

def full_score(query):
    vowels = []
    for word in extract_words(query):
        try:
            vowel_words = [phoneme for phoneme in arpabet[word][0] if phoneme[0] in 'AEIOU']
            vowels.append(vowel_words)
        except KeyError:
            pass
    vowels = [item for sublist in vowels for item in sublist]

    # ok, try a boatload of scales
    score = []
    for scaling in [2, 3, 5, 8, 13, 21, 34, 55, 89, 144]:
        score_accumulator = []
        for grouping in grouper(vowels, scaling):
            score_accumulator.append(clusterability(grouping))
        score.append(sum(score_accumulator) / float(len(score_accumulator)))
    return np.array(score)

if __name__ == "__main__":
    hamilton_score_0 = full_score(hamiltons[0])
    hamilton_score_1 = full_score(hamiltons[1])
    stackoverflow_score = full_score(stackoverflow)
    nyt_score = full_score(nyt)
    average_score = (hamilton_score_0 + hamilton_score_1 + stackoverflow_score + nyt_score) / 4.0

    plt.plot(hamilton_score_0 - average_score, color='r')
    plt.plot(hamilton_score_1 - average_score, color='g')
    plt.plot(stackoverflow_score - average_score, color='b')
    plt.plot(nyt_score - average_score, color='k')
    plt.show()




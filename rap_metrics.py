import nltk
from collections import Counter

hamilton = """How does a bastard, orphan, son of a whore and a
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
And he wrote his first refrain, a testament to his pain"""

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

arpabet = nltk.corpus.cmudict.dict()

def extract_words(query):
	query = query.replace("\n", " ")
	query = query.split(" ")
	query = [''.join([c.lower() for c in word if c.isalpha()]).lower() for word in query]
	return query


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
	print len(vowels)
	print clusterability(vowels)

if __name__ == "__main__":
	full_score(hamilton)
	full_score(stackoverflow)




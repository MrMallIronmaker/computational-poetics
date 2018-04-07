import nltk
from collections import Counter
from matplotlib import pyplot as plt
import numpy as np

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

def full_score(query, vowels=True, consonants=True):
    vowels = []
    for word in extract_words(query):
        try:
            vowel_words = [
                phoneme for phoneme in arpabet[word][0] 
                if (vowels and phoneme[0] in 'AEIOU') 
                    or (consonants and phoneme[0] not in 'AEIOU')]
            vowels.append(vowel_words)
        except KeyError:
            pass
    vowels = [item for sublist in vowels for item in sublist]

    # ok, try a boatload of scales
    score = []
    for scaling in fibonacci_scaling_upto(len(vowels)):
        score_accumulator = []
        for grouping in grouper(vowels, scaling):
            score_accumulator.append(clusterability(grouping))
        score.append(sum(score_accumulator) / float(len(score_accumulator)))
    return np.array(score)

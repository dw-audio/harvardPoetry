# -*- coding: utf-8 -*-
"""
Created on Fri Jul  1 20:15:14 2022

@author: Dan
"""

import nltk  # you will need to run nltk.download('cmudict') first time
import random
import re


def rhyme(inp, subset=None):
    """Uses ntlk dictionary to find all the words that rhyme with input.

    PARAMETERS
    ----------
    inp : string
        input word
    subset : dict
        dictionary of words and their pronunciations
        see nltk.corpus.cmudict.entries() for an example
        and function make_pronunciation_list()

    RETURNS
    -------
    set(rhymes):
        set object containing all the words that rhyme with inp in either the
        cmudict or a subset of that dict
    """
    if subset:
        entries = subset
    else:
        entries = nltk.corpus.cmudict.entries()
    allPronunciations = entries.get(inp.lower())
    rhymes = []
    if allPronunciations is not None:  # if the input word is in the dictionary
        for pronunciation in allPronunciations:
            firstVowelIndex = findFirstVowel(pronunciation)
            for other_word, other_pronunciations in entries.items():
                if len(other_pronunciations) == 0:
                    print('yuo')
                for other_pronunciation in other_pronunciations:
                    if other_pronunciation[firstVowelIndex:] == pronunciation[firstVowelIndex:]:
                        rhymes.append(other_word)
    return set(rhymes)


def findFirstVowel(pronunciation_list):
    """Return the index of the first vowel in a list of pronunciation tokens"""
    v = [vowel(p) for p in pronunciation_list]
    return v.index(True)


def vowel(pronunciation_token):
    """Returns true if the pronunciation token contains a number,
    indicating it represents a vowel"""
    if re.findall('[0-9]', pronunciation_token):
        return True
    else:
        return False


def doTheyRhyme(word1, word2, subset=None):
    """Returns true if word1 and word2 rhyme

    PARAMETERS
    ----------
    word1 : string
    word2 : string
    subset : dict
        dictionary containing words and their possible pronunciations
        see nltk.corpus.cmudict.entries() for an example
    """
    # first, we don't want to report 'glue' and 'unglue' as rhyming words
    # those kind of rhymes are LAME
    if word1.find(word2) == len(word1) - len(word2):
        return False
    if word2.find(word1) == len(word2) - len(word1):
        return False
    return word1 in rhyme(word2, subset=subset)


def import_sentence_list(filename):
    """Returns a list of sentences from a file

    The file must be formatted with one sentence per line,
    with each sentence ending in a full stop.
    """
    with open(filename, 'r') as f:
        lines = f.readlines()
    return lines


def list_last_words(sentenceList):
    """Return a list of all the last words in a list of sentences"""
    return [sentence.split(' ')[-1].strip().strip('.')
            for sentence in sentenceList]


def last(sentence):
    """Returns the last word in a sentence"""
    return sentence.split(' ')[-1].strip().strip('.')


def make_pronunciation_dict(word_list):
    """
    Make a dict containing the pronunciations of the words in a list

    Parameters
    ----------
    word_list : list
        list of words

    Returns
    -------
    reducedEntries : dict where keys are words and values are a nested list
        of possible pronunciations. See nltk.corpus.cmudict.entries()
        for an example.
    """
    # directly reducing the corpus to a dict possibly loses some pronunciations
    # allEntries = dict(nltk.corpus.cmudict.entries())
    # So instead make a list of possibly pronunciations in the dict values
    allEntries = {}
    for word, pronunciation in nltk.corpus.cmudict.entries():
        if word in allEntries.keys():
            allEntries[word].append(pronunciation)
        else:
            allEntries[word] = [pronunciation]

    # dictionary comprehension to extract all key-value pairs from allEntries
    # where the key is in both the word list and the allEntries dict
    reducedEntries = {word: allEntries[word] for word in allEntries.keys() & word_list}

    return reducedEntries


def find_rhyming_sentences(sentenceList):
    """Find all the sentences that rhyme in a list of sentences"""
    last_words = list_last_words(sentenceList)
    # find the last word in all the sentences
    # make a list of how to pronounce all those words
    reducedEntries = make_pronunciation_dict(last_words)
    rhyming_sentences = []  # start an empty list of rhyming sentences
    while len(sentenceList) > 0:  # keep going until all sentences have been scanned
        # remove the current sentence from the list
        current_sentence = sentenceList.pop()
        # focus on the last word of this sentence
        current_word = last(current_sentence)
        # place the current working sentence in the list of rhyming sentences
        rhyming_sentences.append([current_sentence])
        # it may be that there are no rhymes for this, we will deal with that
        # later
        for other_sentence in sentenceList.copy():
            # loop through all the other sentences
            # (we take a copy of the sentenceList here to avoid modifying the
            # list we are looping over, python could get confused)
            # check the last word of the other sentence
            other_word = last(other_sentence)
            # check if the current word rhymes with the other word
            # print(f"Checking {current_word} and {other_word}")
            they_rhyme = doTheyRhyme(
                current_word, other_word, subset=reducedEntries)
            if they_rhyme:
                # place the other sentence next to the current sentence in the
                # big list of rhyming sentences
                rhyming_sentences[-1].append(other_sentence)
                # then remove it from the list of sentences so we don't see it
                # again next time we loop
                sentenceList.remove(other_sentence)
    # remove all entries from the rhyming sentences list which only have one
    # element (they don't rhyme with anything)
    return [lst for lst in rhyming_sentences if len(lst) > 1]


def poem(rhyming_sentences):
    """Print a random poem in ABAB form using the list of rhyming sentences"""
    couples = random.sample(
        rhyming_sentences, 2)  # take two bunches of random sentences
    repeat = True
    while repeat:  # keep trying to find pairs of sentences
        a = random.sample(couples[0], 2)
        b = random.sample(couples[1], 2)
        # until you find ones where the last words are not the same
        if last(a[0]) != last(a[1]) and last(b[0]) != last(b[1]):
            repeat = False
    print(a[0])
    print(b[0])
    print(a[1])
    print(b[1])


# %%
if __name__ == "__main__":
    sentenceList = import_sentence_list('harvard_trimmed.txt')
    rhyming_sentences = find_rhyming_sentences(sentenceList)

    # %%
    poem(rhyming_sentences)

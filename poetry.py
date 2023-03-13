# -*- coding: utf-8 -*-
"""
Created on Fri Jul  1 20:15:14 2022

@author: Dan
"""

import nltk  # you will need to run nltk.download('cmudict') first time
import random

def rhyme(inp, subset=None):
    """Uses ntlk dictionary to find all the words that rhyme with input. 
    
    PARAMETERS
    ----------
    inp : string
        input word 
    subset : list of 2-tuples 
        list of words and their pronunciations 
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
    syllables = [(word, syl) for word, syl in entries if word == inp]
    rhymes = []
    for (word, syllable) in syllables:
            rhymes += [word for word, pron in entries if pron[1:] == syllable[1:]]
    return set(rhymes)
 
def doTheyRhyme(word1, word2, subset=None):
    """Returns true if word1 and word2 rhyme
    
    PARAMETERS
    ----------
    word1 : string
    word2 : string 
    subset : list of 2-tuples 
        list of words and their pronunciations 
        see nltk.corpus.cmudict.entries() for an example
    """
    # first, we don't want to report 'glue' and 'unglue' as rhyming words
    # those kind of rhymes are LAME
    if word1.find(word2) == len(word1) - len(word2):
        return False
    if word2.find(word1) == len(word2) - len(word1): 
        return False
    return word1 in rhyme(word2, subset)

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
    return [sentence.split(' ')[-1].strip().strip('.') for sentence in sentenceList]


def last(sentence):
    """Returns the last word in a sentence"""
    return sentence.split(' ')[-1].strip().strip('.')

def make_pronunciation_list(word_list):
    """
    Make a list containing the pronunciations of the words in a list

    Parameters
    ----------
    word_list : list 
        list of words

    Returns
    -------
    reducedEntries : list of 2 tuples
           list of words and their pronunciations 
           see nltk.corpus.cmudict.entries() for an example

    """
    allEntries = nltk.corpus.cmudict.entries()
    reducedEntries = []
    for word, syl in allEntries:
        if word in word_list:
            reducedEntries.append((word, syl))
    return reducedEntries


def find_rhyming_sentences(sentenceList):
    """Find all the sentences that rhyme in a list of sentences"""
    last_words = list_last_words(sentenceList)  # find the last word in all the sentences
    reducedEntries = make_pronunciation_list(last_words)  # make a list of how to pronounce all those words 
    rhyming_sentences = []  # start an empty list of rhyming sentences 
    while len(sentenceList)>0:  # keep going until all sentences have been scanned
        current_sentence = sentenceList.pop()  # remove the current sentence from the list
        current_word = last(current_sentence)  # focus on the last word of this sentence
        rhyming_sentences.append([current_sentence])  # place the current working sentence in the list of rhyming sentences 
        # it may be that there are no rhymes for this, we will deal with that later
        for other_sentence in sentenceList.copy():  # loop through all the other sentences 
            # (we take a copy of the sentenceList here to avoid modifying the list we are looping over, python could get confused) 
            other_word = last(other_sentence)  # check the last word of the other sentence
            they_rhyme = doTheyRhyme(current_word, other_word, subset=reducedEntries)  # check if the current word rhymes with the other word 
            if they_rhyme: # 
                rhyming_sentences[-1].append(other_sentence) # place the other sentence next to the current sentence in the big list of rhyming sentences 
                sentenceList.remove(other_sentence)  # then remove it from the list of sentences so we don't see it again next time we loop
    # remove all entries from the rhyming sentences list which only have one element (they don't rhyme with anything)
    return [lst for lst in rhyming_sentences if len(lst)>1]  
    

def poem(rhyming_sentences):
    """Print a random poem in ABAB form using the list of rhyming sentences"""
    couples = random.sample(rhyming_sentences, 2)  # take two bunches of random sentences
    repeat=True 
    while repeat:  # keep trying to find pairs of sentences 
        a = random.sample(couples[0], 2)
        b = random.sample(couples[1], 2)
        if last(a[0]) != last(a[1]) and last(b[0]) != last(b[1]): # until you find ones where the last words are not the same
            repeat=False
    print(a[0])
    print(b[0])
    print(a[1])
    print(b[1])
    
            
if __name__ == "__main__":
    sentenceList = import_sentence_list('harvard_trimmed.txt')
    rhyming_sentences = find_rhyming_sentences(sentenceList)
    
    # %% 
    poem(rhyming_sentences)
        
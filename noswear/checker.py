# Copyright (c) 2021 FOSS-Devs
# See LICENSE in the project root for license information.
import os
import difflib

def get_data(path):
    return os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'data\\wordlist.txt'))

def check(string, similarity: float = 0.91, lib: str = None):
    if lib is None:
        with open(get_data("wordlist.txt"), "r") as words:
            badwords = words.read().splitlines()
    else:
        with open(get_data(lib), "r") as words:
            badwords = words.read().splitlines()
    #a = ["a", "@", "*"]
    #i = ["i", "*", "1", "!"]
    #o = ["o", "*", "@", "0"]
    #u = ["u", "*"]
    #v = ["v", "*"]
    #l = ["l", "1"]
    #e = ["e", "*", "3"]
    #s = ["s", "$", "5"]
    #t = ["t", "7"]
    spec_char = {"@": "a", "1": "i", "!": "i", "0": "o", "1": "l", "3": "e", "$": "s", "5": "s"}
    string = string.lower()
    for attr, value in spec_char.items():
        string = string.replace(attr, value)
    if ' ' in string:
        string = ' '.join(string.split())
        for word in string.split(' '):
            word = ''.join(filter(str.isalpha, word))
            for bad in badwords:
                if diffcheck(word, bad, similarity) or bad in word:
                    return True
    else:
        for bad in badwords:
            if bad in string:
                return True 
        if diffcheck(string, bad, similarity):
            return True
    return False

def diffcheck(word, badword, similarity: float):
    score = difflib.SequenceMatcher(None, word, badword).quick_ratio()
    if score >= similarity:
        return True
    return False
    

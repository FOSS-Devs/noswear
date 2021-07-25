# Copyright (c) 2021 FOSS-Devs
# See LICENSE in the project root for license information.
import os
import difflib

def get_data(path):
    return os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'data\\wordlist.txt'))

def check(string, similarity: float = 0.80, lib: str = None):
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
    spec_char = {"@": "a", "1": "i", "!": "i", "0": "o", "1": "l", "3": "e", "$": "s", "5": "s", "4": "a", "7": "t", "3": "e"}
    string = string.lower()
    for attr, value in spec_char.items():
        string = string.replace(attr, value)
    if ' ' in string:
        string = ' '.join(string.split())
        for word in string.split(' '):
            word = ''.join(filter(str.isalpha, word))
            for bad in badwords:
                if bad == word:
                    return True 
                elif len(word) == len(bad) and diffcheck(word, bad, similarity):
                    return True
                elif len(word) >= 4 and len(bad) > 3:
                    if bad in word or word in bad:
                        return True
    else:
        for bad in badwords:
            if bad == string:
                return True 
            elif len(string) == len(bad) and len(string) <= 12 and diffcheck(string, bad, similarity):
                return True
            elif len(string) >= 4 and len(bad) > 3:
                if bad in string or string in bad:
                    return True
    return False

def diffcheck(word, badword, similarity: float):
    score = difflib.SequenceMatcher(None, word, badword).quick_ratio()
    if score >= similarity:
        return True
    return False
    

# Copyright (c) 2021 FOSS-Devs
# See LICENSE in the project root for license information.
import os
import difflib

def get_data(path):
    _ROOT = os.path.abspath(os.path.dirname(__file__))
    _ROOT = _ROOT + "\\data\\"
    return os.path.join(_ROOT, path)

def check(sentence, similarity: float = 0.75, lib: str = None):
    if lib is None:
        with open(get_data("wordlist.txt"), "r") as words:
            lines = words.readlines()
    else:
        with open(get_data(lib), "r") as words:
            lines = words.readlines()
    wordlist = [l.replace("\n", "") for l in lines]
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
    sentence = sentence.lower()
    for attr, value in spec_char.items():
        sentence = sentence.replace(attr, value)
    for j in wordlist:
        if j in sentence:
            return True 
    if " " in sentence:
        sentence = " ".join(sentence.split())
        for i in sentence.split(" "):
            i = ''.join(filter(str.isalpha, i))
            if not diffcheck(sentence, similarity, lib):
                pass
            else:
                return True
    else:
        if diffcheck(sentence, similarity, lib):
            return True
    return False

def diffcheck(sentence, similarity: float = 0.75, lib: str = "wordlist.txt"):
    with open(get_data(lib), "r") as words:
        lines = words.readlines()
    wordlist = [l.replace("\n", "") for l in lines]
    for keyword in wordlist:
        score = difflib.SequenceMatcher(None, sentence.lower(), keyword).quick_ratio()
        if score >= similarity:
            return True
    return False
    

# Copyright (c) 2021 FOSS-Devs
# See LICENSE in the project root for license information.
import os

_ROOT = os.path.abspath(os.path.dirname(__file__))

def get_data(path):
    return os.path.join(_ROOT, path)

def checker(sentence):
    with open(get_data('wordlist.txt'), "r") as words:
        lines = words.readlines()
    wordlist = [l.replace("\n", "") for l in lines]
    a = ["a", "@", "*"]
    i = ["i", "*", "1", "!"]
    o = ["o", "*", "@", "0"]
    u = ["u", "*"]
    v = ["v", "*"]
    l = ["l", "1"]
    e = ["e", "*", "3"]
    s = ["s", "$", "5"]
    t = ["t", "7"]
    spec_char = {"!": "i", "@": "a", "$": "s"}
    sentence = sentence.lower()
    for attr, value in spec_char.items():
        sentence = sentence.replace(attr, value)
    for j in wordlist:
        if j in sentence:
            return True
    return False

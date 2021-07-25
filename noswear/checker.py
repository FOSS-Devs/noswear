# Copyright (c) 2021 FOSS-Devs
# See LICENSE in the project root for license information.
import os
import difflib

class noswear():
    badlibpath = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'data\\wordlist.txt'))
    whitelist = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'data\\clean.txt'))
    
    def __init__(self, string, similarity: float = 0.60, badlib = badlibpath, whitelist = whitelist):
        self.string = string
        self.similarity = similarity
        self.badlib = badlib
        self.whitelist = whitelist
        self.getresult = False
        self._check()

    def _check(self):#, string, similarity: float = 0.76, path = path):
        self.getresult = False
        with open(f"{self.badlib}", "r") as words:
            badwords = words.read().splitlines()
        with open(f"{self.whitelist}", "r") as whitelist:
            normal_words = whitelist.read().splitlines()
        spec_char = {"@": "a", "1": "i", "!": "i", "0": "o", "1": "l", "3": "e", "$": "s", "5": "s", "4": "a"}
        string = self.string.lower()
        for attr, value in spec_char.items():
            string = string.replace(attr, value)
        if ' ' in string:
            string = ' '.join(string.split())
            for word in string.split(' '):
                word = ''.join(filter(str.isalpha, word))
                for badword in badwords:
                    if not word in normal_words:
                        if self._checker(word, badword, self.similarity):
                            self.getresult = True
                            return self.getresult
        else:
            for badword in badwords:
                    if not string in normal_words:
                        if self._checker(string, badword, self.similarity):
                            self.getresult = True
                            return self.getresult
        return self.getresult

    def _diffcheck(self, word, badword, similarity: float):
        score = difflib.SequenceMatcher(None, word, badword, autojunk=False).ratio()
        if score >= similarity:
            return True
        return False

    def _checker(self, string, badword, similarity: float):
        if badword == string:
            return True 
        elif len(string) == len(badword) and self._diffcheck(string, badword, similarity):
            return True
        elif len(string) >= 6 and len(badword) > 3:
            if badword in string or string in badword:
                return True
        return False
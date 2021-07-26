# Copyright (c) 2021 FOSS-Devs
# See LICENSE in the project root for license information.
import os
import difflib

class noswear():
    badlibpath = os.path.join(os.path.abspath(os.path.dirname(os.path.abspath(__file__))), "wordlist.txt")
    whitelist = os.path.join(os.path.abspath(os.path.dirname(os.path.abspath(__file__))), "clean.txt")
    
    def __init__(self, string, sensitivity: float = 0.73, badlib = badlibpath, whitelist = whitelist):
        self.string = string
        self.sensitivity = sensitivity
        self.badlib = badlib
        self.whitelist = whitelist
        self.getresult = False
        self.fullresult = None
        self._check()

    def _check(self):
        self.getresult = False
        with open(f"{self.badlib}", "r") as words:
            badwords = words.read().splitlines()
        with open(f"{self.whitelist}", "r") as whitelist:
            normal_words = whitelist.read().splitlines()
        spec_char = {"@": "a", "1": "i", "!": "i", "0": "o", "1": "l", "3": "e", "$": "s", "5": "s", "4": "a"}
        string = self.string.lower()
        for attr, value in spec_char.items():
            string = string.replace(attr, value)
        if ' ' in string and len(string) > 9:
            string = ' '.join(string.split())
            for word in string.split(' '):
                word = ''.join(filter(str.isalpha, word))
                for badword in badwords:
                    if not word in normal_words:
                        if self._checker(word, badword, self.sensitivity):
                            self.getresult = True
                            return self.getresult
        elif ' ' in string and len(string) < 10:            
            string = ''.join(filter(str.isalpha, string))
            for badword in badwords:
                if not string in normal_words:
                    if self._checker(string, badword, self.sensitivity):
                        self.getresult = True
                        return self.getresult
        else:
            string = ''.join(filter(str.isalpha, string))
            for badword in badwords:
                if not string in normal_words:
                    if self._checker(string, badword, self.sensitivity):
                        self.getresult = True
                        return self.getresult
        return self.getresult

    def _diffcheck(self, word, badword, sensitivity: float):
        oversize = len(word) + 2
        undersize = len(word) - 2
        if len(badword) <= oversize and len(badword) >= undersize:
            score = difflib.SequenceMatcher(None, word, badword, autojunk=False).ratio()
            if score >= sensitivity:
                self.fullresult = {"method": 2, "badword": badword, "detected": word, "score": score}
                return True
        return False

    def _checker(self, string, badword, sensitivity: float):
        if badword == string:
            self.fullresult = {"method": 1, "badword": badword, "detected": string}
            return True 
        elif self._diffcheck(string, badword, sensitivity):
            return True
        elif len(string) > 3 and len(badword) > 3:
            if badword in string:
                self.fullresult = {"method": 3, "badword": badword, "detected": string}
                return True
        return False
# Copyright (c) 2021 FOSS-Devs
# See LICENSE in the project root for license information.
import os
import difflib
import textwrap
import re

class noswear():
    badlibpath = os.path.join(os.path.abspath(os.path.dirname(os.path.abspath(__file__))), "wordlist.txt")
    whitelist = os.path.join(os.path.abspath(os.path.dirname(os.path.abspath(__file__))), "clean.txt")
    
    def __init__(self, string, sensitivity: float = 80, badlib = badlibpath, whitelist = whitelist):
        self.string = string
        if sensitivity < 1 or sensitivity > 100:
            raise ValueError
        self.sensitivity = sensitivity / 8000
        self.score = None
        self.badlib = badlib
        self.whitelist = whitelist
        self.getresult = False
        self.fullresult = None
        self._check()

    def _check(self):
        with open(f"{self.badlib}", "r") as words:
            badwords = words.read().splitlines()
        with open(f"{self.whitelist}", "r") as whitelist:
            normal_words = whitelist.read().splitlines()
        spec_char = {"@": "a", "1": "i", "!": "i", "0": "o", "1": "l", "3": "e", "$": "s", "5": "s", "4": "a", "7": "t"}
        string = self.string.lower()
        for attr, value in spec_char.items():
            string = string.replace(attr, value)
        string = re.sub(r"[^a-zA-Z0-9]+", ' ', string)
        spaces = len(string.split())
        _first = string.replace(' ', '')
        for badword in badwords:
            if self._pre_check(_first, badword):
                self.getresult = True
                return self.getresult
        if spaces > 1 and len(string) > 9:
            string = ' '.join(string.split())
            for word in string.split(' '):
                for badword in badwords:
                    if not word in normal_words:
                        if self._checker(word, badword, self.sensitivity):
                            self.getresult = True
                            return self.getresult
        else:
            string = textwrap.wrap(string, 5)
            for badword in badwords:
                for word in string:
                    if not word in normal_words:
                        if self._checker(word, badword, self.sensitivity):
                            self.getresult = True
                            return self.getresult
        return self.getresult

    def _diffcheck(self, word, badword, sensitivity: float):
        oversize = len(word) + 2
        undersize = len(word) - 2
        if len(badword) <= oversize and len(badword) >= undersize:
            score = difflib.SequenceMatcher(None, word, badword, autojunk=True).quick_ratio()
            if score >= sensitivity:
                self.score = score
                return True
        return False

    def _checker(self, string, badword, sensitivity: float):
        x = len(string)
        sensitivity = (x ** 2) / 500 + 0.79 +  sensitivity
        if sensitivity > 1:
            sensitivity = 0.96
        self.fullresult = {"method": None, "badword": None, "detected": string, "score": self.score, "sensitivity": sensitivity}
        if badword == string:
            {"method": 1, "badword": badword, "detected": string, "score": self.score, "sensitivity": sensitivity}
            return True 
        elif len(string) <= 12 and self._diffcheck(string, badword, sensitivity):
            self.fullresult = {"method": 2, "badword": badword, "detected": string, "score": self.score, "sensitivity": sensitivity}
            return True
        return False

    def _pre_check(self,string, badword):
        if len(badword) > 3:
            if badword in string:
                self.fullresult = {"method": 0, "badword": badword, "detected": string, "score": self.score, "sensitivity": None}
                return True
        return False
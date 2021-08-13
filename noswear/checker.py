# Copyright (c) 2021 FOSS-Devs
# See LICENSE in the project root for license information.
import os
import difflib
#import textwrap
#import re
import json

class noswear():
    badlibpath = os.path.join(os.path.abspath(os.path.dirname(os.path.abspath(__file__))),"data", "wordlist.txt")
    whitelist = os.path.join(os.path.abspath(os.path.dirname(os.path.abspath(__file__))),"data", "clean.json")
    
    def __init__(self, string, difficulty: float = 80, badlib = badlibpath, whitelist = whitelist):
        if difficulty < 1 or difficulty > 100:
            raise ValueError
        self.string = string
        self.difficulty = difficulty / 1800
        self.score = None
        self.badlib = badlib
        self.whitelist = whitelist
        self.getresult = False
        self.fullresult = {"method": None, "badword": None, "word": None, "score": self.score, "difficulty": None}
        self._check()

    def _check(self):
        with open(f"{self.badlib}", "r") as words:
            badwords = words.read().splitlines()
        with open(f"{self.whitelist}", "r") as whitelist:
            normal_words = json.load(whitelist)
        spec_char = {"@": "a", "1": "i", "!": "i", "0": "o", "1": "l", "3": "e", "$": "s", "5": "s", "4": "a", "7": "t"}
        string = self.string.lower()
        for attr, value in spec_char.items():
            string = string.replace(attr, value)
        #string = re.sub(r"[^a-zA-Z0-9]+", ' ', string)
        string = ''.join(l for l in string if l.isalnum() or l == " ")
        string = ' '.join(string.split())
        spaces = len(string.split())
        no_space = string.replace(' ', '')
        if len(no_space) < 10 and spaces > 1:
            string = self._filter_clean_word(no_space, normal_words)
            for badword in badwords:
                if self._checker(string, badword, self.difficulty):
                    self.getresult = True
                    return self.getresult
        elif spaces > 1 and len(string) > 9:
            string = ' '.join(string.split())
            string = string.split(' ')
            string = self._filter_clean_word(string, normal_words)
            for word in string:
                for badword in badwords:
                    if self._checker(word, badword, self.difficulty):
                        self.getresult = True
                        return self.getresult
        else:
            no_space = self._filter_clean_word(no_space, normal_words)
            for badword in badwords:
                if self._simple_check(no_space, badword):
                    self.getresult = True
                    return self.getresult
        #else:
        #    string = textwrap.wrap(string, 5)
        #    string = self._filter_clean_word(string, normal_words)
        #    for badword in badwords:
        #        for word in string:
        #            if self._checker(word, badword, self.difficulty):
        #                self.getresult = True
        #                return self.getresult
        return self.getresult

    def _diffcheck(self, word, badword, difficulty: float):
        oversize = len(word) + 2
        undersize = len(word) - 2
        if len(badword) <= oversize and len(badword) >= undersize:
            score = difflib.SequenceMatcher(None, word, badword, autojunk=True).quick_ratio()
            if score >= difficulty:
                self.score = score
                return True
        return False

    def _checker(self, string, badword, difficulty: float):
        x = len(string)
        difficulty = (x ** 2) / 500 + 0.79 +  difficulty
        if difficulty > 1:
            difficulty = 0.96
        self.fullresult = {"method": None, "badword": None, "word": string, "score": self.score, "difficulty": difficulty}
        if badword == string:
            {"method": 2, "badword": badword, "word": string, "score": self.score, "difficulty": difficulty}
            return True 
        elif len(string) <= 12 and self._diffcheck(string, badword, difficulty):
            self.fullresult = {"method": 3, "badword": badword, "word": string, "score": self.score, "difficulty": difficulty}
            return True
        return False

    def _simple_check(self,string, badword):
        if len(badword) > 3:
            if badword in string:
                self.fullresult = {"method": 1, "badword": badword, "word": string, "score": self.score, "difficulty": None}
                return True
        return False

    def _filter_clean_word(self, string, normal_words):
        if type(string) is list:
            for w in normal_words:
                for word in string:
                    if word == w:
                        string.remove(word)
        else:
            for w in normal_words:
                if string == w:
                    string = string.replace(string, '')
        return string

noswear("hello").fullresult
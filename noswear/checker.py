def checker(sentence):
    with open("wordlist.txt", "r") as words:
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
    words = get_words()
    for i in sentence:
        for j in wordlist:
            if i.lower() == j.lower():
                return True
    return False
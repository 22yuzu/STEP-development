import sys

def make_hashtable(words):
    hashtable = {}

    for word in words:
        key = ''.join(sorted(word))
        if key not in hashtable:
            hashtable[key] = []
        hashtable[key].append(word)

    return hashtable


def find(word, table):
    key = ''.join(sorted(word))
    if key in table:
        return table[key]
    else:
        return []


def main():
    words = []

    with open("words.txt", "r") as f:
        for line in f:
            word = line.strip()
            if word != "":
                words.append(word)

    table = make_hashtable(words)

    for line in sys.stdin:
        word = line.strip()
        if word == "":
            continue
        ans = find(word, table)
        if len(ans) == 0:
            print("")
        else:
            print(" ".join(ans))

main()

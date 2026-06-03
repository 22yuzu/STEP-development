# 一応inputとoutputも意識

def make_hashtable(words):
    hashtable = {}
    for word in words:
        count = [0] * 26
        for ch in word:
            i = ord(ch) - ord('a')
            count[i] += 1
        key = tuple(count) 
        if key not in hashtable:
            hashtable[key] = []
        hashtable[key].append(word)
    return hashtable


def find(word, table):
    count = [0] * 26
    for ch in word:
        i = ord(ch) - ord('a')
        count[i] += 1
    key = tuple(count)
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

    while True:
        try:
            word = input().strip()
        except EOFError:
            break
        if word == "":
            continue
        ans = find(word, table)
        if len(ans) == 0:
            print("")
        else:
            print(" ".join(ans))

main()

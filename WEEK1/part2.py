import sys

SCORES = {
    "a": 1, "e": 1, "h": 1, "i": 1, "n": 1,
    "o": 1, "r": 1, "s": 1, "t": 1,
    "c": 2, "d": 2, "l": 2, "m": 2, "u": 2,
    "b": 3, "f": 3, "g": 3, "p": 3, "v": 3, 
    "w": 3, "y": 3,
    "j": 4, "k": 4, "q": 4, "x": 4, "z": 4
}

def make_wordlist(words):
    word_list = []

    for word in words:
        count = [0] * 26
        score = 0
        for ch in word:
            i = ord(ch) - ord('a')
            count[i] += 1
            score += SCORES[ch]
        word_list.append((score, word, count))

    word_list.sort(reverse=True)
    return word_list

def find(word, word_list):
    input_count = [0] * 26

    for ch in word:
        i = ord(ch) - ord('a')
        input_count[i] += 1

    for score, ans, count in word_list:
        can_make = True
        for i in range(26):
            if count[i] > input_count[i]:
                can_make = False
                break
        if can_make:
            return ans

    return ""

def main():
    data_file = sys.argv[1]
    dictionary_words = []

    with open("words.txt", "r") as f:
        for line in f:
            word = line.strip()
            if word != "":
                dictionary_words.append(word)

    input_words = []

    with open(data_file, "r") as f:
        for line in f:
            word = line.strip()
            if word != "":
                input_words.append(word)

    word_list = make_wordlist(dictionary_words)
    for word in input_words:
        ans = find(word, word_list)
        print(ans)

main()
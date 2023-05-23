def find_anagram(word, dictionary):
    """Find anagram of the input word in the dictionary.

    Using binary search to find the anagram.

    Args:
    word: A string of the input word.
    dictionary: A list of strings of the dictionary.

    Returns:
    A list of strings of the anagram of the input word.
    """
    if(dictionary == None or word == None or len(word) == 0 or len(dictionary) == 0):
        return None
    sorted_word = sorted(word)
    sorted_dictionary = []
    # sort each word in dictionary
    for word in dictionary:
        sorted_dictionary.append((sorted(word),word))
    # sort the dictionary
    sorted_dictionary.sort()
    
    anagrams = []
    l = 0
    r = len(sorted_dictionary) - 1
    while l <= r:
        mid = (l + r) // 2
        if sorted_dictionary[mid][0] == sorted_word:
            anagrams.append(sorted_dictionary[mid][1])
            l = mid + 1
        elif sorted_dictionary[mid][0] < sorted_word:
            l = mid + 1
        else:
            r = mid - 1
    return len(anagrams) > 0 and anagrams or "not found"

if __name__ == "__main__":
    # str = input("Enter a word: ")
    with open('anagram/words.txt') as f:
        dictionary = f.read().splitlines()
    # test cases
    str = ["cat","dog", "","a","acrosticallyptah","fjodhau;hfomapofgjhfahuasdhfjpsdjop:", "statueofliberty", "silent"]
    for i in range(len(str)):
        ans = find_anagram(str[i], dictionary)
        print(ans)


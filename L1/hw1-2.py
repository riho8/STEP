from collections import Counter

def check_score(word):
    """Calculates the score of the word.

    Using the input word and score rule, computes the total score of the word.

    Args:
    word: A string to calculate the score.

    Returns:
    An int value of the calculated score.
    """
    score = 0
    score_arr = [1, 3, 2, 2, 1, 3, 3, 1, 1, 4, 4, 2, 2, 1, 1, 3, 4, 1, 1, 1, 2, 3, 3, 4, 3, 4]
    for char in word:
        score += score_arr[ord(char) - ord('a')]
    return score

def is_anagram(base_counter_dict, dictionary_counter_dict):
    """Checks if a word from dictionary is an anagram of target word.

    Compares the character counts in dictionary_counter_dict with the character counts
    in base_counter_dict. Returns True if dictionary_counter_dict word can be formed 
    using the characters in base_counter_dict.

    Args:
    base_counter_dict: A dictionary representing the character counts of the target word.
    dictionary_counter_dict: A dictionary representing the character counts of a word from dictionary.

    Returns:
    A boolean value indicating whether dictionary_counter_dict is an anagram of base_counter_dict.
    """
    for char, count in dictionary_counter_dict.items():
        if char not in base_counter_dict or count > base_counter_dict[char]:
            return False
    return True

def find_anagram(word_file, dictionary):
    """Find best anagram of each word in the input file in the dictionary.

    Using the input word and score rule, finds the anagram of each word which has the highest score.

    Args:
    word_file: input file name.
    dictionary: A list of strings of the dictionary.

    Returns:
    A list of strings of the best anagram of each word in the input file.
    """	
    if(dictionary == None or word_file == None or len(dictionary) == 0):
        return None
    with open(word_file) as f:
        words = f.read().splitlines()
    sorted_words = [''.join(sorted(word)) for word in words]
    sorted_dictionary = [''.join(sorted(word)) for word in dictionary]
    word_to_counter_list = [(word, Counter(word)) for word in sorted_words]
    dictionary_to_counter_list = [(word, Counter(word)) for word in sorted_dictionary]
    score_sorted_dictionary_list = sorted(dictionary_to_counter_list, key=lambda x: check_score(x[0]), reverse=True)
    anagrams = []

    for i in range(len(word_to_counter_list)):
        ans = ""        
        for j in range(len(score_sorted_dictionary_list)):
            if is_anagram(word_to_counter_list[i][1], score_sorted_dictionary_list[j][1]) == True:
                ans = dictionary[sorted_dictionary.index(score_sorted_dictionary_list[j][0])]
                break
        anagrams.append(ans)
        
    return anagrams


# python3 score_checker.py small.txt small_answer.txt
# python3 score_checker.py medium.txt medium_answer.txt
# python3 score_checker.py large.txt large_answer.txt

if __name__ == "__main__":      
    target = input("Type s or m or l: ")

    with open('anagram/words.txt') as f:
            dictionary = f.read().splitlines()
    if target == 's':
        anagram = find_anagram("anagram/small.txt", dictionary)
        with open('anagram/small_answer.txt', 'w') as f:
                for item in anagram:
                    f.write("%s\n" % item)
        print("small done")
    elif target == 'm':
        anagram = find_anagram("anagram/medium.txt", dictionary)
        with open('anagram/medium_answer.txt', 'w') as f:
                for item in anagram:
                    f.write("%s\n" % item)
        print("medium done")
    elif target == 'l':
        anagram = find_anagram("anagram/large.txt", dictionary)
        with open('anagram/large_answer.txt', 'w') as f:
                for item in anagram:
                    f.write("%s\n" % item)
        print("large done")
    else:
        print("wrong input")

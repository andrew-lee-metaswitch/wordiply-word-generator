from typing import List
from wordfreq import zipf_frequency
from nltk.corpus import words
import json

# Install the 'populat' words'
# import nltk
# nltk.download()

word_list: List[str] = words.words()


def get_all_words_by_substring(starting_word: str) -> List[str]:
    """
    Returns a list of words that the starting_word is a substring of, sorted by word length
    e.g. get_all_words_by_substring("moon") = ["moons", "moons", .... "moonwalker"]
    """
    return sorted(
        [w for w in word_list if starting_word in w],
        key=lambda w: len(w),
    )


# Reasonable Zipf values are between 0 and 8,
# but because of the cutoffs described above,
# the minimum Zipf value appearing in these lists is 1.0
# for the 'large' wordlists and 3.0 for 'small'.
#  We use 0 as the default Zipf value
# for words that do not appear in the given wordlist,
#  although it should mean one occurrence per billion words.
def is_word_common(word: str) -> bool:
    return zipf_frequency(word, "en") > 0


def is_longest_word_common(starting_word: str) -> bool:
    words_it_is_substring_of = get_all_words_by_substring(starting_word)
    longest_word_length = len(words_it_is_substring_of[-1])
    longest_words = [
        w for w in words_it_is_substring_of if len(w) == longest_word_length
    ]
    # print(longest_words)
    # p#rint([(is_word_common(w) for w in longest_words)])
    return any([(is_word_common(w) for w in longest_words)])


def get_common_words(wl: List[str]) -> List[str]:
    return [w for w in wl if is_word_common(w)]


def get_possible_start_words() -> List[str]:
    return


POTENTIAL_STARTING_WORDS_LIST = [
    w for w in word_list if len(w) in [3, 4, 5] and zipf_frequency(w, "en") > 4
]
AUTOGEN_LIST = {}
for starting_word in POTENTIAL_STARTING_WORDS_LIST:

    if starting_word[0].isupper():
        continue

    # First find all the words that the starting words is a substring of
    wordiply_answers = get_all_words_by_substring(starting_word)
    longest_word_length = len(wordiply_answers[-1])

    if longest_word_length < 10:
        continue

    # Next get all the common words we can make from this word
    common_wordiply_answers_of_longest_length = [
        w
        for w in wordiply_answers
        if is_word_common(w) and len(w) == longest_word_length and not w[0].isupper()
    ]

    if not common_wordiply_answers_of_longest_length:
        continue

    # If the longest word that can be make is 10 letters o longer, and if at least one of the
    # word of longest length is a common word, then this is a good starting word!
    if common_wordiply_answers_of_longest_length:
        AUTOGEN_LIST[starting_word] = {
            w: zipf_frequency(w, "en")
            for w in common_wordiply_answers_of_longest_length
        }

with open("goodwordiplyopeners.json", "w") as f:
    json.dump(AUTOGEN_LIST, f, indent=2)

from typing import List
from wordfreq import zipf_frequency
from nltk.corpus import words
import json

# Install the 'populat' words'
# import nltk
# nltk.download()

word_list: List[str] = words.words()

# Find all words of length 3,4,5, that are not proper nouns that are 'common'
# We use a zipf_frequency of 4 (one word in every 100,000) to define commonness.
POTENTIAL_STARTING_WORDS_LIST = [
    w
    for w in word_list
    if len(w) in [3, 4, 5] and zipf_frequency(w, "en") > 4 and not w[0].isupper()
]
AUTOGEN_LIST = {}
for starting_word in POTENTIAL_STARTING_WORDS_LIST:

    # First find all the words that the starting words is a substring of, sorted by word-length
    wordiply_answers = sorted(
        [w for w in word_list if starting_word in w],
        key=lambda w: len(w),
    )

    # If the longest word isn't very long this isn't very interesting.
    longest_word_length = len(wordiply_answers[-1])
    if longest_word_length < 10:
        continue

    # Next get all the common words of longest length we can make from this word
    # This is all words with a zipf_frequency > 0 - this means more common than
    # every one word in a billion.
    common_wordiply_answers_of_longest_length = [
        w
        for w in wordiply_answers
        if zipf_frequency(w, "en") > 0
        and len(w) == longest_word_length
        and not w[0].isupper()
    ]

    # If at least one of the word of longest length is a common word,
    # then this is a good starting word!
    if common_wordiply_answers_of_longest_length:
        AUTOGEN_LIST[starting_word] = {
            w: zipf_frequency(w, "en")
            for w in common_wordiply_answers_of_longest_length
        }

with open("goodwordiplyopeners.json", "w") as f:
    json.dump(AUTOGEN_LIST, f, indent=2)

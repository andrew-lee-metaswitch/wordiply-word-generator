# wordiply-word-generator

Generate starting words for [`wordiply`](https://www.wordiply.com/) game

These are words that are:
  - Between 3 and 5 letters long
  - Are common words in their own right
  - Are substrings of much longer words (i.e. words of at least 10 letters)
  - Of all of the words that are of the longest length, at least one of them is 'common'

We define commonness using https://pypi.org/project/wordfreq/ - any positive value for the `zipf_frequency` - deems a word to be common

Requirements:
 - python3
 - install wordfrew and nltk
```
pip install wordfreq
pip install nltk
```
  - Use `nltk` to download the 'popular' word list
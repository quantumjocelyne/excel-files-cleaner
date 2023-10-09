
import operator
import ast
import unittest

class HighScoringWords:
    MAX_LEADERBOARD_LENGTH = 100
    MIN_WORD_LENGTH = 3
    letter_values = {}
    valid_words = []

    def __init__(self, validwords='wordlist.txt', lettervalues='letterValues.txt'):
        """
        Initialise the class with complete set of valid words and letter values
        by parsing text files containing the data
        :param validwords: a text file containing the complete set of valid
        words, one word per line
        :param lettervalues: a text file containing the score for each letter in
        the format letter:score one per line
        :return:
        """
        self.leaderboard = []
        self.wordscore = {}
        with open(validwords) as f:
            self.valid_words = f.read().splitlines()

        with open(lettervalues) as f:
            for line in f:
                key, val = line.split(':')
                self.letter_values[str(key).strip().lower()] = int(val)

    def build_leaderboard_for_word_list(self):
        """
        Build a leaderboard of the top scoring
         MAX_LEADERBOARD_LENGTH words from the complete set of valid words.
        :return: The list of top words
        """
        self._match(self.valid_words, self.wordscore)
        word_score = self._sorted(self.wordscore)
        self.leaderboard = [w[0] for w in word_score][:self. MAX_LEADERBOARD_LENGTH]

        return self.leaderboard

    def build_leaderboard_for_letters(self, starting_letters):
        """
        Build a leaderboard of the top scoring MAX_LEADERBOARD_LENGTH words that
        can be built using only the letters contained in the starting_letters
        string.
        The number of occurrences of a letter in the startingLetters String IS
        significant. If the starting letters are bulx, the word "bull" is NOT
        valid.
        There is only one l in the starting string but bull contains two l
        characters.
        Words are ordered in the leaderboard by their score (with the highest
        score first) and then alphabetically for words which have the same score
        :param starting_letters: a random string of letters from which to build
        words that are valid against the contents of the wordlist.txt file.
        :return:
        """
        words_starting_letters = []
        value = {}
        for word in self.valid_words:
            if word[:len(starting_letters)] == starting_letters:
                words_starting_letters.append(word)
                self._match(words_starting_letters, value)
        set = self._sorted(value)
        return [w[0] for w in set][:self. MAX_LEADERBOARD_LENGTH]


    def _match(self, validword, dict):
        """
        Dictionary for valid words
        """
        for word in validword:
            dict[word] = 0
            for l in word:
                dict[word] += self.letter_values[l]

    def _sorted(self, revscore):
        """
        Words are ordered in the leaderboard by their score (with the highest
        score first) and then alphabetically for words which have the same score
        """

        return sorted(revscore.items(), key=operator.itemgetter(1), reverse=True)




class TestHighScoringWords(unittest.TestCase):

    def setUp(self):
            self.main_list = HighScoringWords('wordlist.txt')
            self.testing = HighScoringWords('wordlist.txt')
            self._100hsw = self.main_list.build_leaderboard_for_word_list()


    def test_initialisation(self):
        self.assertEqual(self.testing.leaderboard, [])
        self.assertEqual(self.testing.valid_words[0], 'aa')
        self.assertEqual(self.testing.letter_values['a'], 1)

    def test_values(self):
        self.testing.build_leaderboard_for_word_list()
        self.assertEqual(self.testing.wordscore['razzamatazzes'], 51)

    def test_leaderboard_for_word_list(self):
        highest = self.testing.build_leaderboard_for_word_list()
        self.assertEqual(highest[0], 'razzamatazzes')
        self.assertEqual(highest[1], 'razzmatazzes')

    def test_scores(self):
        words, scores = self.testing.valid_words, self.testing.wordscore
        self.testing._match(words, scores)
        self.assertEqual(self.testing.wordscore['aal'], 3)

    def test_max_leaderboard_length(self):
        self.assertEqual(len(self._100hsw), 100)

    def test_max_min_100hsw(self):
        self.assertEqual(self._100hsw[0], 'razzamatazzes')
        self.assertEqual(self._100hsw[-1], 'cyclohexylamines')
        self.assertEqual(self._100hsw[-2],'compartmentalizations')


    def test_sorting(self):
        words, score = self.testing.valid_words, self.testing.wordscore
        self.testing._match(words, score)
        highest = self.testing._sorted(self.testing.wordscore)
        self.assertEqual(highest[0], ('razzamatazzes', 51))
        self.assertEqual(highest[1], ('razzmatazzes', 50))
        self.assertEqual(highest[-2], ('us', 2))
        self.assertEqual(highest[-1], ('ut', 2))



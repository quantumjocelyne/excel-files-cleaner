# !/usr/bin/env python
# -*- coding: utf8 -*-

# Python 3.7.2

import unittest
from Geekstatic_ import HighScoringWords

class TestHighScoringWords(unittest.TestCase):
    def setUp(self):
        self.test_list = HighScoringWords('testlist.txt')
        self.long_list = HighScoringWords('wordlist.txt')
        self.top_100 = self.long_list.build_leaderboard_for_word_list()

    def test_initialises_properly(self):
        self.assertEqual(self.test_list.leaderboard, [])
        self.assertEqual(self.test_list.valid_words[0], 'aa')
        self.assertEqual(self.test_list.letter_values['a'], 1)

    def test_word_values(self):
        self.test_list.build_leaderboard_for_word_list()
        self.assertEqual(self.test_list.wordscore['aardwolves'], 17)

    def test_word_leaderboard_list(self):
        highest = self.test_list.build_leaderboard_for_word_list()
        self.assertEqual(highest[0], 'aardwolves')
        self.assertEqual(highest[1], 'aardwolves')

    def test_word_score_hash(self):
        words, scores = self.test_list.valid_words, self.test_list.wordscore
        self.test_list._match(words, scores)
        self.assertEqual(self.test_list.wordscore['aardvarks'], 17)

    def test_does_not_exceed_max_leaderboard_limit(self):
        self.assertEqual(len(self.top_100), 100)

    def test_first_and_last_of_top_100(self):
        self.assertEqual(self.top_100[0], 'razzamatazzes')
        self.assertEqual(self.top_100[-1], 'cyclohexylamines')

    def test_reverse_and_sort(self):
        words, scores = self.test_list.valid_words, self.test_list.wordscore
        self.test_list._match(words, scores)
        highest = self.test_list._sorted(self.test_list.wordscore)
        self.assertEqual(highest[0], ('aardvarks', 17))
        self.assertEqual(highest[1], ('aardwolves', 17))

    def test_filter_by_starting_string(self):
        first_5 = self.test_list.build_leaderboard_for_letters('aardw')
        psychos = self.long_list.build_leaderboard_for_letters('psycho')
        tests = self.long_list.build_leaderboard_for_letters('test')
        self.assertEqual(first_5, ['aardwolves', 'aardwolf'])
        self.assertEqual(psychos[0], 'psychophysiologically')
        self.assertEqual(tests[:2], ['testamentary', 'testifying'])
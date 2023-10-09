__author__ = 'jocelyne'


class HighScoringWords:
    MAX_LEADERBOARD_LENGTH = 100  # the maximum number of items that can appear in the leaderboard
    MIN_WORD_LENGTH = 3  # words must be at least this many characters long
    letter_values = {}
    valid_words = []

    def __init__(self, validwords='wordlist.txt', lettervalues='letterValues.txt'):
        """
        Initialise the class with complete set of valid words and letter values by parsing text files containing the data
        :param validwords: a text file containing the complete set of valid words, one word per line
        :param lettervalues: a text file containing the score for each letter in the format letter:score one per line
        :return:
        """
        self.leaderboard = []  # initialise an empty leaderboard
        self.word_scores = {}
        self.threshold = 0
        with open(validwords) as f:
            self.valid_words = f.read().splitlines()

        with open(lettervalues) as f:
            for line in f:
                (key, val) = line.split(':')
                self.letter_values[str(key).strip().lower()] = int(val)

    def build_leaderboard_for_word_list(self):
        """
        Build a leaderboard of the top scoring MAX_LEADERBOAD_LENGTH words from the complete set of valid words.
        :return:
        """

        # Build the leaderboard using the build_leaderboard method and default arguments
        self.leaderboard = self.build_leaderboard()

    def build_leaderboard_for_letters(self, starting_letters):
        """
        Build a leaderboard of the top scoring MAX_LEADERBOARD_LENGTH words that can be built using only the letters contained in the starting_letters String.
        The number of occurrences of a letter in the startingLetters String IS significant. If the starting letters are bulx, the word "bull" is NOT valid.
        There is only one l in the starting string but bull contains two l characters.
        Words are ordered in the leaderboard by their score (with the highest score first) and then alphabetically for words which have the same score.
        :param starting_letters: a random string of letters from which to build words that are valid against the contents of the wordlist.txt file
        :return:
        """

        # Make a list from the string
        search_letters = list(starting_letters)

        # Initialise an empty list of matches that match our starting letters
        matches = []
        for word in self.valid_words:

            # Skip if the word is not in 5-15 range, move on to next word
            if len(word) not in range(5, 16):
                continue

            # Get the letters in the candidate word
            cand = list(word)

            # Counter for the number of matched letters
            match_count = 0

            # Loop through the letters in our starting letters
            for letter in search_letters:
                # print('Letter=',letter)
                if letter in cand:
                    i = cand.index(letter)
                    # print("i =",i)
                    cand.pop(i)
                    # print(cand)
                    match_count += 1

            # Success if all letters have been matched, add match to list of matches
            if match_count == len(word):
                matches.append(word)

        # Check if the full leaderboard is built, if not build it now
        if self.leaderboard == []:
            self.build_leaderboard_for_word_list()

        new_leaderboard = self.build_leaderboard(scores=self.word_scores, words=matches)

        # Return the leaderboard for letters_list as a list
        return new_leaderboard

    def build_leaderboard(self, words=None, scores=None):
        '''
        Generic method to build a leaderboard

        words: A list of words to use to construct a leaderboard, if value is None then it uses self.valid_words
        scores: A dictionary of (word,score) key-val pairs, if value is None it builds them
        '''
        # Our leaderboard list of words
        leaderboard = []
        # Our threshold for entry into the leaderboard, will be the minimum score
        threshold = 0

        # If none, use the full list of valid words
        if words == None:
            words = self.valid_words

        for word in words:
            # Skip if the word is less than minimum length
            if len(word) < self.MIN_WORD_LENGTH:
                continue

            # If no scores given as an argument, then build scores for the class as you go
            if scores == None:
                score = 0
                for letter in list(word):
                    score += self.letter_values[letter]

                self.word_scores[word] = score

            # If the leaderboard is still not full, add this word
            if len(leaderboard) < self.MAX_LEADERBOARD_LENGTH:
                leaderboard.append(word)
                # Recalculate the threshold
                threshold = min([self.word_scores[word] for word in leaderboard])

            # If the leaderboard is full but this word has a high enough score, add and adjust the threshold
            elif self.word_scores[word] > threshold:
                leaderboard.append(word)
                threshold = min([self.word_scores[word] for word in leaderboard])

                # Pick the (ambigious) loser, who has the lowest score and drop them from the list
                loser = [self.word_scores[word] for word in leaderboard].index(threshold)
                leaderboard.pop(loser)

        # Sort by the negative of the score (saves reversing)
        leaderboard.sort(key=lambda word: (-self.word_scores[word], word))
        return leaderboard


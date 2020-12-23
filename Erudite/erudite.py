# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : Nazariy Kutsalaba
# Collaborators : -
# Time spent    : 2 days

import math
import random
import string
from functools import reduce
import re
import copy

# constants
VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7
WILDCARD = '*'
EXIT_THE_GAME = '!!'

# max number of allowed hands
MAX_HANDS = 6

SCRABBLE_LETTERS_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4,
    'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1,
    'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1,
    's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8,
    'y': 4, 'z': 10
}

WORDLIST_FILENAME = "words.txt"


class Erudite:
    """
    This class describes the game "Erudite"

    Methods
    -------
    play_game()
        This function controls the process of drawing all hands.
        There is a dialogue with the user, and the results are displayed on the screen.
    """

    __WORDLIST = list()

    def __init__(self):
        """
        The class attributes are initialized in this constructor
        """

        self.__total_one_hand = 0

    @classmethod
    def __get_all_words(cls):
        """
        Returns a list of valid words. Words are strings of lowercase letters.

        Depending on the size of the word list, this function may
        take a while to finish.
        """

        if not cls.__WORDLIST:
            inFile = open(WORDLIST_FILENAME, 'r')

            for line in inFile:
                cls.__WORDLIST.append(line.strip().lower())

        return cls.__WORDLIST

    @staticmethod
    def __deal_hand():
        """This function randomly selects letters from VOWELS and CONSONANTS,
            and adds them to the dictionary, as well as adds a WILDCARD.

        :returns: dictionary (string -> int)

        """

        hand = dict()
        num_vowels = int(math.ceil(HAND_SIZE / 3))

        for i in range(num_vowels - 1):
            x = random.choice(VOWELS)
            hand[x] = hand.get(x, 0) + 1

        for i in range(num_vowels, HAND_SIZE):
            x = random.choice(CONSONANTS)
            hand[x] = hand.get(x, 0) + 1

        hand[WILDCARD] = 1

        return hand

    @staticmethod
    def __get_word_score(word, num):
        """This feature counts the number of points for a guessed word

        :param: word : string, that is guessed word
        :param: num : int, the number of letters left in the current hand
        :returns: the score for a word. Assumes the word is a valid word.

        """

        sum_of_points = sum(list(map(lambda char: SCRABBLE_LETTERS_VALUES[char] if char != WILDCARD else 0, word)))
        coefficient = max(1, HAND_SIZE * len(word) - 3 * (num - len(word)))
        return sum_of_points * coefficient

    @staticmethod
    def __get_frequency_dict(sequence):
        """This function converts a list or string of characters into a dictionary

        :param: sequence : string or list
        :returns: dictionary, where the keys are elements of the sequence
            and the values are integer counts, for the number of times that
            an element is repeated in the sequence.

        """

        # freqs: dictionary (element_type -> int)
        freq = dict()
        for x in sequence:
            freq[x] = freq.get(x, 0) + 1
        return freq

    @staticmethod
    def __letters_hand(hand):
        """This function converts values from the dictionary to a string

        :param hand : dictionary (string -> int)
        :returns: string, with letters
        """

        roster = list()
        for letter in hand.keys():
            for j in range(hand[letter]):
                roster.append(letter)
        return ' '.join(roster)

    def __update_hand(self, letters_word, hand):
        """This function updates the new_hand. Updates the hand: uses up the letters in the given word
            and returns the new hand, without those letters in it. Has no side effects: does not modify hand.

        :param: letters_word : string, that is guessed word
        :param: hand : dictionary (string -> int)
        :returns: dictionary (string -> int) with mofified hand
        """

        modified_hand = dict()

        for key, value in hand.items():

            if key in letters_word and letters_word[key] < value:
                if letters_word[key] != 0:
                    modified_hand[key] = value - letters_word[key]

            elif key not in letters_word:
                modified_hand[key] = value
        return modified_hand

    def __is_valid_word(self, word, hand):
        """This function checks if the entered word is in the word list.

        :param: word : string, that is guessed word
        :param: hand : dictionary (string -> int)
        :returns: True if word is in the word_list. Otherwise, returns False.
        """

        if WILDCARD in word:
            for vowel in VOWELS:
                temp_word = re.sub('[*]', vowel, word)
                if temp_word in self.__get_all_words():
                    return True

        letters_word = self.__get_frequency_dict(word)

        if word in self.__get_all_words():
            for key, value in letters_word.items():
                if key not in hand or value > hand[key]:
                    return False
            return True
        return False

    @staticmethod
    def __check_input():
        '''This function check the correct input numbers.

        :returns: number of hands
        '''

        while True:
            number_input = input('Enter total number of hands: ')

            if number_input.isdigit():
                if MAX_HANDS > int(number_input) > 0:
                    break
            print(f'Please, enter a number from 1 to {MAX_HANDS}.')
        return int(number_input)

    def __substitute_hand(self, hand, initial_hand):
        """This function changes the letter of the hand selected by the user to any other hand
        that is not part of this hand.

        :param: initial_hand: dictionary (string -> int), that is a hand on the current game circuit
        :param: hand : dictionary (string -> int)
        :returns: dictionary (string -> int), the hand from which the player will start his game
        """

        roster = list()
        new_input = input("Would you like to substitute a letter? ")

        if new_input == 'yes':
            letter = input("Which letter would you like to replace: ")
            letter = letter.lower()

            if letter not in initial_hand:
                return hand

            for char in CONSONANTS + VOWELS:
                if char not in initial_hand:
                    roster.append(char)

            new_letter = random.choice(roster)

            if hand[letter] == 1:
                del hand[letter]
            else:
                hand[letter] = hand[letter] - 1
            hand[new_letter] = 1
        return hand

    def __game_results_output(self, hand):
        """This function displays the final results for the current hand.

        :param: hand : dictionary (string -> int)
        """

        if not hand:
            print("Ran out of letters")
            print(f'Total score for this hand: {self.__total_one_hand}')
            print('-' * 10)

        else:
            print(f'Total score for this hand: {self.__total_one_hand}')
            print('-' * 10)

    def __play_hand(self, initial_hand):
        """This function controls the process of drawing one hand. Conducts a dialogue with the user,
            as well as displays the results on the screen.

        :param: initial_hand: dictionary (string -> int), that is a hand on the current game circuit

        """

        print(f'Current hand: {self.__letters_hand(initial_hand.copy())}')
        hand = self.__substitute_hand(initial_hand.copy(), initial_hand)
        num = HAND_SIZE

        while len(hand) >= 1:
            print(f'Current hand: {self.__letters_hand(hand)}')
            word = input("Enter word, or “!!” to indicate that you are finished: ").lower()

            if word == EXIT_THE_GAME:
                break

            if self.__is_valid_word(word, hand):
                total = self.__get_word_score(word, num)
                self.__total_one_hand += total
                hand = self.__update_hand(self.__get_frequency_dict(word), hand)
                print(f'"{word}" earned {total} points. Total: {self.__total_one_hand} points')
                print()

            else:
                hand = self.__update_hand(self.__get_frequency_dict(word), hand)
                print("That is not a valid word. Please choose another word.")
                print()

            num = sum(hand.values())

        self.__game_results_output(hand)

    def play_game(self):
        '''This function controls the process of drawing all hands.
            There is a dialogue with the user, and the results are displayed on the screen.

        '''

        score_all_game = 0
        number_of_distributions = self.__check_input()

        # hand distribution
        initial_hand = self.__deal_hand()

        while number_of_distributions > 0:

            if number_of_distributions == 0:
                break

            self.__play_hand(initial_hand)
            new_input = input("Would you like to replay the hand? ").lower()

            if new_input != "yes":
                initial_hand = self.__deal_hand()
                number_of_distributions -= 1
                score_all_game += self.__total_one_hand

            self.__total_one_hand = 0
        print(f'Total score over all hands: {score_all_game}')


if __name__ == '__main__':
    # starting process
    game = Erudite()
    game.play_game()


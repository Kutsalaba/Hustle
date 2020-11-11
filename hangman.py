# Problem Set 2, hangman.py
# Name: Kutsalaba Nazariy
# Students group: KM-04
# Collaborators: Alexey Garmash
# Time spent: 5 days

# Import modules
import random
import string
from string import ascii_letters


# declaring constants

# VOWELS_LETTERS - set of vowels
VOWELS_LETTERS = {'a', 'o', 'i', 'u', 'e'}

# UNKNOWN_LETTER - symbol underscore
UNKNOWN_LETTER = '_'

# HINT_SYMBOL - symbols for the game with hints
HINT_SYMBOL = '*'


class Hangman:
    '''
    This class describes the game "Hangman"

    Attributes
    ----------
    warning_left : int
        Number of warnings in game
    guesses_left : int
        Number of guesses in game
    __secret_word : str
        Word from word_list at random
    letters_guessed : set
        A set to store the letters to be entered

    Constants
    ---------
    WARNING_LEFT : int
        Number of warnings in game
    GUESSES_LEFT : int
        Number of guesses in game
    __word_list = None
        Get word_list from txt and create a variable word_list

    Methods
    -------
    __guess_word()
        This function checks whether the letters of the secret word are in the set of selected letters
    __get_guessed_word()
        This function adds items to the my_word list, if an item of my_word is in the letters_guessed,
        this item is added, if not, an underscore is added
    __get_available_letters()
        This function is added to the roster of Cyrillic elements that are not included in the letters_guessed
    __warning_letters(new_input)
        This function subtracts the number of attempts depending on the unpredictable letter (vowel or consonant)
    __subtraction_attempts()
        This function takes away the attempt if the number of warnings is 0, otherwise the warning is taken away
    __perfect_input(new_input)
        This function processes the input data and perform the corresponding operations
    __match_with_gaps(my_word, other_word)
        This function compares the length of my_word with other_words, and also compares
        letters with the same positions
    __show_possible_matches(my_word)
        This function displays all words that satisfy the conditions
        in the function match_with_gaps(my_word, other_word)
    __game_beginning_output()
        This function displays information about the start of the game
    __game_iterations_output(available_letters)
        This function displays information about the iterations of the game
    __game_results_output()
        This function displays information about the results of the game
    __warnings_numbers_output(my_word)
        This function determines the output to the screen.
    run_hangman()
        This is the main function. This function checks the user's input and calls up all other auxiliary functions

    Classmethod
    -----------
    __get_all_words()
        Depending on the size of the word list, this function may take a while to finish
    __choose_word()
        This function selects a random word, with wordlist
    '''

    WARNING_LEFT = 3
    GUESSES_LEFT = 6
    __word_list = None


    def __init__(self):
        '''
        The class attributes are initialized in this constructor
        '''

        self.warning_left = self.WARNING_LEFT
        self.guesses_left = self.GUESSES_LEFT
        self.__secret_word = self.__choose_word()
        self.letters_guessed = set()


    @classmethod
    def __get_all_words(cls):
        """
        Returns a list of valid words. Words are strings of lowercase letters.

        Depending on the size of the word list, this function may
        take a while to finish.
        """
        if not cls.__word_list:
            cls.__word_list = open("words.txt", 'r').readline().split()

        return cls.__word_list


    @classmethod
    def __choose_word(cls):
        """This function selects a random word, with wordlist.

        :param wordlist: Uses method choice() from the module "random";
        :return: word from wordlist at random.

        """

        return random.choice(cls.__get_all_words())


    def __guess_word(self):
        '''This function checks whether the letters of the secret word are in the set of selected letters.

        :return: boolean, True if all the letters of secret_word are in letters_guessed;
            False otherwise
        '''

        for char in self.__secret_word:
            if char not in self.letters_guessed:
                return False

        return True


    def __get_guessed_word(self):
        '''This function adds items to the my_word list, if an item of my_word is in the letters_guessed,
            this item is added, if not, an underline is added.

        :returns: string, comprised of letters, underlines (_), and spaces that represents
            which letters in secret_word have been guessed so far.
        '''

        my_word = []

        for char in self.__secret_word:
            if char in self.letters_guessed:
                my_word.append(char)
            else:
                my_word.append(UNKNOWN_LETTER)
        return ' '.join(my_word).strip()


    def __get_available_letters(self):
        '''This function is added to the roster of Cyrillic elements that are not included in the letters_guessed.

        :returns: string (of letters), comprised of letters that represents which letters have not
            yet been guessed.
        '''

        roster = []

        for char in string.ascii_lowercase:
            if char not in self.letters_guessed:
                roster.append(char)
        return ''.join(roster)


    def __warning_letters(self, new_input: str):
        '''This function subtracts the number of attempts depending on the unpredictable letter (vowel or consonant).

        :param: new_input: str, the letter entered by the user;
        :return: the number of guesses left, output text.
        '''

        if new_input in VOWELS_LETTERS:
            self.guesses_left -= 2
        else:
            self.guesses_left -= 1
        conclusion = "Oops! That letter is not in my word: "

        return conclusion


    def __subtraction_attempts(self):
        '''This function takes away the attempt if the number of warnings is 0, otherwise the warning is taken away

        :return: the number of warnings remaining, number of remaining attempts
        '''

        if self.warning_left < 0:
            self.guesses_left -= 1
        else:
            self.warning_left -= 1


    def __perfect_input(self, new_input: str):
        '''This function processes the input data and perform the corresponding operations.

        :param: new_input: str, the letter entered by the user;

        :return: string, comprised of letters, string (of letters), comprised of letters that represents which
            letters have not yet been guessed.The set of all entered letters.The number of warnings remaining.
            The number of remaining attempts. Output text.
        '''
        new_input = new_input.lower()

        if new_input in self.__secret_word:
            if new_input in self.letters_guessed:
                self.__subtraction_attempts()
                conclusion = self.__warnings_numbers_output("You've already guessed that letter")
            else:
                conclusion = "Good guess: "
        else:
            if new_input not in self.letters_guessed:
                conclusion = self.__warning_letters(new_input)
            else:
                self.__subtraction_attempts()
                conclusion = self.__warnings_numbers_output("You've already guessed that letter")

        self.letters_guessed.add(new_input)
        check_letters = self.__get_available_letters()
        my_word = self.__get_guessed_word()

        return my_word, check_letters, conclusion


    def __match_with_gaps(self, my_word: list, other_word: str):
        '''This function compares the length of my_word with other_words, and also compares
            letters with the same positions.

        :param: my_word : list, list with underscore characters, current guess of secret word
        :param: other_word : str, regular English word;
        :returns: boolean, True if all the guessed letters of the guessed word match the letters
            in the word from the list that have the same indexes;
            False otherwise.
        '''

        if len(my_word) != len(other_word):
            return False

        for char, new in zip(my_word, other_word):
            if not (char == UNKNOWN_LETTER or char == new) or (char == UNKNOWN_LETTER and new in my_word) or \
                    (new in self.letters_guessed and new != char):
                return False

        return True


    def __show_possible_matches(self, my_word: str):
        '''This function displays all words that satisfy the conditions
                 in the function match_with_gaps(my_word, other_word).If no matches are found,
                 it displays "No matches found". If a match is found, it displays string of all words t
                 hat match the guessed pattern secret word. Keep in mind that in hangman when a letter is guessed,
                 all the positions at which that letter occurs in the secret word are revealed.
                 Therefore, the hidden letter(_) cannot be one of the letters in the word
                 that has already been revealed.


        :param: my_word : str, string with underlines characters, current guess of secret word;
        '''

        lst = []
        my_word = my_word.replace(" ", "")

        for other_word in self.__get_all_words():
            if self.__match_with_gaps(my_word, other_word):
                lst.append(other_word)

        if not lst:
            print("No matches found")
        else:
            print(f"Possible word matches are: {' '.join(lst)}")


    def __game_beginning_output(self):
        '''This function displays the text of the beginning of the game.

        '''

        print('Welcome to the game Hangman!')
        print(f'I am thinking of a word that is {len(self.__secret_word)} letters long.')
        print('You have 3 warnings and 6 guesses left')


    def __game_iterations_output(self, available_letters: str):
        '''This function displays the text of the iterations of the game.

        :param: available_letters : str, letters that the user has not yet entered;
        '''

        print('-' * 16)
        print(f"You have {self.guesses_left} guesses left")
        print(f"Available Letters: {available_letters}")


    def __game_results_output(self):
        '''This function displays the text of the results of the game.

        '''

        if self.guesses_left > 0 and self.__guess_word():
            # Victory
            calculate_score = len(set(self.__secret_word)) * self.guesses_left
            print('_' * 12)
            print("Congratulations, you won!")
            print("Your total score for this game is:", calculate_score)

        elif self.guesses_left <= 0 or self.__guess_word():
            # Loose
            print('_' * 12)
            print(f"Sorry,you ran out of guesses. The word was {self.__secret_word}.")


    def __warnings_numbers_output(self, message: str):
        '''This function determines the output to the screen.

        :param: message : str, message text
        :param my_word: str, string with underlines characters, current guess of secret word;
        :return
        '''

        if self.warning_left >= 0:
            conclusion = f"Oops! {message}. You have {self.warning_left} warnings left:"
            if self.warning_left == 0:
                self.warning_left -= 1
        else:
            conclusion = f"Oops! {message}. You have no warnings left so you lose one guess:"
        return conclusion

    def run_hangman(self):
        '''This is the main function. This function checks the input of users,
            and therefore the user uses a methodical class.

        Parameters
        ----------
        secret_word : str
            contains unique letters in the word;
        my_word : str
            string with _ characters, current guess of secret word;
        guesses_left : int
            Var of guesses in game
        letters_guessed : set
            A set to store the letters to be entered
        warning_left : int
            Var of warnings in game
        '''

        # will contain the letters that have been guessed
        my_word = self.__get_guessed_word()

        # the text of the beginning of the game
        self.__game_beginning_output()

        # Main loop of game - each try is an iteration of that loop.
        while self.guesses_left > 0 and not self.__guess_word():

            self.__game_iterations_output(self.__get_available_letters())

            new_input = input("Please guess a letter: ")

            if new_input == HINT_SYMBOL:
                self.__show_possible_matches(my_word)


            elif not new_input in ascii_letters or len(new_input) != 1:
                self.__subtraction_attempts()
                print(self.__warnings_numbers_output('That is not a valid letter'),my_word)


            elif new_input in ascii_letters  and len(new_input) == 1:
                my_word, check_letters, conclusion = self.__perfect_input(new_input)
                print(conclusion, my_word)

        # output results
        self.__game_results_output()


if __name__ == "__main__":

    # starting process
    run_game = Hangman()
    run_game.run_hangman()


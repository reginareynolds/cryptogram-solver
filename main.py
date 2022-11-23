import sys
import collections
import os
import time
from functools import partial
from threading import Thread
import inspect

# from wordfreq import word_frequency

from idna import check_hyphen_ok
from patterns import get_word_pattern
from word_patterns import dictionary_patterns
from copy import deepcopy
from math import prod

import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget


# Find common potential decryption values
def common_keys(cypher_one, cypher_two):
    common_cypher = Cypher()
    for letter in cypher_one:
        if cypher_one[letter] == []:  # First cypher is empty
            # Copy over everything from second cypher
            for value in cypher_two[letter]:
                common_cypher.cypher[letter].append(value)
        elif cypher_two[letter] == []:  # Second cypher is empty
            # Copy over everything from first cypher
            for value in cypher_one[letter]:
                common_cypher.cypher[letter].append(value)
        else:
            for value in cypher_one[letter]:  # First cypher has a value
                # Second cypher has the same value
                if value in cypher_two[letter]:
                    common_cypher.cypher[letter].append(value)
    return common_cypher


class Cypher():
    def __init__(self):
        self.cypher = {
            "A": [],
            "B": [],
            "C": [],
            "D": [],
            "E": [],
            "F": [],
            "G": [],
            "H": [],
            "I": [],
            "J": [],
            "K": [],
            "L": [],
            "M": [],
            "N": [],
            "O": [],
            "P": [],
            "Q": [],
            "R": [],
            "S": [],
            "T": [],
            "U": [],
            "V": [],
            "W": [],
            "X": [],
            "Y": [],
            "Z": []}

    # Match possible decryption values to encrypted values
    def add_cypher_keys(self, length, encrypted_value, decrypted_source):
        for decrypted_value in decrypted_source:
            for letter in range(0, length):
                # Make sure decrypted value is not already accounted for
                if decrypted_value[letter] not in self.cypher[encrypted_value[letter]]:
                    self.cypher[encrypted_value[letter]].append(decrypted_value[letter])


class Alphabet():
    def __init__(self):
        # Statistical frequency of letters in the English language
        self.stat_frequency = [
            ["A", 0.084966],
            ["B", 0.020720],
            ["C", 0.045388],
            ["D", 0.033844],
            ["E", 0.111607],
            ["F", 0.018121],
            ["G", 0.024705],
            ["H", 0.030034],
            ["I", 0.075448],
            ["J", 0.001965],
            ["K", 0.011016],
            ["L", 0.054893],
            ["M", 0.030129],
            ["N", 0.066544],
            ["O", 0.071635],
            ["P", 0.031671],
            ["Q", 0.001962],
            ["R", 0.075809],
            ["S", 0.057351],
            ["T", 0.069509],
            ["U", 0.036308],
            ["V", 0.010074],
            ["W", 0.012899],
            ["X", 0.002902],
            ["Y", 0.017779],
            ["Z", 0.002722]]

        # Actual frequency of letters in text
        self.frequency = [
            ["A", None],
            ["B", None],
            ["C", None],
            ["D", None],
            ["E", None],
            ["F", None],
            ["G", None],
            ["H", None],
            ["I", None],
            ["J", None],
            ["K", None],
            ["L", None],
            ["M", None],
            ["N", None],
            ["O", None],
            ["P", None],
            ["Q", None],
            ["R", None],
            ["S", None],
            ["T", None],
            ["U", None],
            ["V", None],
            ["W", None],
            ["X", None],
            ["Y", None],
            ["Z", None]]


class Cryptogram():
    def __init__(self):
        self.file = None
        self.encrypted = None
        self.words = []  # Access using [x], where x is the word number index
        self.letter_count = collections.Counter()  # Running count of letter appearances in encrypted text
        self.letters = Alphabet()
        self.word_patterns = {}
        self.cyphers = []
        self.final_cypher = Cypher()
        self.decrypted = None
        self.dict_length = 0
        self.message_length = None
        self.wrong_indices = []  # List of all wrong indices, regardless of encrypted letter
        self.word_indices = []  # Track beginning and end indices of words        
        self.counter = 0  # Class variable version of previously decrypt function local count variable
        self.solved_tracker = []#(encrypted letter, True if solved, solution letter)]  # List the same length as the number of characters in the encrypted message. Each item in list is either True for a solved character or False for an unsolved letter

    def parse(self):
        # Parse encrypted file
        with open(self.file) as contents:
            self.encrypted = contents.readlines()

        # Strip whitespaces and standardize letters to same case
        for line in range(0, len(self.encrypted)):
            self.encrypted[line] = self.encrypted[line].strip().upper()

        # Join all encrypted lines
        self.encrypted = ''.join(line for line in self.encrypted)

        # Split into words
        words = self.encrypted.split(' ')

        # Check words for alphabetic characters
        alphabetic = ''
        for word in words:
            for letter in word:
                if letter.isalpha():
                    alphabetic = ''.join((alphabetic, letter))
            self.words.append(alphabetic)
            alphabetic = ''
        self.count(self.encrypted[line])

        # Count the total number of alphabetic characters
        total = 0
        for letter in self.letter_count:
            if letter.isalpha():
                total = total + self.letter_count[letter]

        # Record the frequency of alphabetic characters
        for letter in self.letter_count:
            if letter.isalpha():
                for pair in self.letters.frequency:
                    if pair[0] == letter:
                        pair[1] = self.letter_count[letter]/total

        # Determine word patterns for words in encrypted text
        for word in self.words:
            pattern = get_word_pattern(word)

            # Check for word pattern in pattern list
            if pattern in self.word_patterns:
                # Add encrypted English word to matching pattern key
                self.word_patterns[pattern].append(word)
            else:
                # Create new pattern key and initialize value list with encrypted English word
                self.word_patterns[pattern] = [word]

        # Compare word patterns in encrypted text to word patterns in English dictionary
        for pattern in self.word_patterns:
            # Map all potential decrypted values to corresponding encrypted values
            for encrypted_match in self.word_patterns[pattern]:
                cypher = Cypher()  # Create new cypher
                cypher.add_cypher_keys(len(pattern), encrypted_match, dictionary_patterns[pattern])
                self.cyphers.append(cypher)

        # Find common potential decrypted values in cyphers
        for count in range (0, len(self.cyphers)):
            self.final_cypher = common_keys(self.cyphers[count].cypher, self.final_cypher.cypher)

        # Set decrypted to encrypted BEFORE simplify_decryption to prevent undoing progress in update_dec_text
        self.decrypted = self.encrypted

        # Set list to correct length
        self.solved_tracker = [False] * len(self.encrypted)

        # Simplify common decrypted values
        self.simplify_decryption()

        # Decrypt as much of message as possible
        self.decrypt()
        # TODO: Determine how many times to rerun decrypt function

    # Update letter count for file
    def count(self, word):
        self.letter_count.update(word)

        # TODO: Account for letter frequency

    # Remove any correctly decrypted letters from potential decryptions of other encrypted letters
    def simplify_decryption(self):
        # Get dictionary length
        self.dict_length = sum([len(val) for val in self.final_cypher.cypher.values()])

        solved = []
        rerun = []

        self.solved_letters(solved)

        for letter in self.final_cypher.cypher:
            if len(self.final_cypher.cypher[letter]) > 1:
                for value in solved:
                    # Remove already decrypted values from potential decrypted values
                    if value[1] in self.final_cypher.cypher[letter]:
                        self.final_cypher.cypher[letter].remove(value[1])

        # If removing already decrypted values leaves more letters with only one potential decrypted value, call function again
        self.solved_letters(rerun)
        if len(rerun) > len(solved):
            self.simplify_decryption()
        else:
            self.cypher_update()

    # Find letters with only one potential decryption for encrypted value, which must be correct
    def solved_letters(self, list):
        for letter in self.final_cypher.cypher:
            if len(self.final_cypher.cypher[letter]) == 1:
                list.append([letter, self.final_cypher.cypher[letter][0]])

    # Update decryption cypher in Kivy screen
    def cypher_update(self, *kwargs):
        # Reset counter
        self.counter = 0

        cryptogram_page = app.frame.carousel.slides[1]
    
        # Get list of encrypted characters from self.final_cypher.cypher
        encrypted_chars = [entry for entry in self.final_cypher.cypher if len(self.final_cypher.cypher[entry])]
    
        # By checking if a letter is solved BEFORE updating the button, it allows the replacement of that character to happen
        # before sending any GUI update signals. This lets the button AND the decrypted text update simultaneously.
        for item in encrypted_chars:
            # Letter is solved
            if len(self.final_cypher.cypher[item])==1:
                # Replace encrypted character with solution
                self.update_dec_text(item, self.final_cypher.cypher[item])

                # Update decrypted text in Kivy window
                Clock.schedule_once(partial(cryptogram_page.update_text, self.decrypted))
            # Update buttons in decryption cypher
            Clock.schedule_once(partial(cryptogram_page.update_decryption_possibilities, encrypted_chars.index(item), self.final_cypher.cypher[item]))
            time.sleep(1)

    # Update decryption with each cypher update
    def update_dec_text(self, enc_char, solution):
        for letter in range(0, len(self.encrypted)):
            if self.encrypted[letter] == enc_char:
                self.decrypted = self.decrypted[:letter] + solution[0] + self.decrypted[letter+1:]
                self.counter = self.counter + 1
                self.solved_tracker[letter] = True

    def decrypt(self):
        print("encrypted")
        print(self.encrypted)
        print("decrypted")
        print(self.decrypted)

        # Already determined message length
        if self.message_length:
            pass
        # Determine alphabetic message length
        else:
            self.message_length = 0
            for letter in self.encrypted:
                if letter.isalpha():
                    self.message_length = self.message_length + 1

        # THREE CASES:
        # Case one: self.decrypted is identical to self.encrypted, meaning no letters were able to be replaced
        # Case two: self.decrypted is not identical to self.encrypted, but count is not equal to self.message_length, meaning not all letters were replaced
        # Case three: self. decrypted is not identical to self.encrypted, and count is equal to self.message_length, meaning all letters were replaced
        if self.counter != self.message_length:
            print("decrypt caller name: ", inspect.stack()[1][3])

            self.partially_solved()
            # self.find_key_words()
            self.remove_non_words()
            # self.user_choice()
            # self.rerun_check()

    def find_wrong_indices(self, incorrect_letters):
        self.wrong_indices = []
        self.word_indices = []

        for letter in range(0, len(self.solved_tracker)):
            if not self.solved_tracker[letter]:
                # Record index of uncertain letters
                if self.encrypted[letter].isalpha():
                    incorrect_letters.cypher[self.encrypted[letter]].append(letter)
                    self.wrong_indices.append(letter)
                # Record index of space between words
                if self.encrypted[letter].isspace():
                    self.word_indices.append(letter)

        # # TODO: Update decrypted text in Kivy window?
        # cryptogram_page = app.frame.carousel.slides[1]
        # Clock.schedule_once(partial(cryptogram_page.update_text, self.decrypted))
        # time.sleep(3)  # Keeps iterations of decryption visible instead of iterating instantaneously 


    # Takes partially solved words and searches the dictionary for matching patterns that specifically have the solved letters in those spots
    def partially_solved(self):
        # TODO: Remove a fully solved word from self.words. There is no need to continue iterating through words that are already solved.
        for word in self.words:
            index = 0
            correct_indices = []  # Holds solved letters and their position in the word
            for letter in word:
                # Solved letter
                # TODO: Incorporate solved_letters function
                if len(self.final_cypher.cypher[letter]) == 1:
                    correct_indices.append((index, self.final_cypher.cypher[letter]))
                index = index + 1

            # TODO: Determine how this is affected by punctuation, i.e. a contraction
            # Only partially solved word
            if len(correct_indices) != len(word):
                pattern = get_word_pattern(word)
                wrong_matches = []
                dictionary_matches = deepcopy(dictionary_patterns[pattern])

                # Find matching dictionary patterns
                for dictionary_match in dictionary_matches:
                    for correct_index in correct_indices:
                        # Note what words in the dictionary matched the word pattern but DID NOT have fully solved letters in the correct spot
                        if dictionary_match[correct_index[0]] != correct_index[1][0]:
                            wrong_matches.append(dictionary_match)
                            break

                # Remove any dictionary matches that don't have the solved letters in the correct spots
                for match in wrong_matches:
                    dictionary_matches.remove(match)

                print(self.final_cypher.cypher)
                cypher = Cypher()  # Create new cypher
                cypher.add_cypher_keys(len(word), word, dictionary_matches)
                self.final_cypher = common_keys(cypher.cypher, self.final_cypher.cypher)
                self.simplify_decryption()
# TODO: Potentially remove all keys that are not solved, then search for dictionary matches with solved letters in correct spots and add corresponding new possibilities to unsolved letters

    # Identify potential key words and prefixes/suffixes
    def find_key_words(self):
        # Key three letter words: and, are, but, for, had, her, his, its, nor, she, the, was, yet
        # Key two letter words: am, an, as, at, be, by, do, go, he, if, in, is, it, me, my, no, of, on, or, so, to, up, us, we
        # Key one letter words: I, a
        # Key prefixes: bi-, co-, de-, dis-, ex-, in-, mis-, non-, post-, pre-, pro-, re-, sub-, un-
        # Key suffixes: -able, -acy, -al, -ate, -dom, -ed, -en, -er, -ful, -fy, -ing, -ion, -ish, -ist, -ive, -ize, -less, -ment, -ness, -or, -ship, -ty, -y
        # Key double letters, in order of frequency in the English language: ll, ss, ee, oo, tt, ff, pp, rr

        for line in range(0, len(self.words)):
            for word in self.words[line]:
                # One letter words
                if len(word) == 1:
                    # Not solved yet
                    if len(self.final_cypher.cypher[word]) != 1:
                        # If only one of the one letter words is present, it is automatically correct
                        if 'A' in self.final_cypher.cypher[word] and 'I' not in self.final_cypher.cypher[word]:
                            self.final_cypher.cypher[word] = 'A'
                        elif 'I' in self.final_cypher.cypher[word] and 'A' not in self.final_cypher.cypher[word]:
                            self.final_cypher.cypher[word] = 'I'
                        # Otherwise, add both one letter words as possibilities as needed
                        else:
                            if 'A' not in self.final_cypher.cypher[word]:
                                self.final_cypher.append('A')
                            if 'I' not in self.final_cypher.cypher[word]:
                                self.final_cypher.append('I')
                # Two letter words
                if len(word) == 2:
                    first_letter = word[0]
                    second_letter = word[1]
                    # Either letter not solved yet
                    if len(self.final_cypher.cypher[first_letter]) == 1:
                        if len(self.final_cypher.cypher[second_letter]) != 1:
                            pass

    # Remove uncertain letter possibilities that result in non-words
    def remove_non_words(self):
        test_decrypt = list(deepcopy(self.decrypted))

        wrong = []  # In form of ((a, b), [c...]), where a and b are the start and end indices of the word and c... are the uncertain letters within the word
        self.wrong_words(wrong)

        # TODO: Account for words in which multiple letters are incorrect. For example, in "HxLLz", if x can be E or I and z can be O or Y, there are 4 possible words: HELLO, HILLO, HELLY, HILLY. May need to use total_possibility logic from before but limit it to words, not lines
        # Remove potential decrypted letters if fully decrypted words don't show up in the dictionary
        partial_words = []

        # Loop through words containing uncertain letters
        for word in wrong:
            indices = word[1]  # Incorrect indices within the word
            for index in indices:
                enc_letter = test_decrypt[index]  # Encrypted uncertain letter
                letter_possibilities = self.final_cypher.cypher[enc_letter]  # Decrypted letter possibilities for encrypted letter
                # Loop through decrypted letter possibilities
                for dec_letter in letter_possibilities:
                    copy = list(deepcopy(self.decrypted))
                    copy[word[1][0]] = dec_letter  # Replace encrypted letter with possible decrypted letter
                    partial_word = (''.join(copy[word[0][0]:word[0][1]]).strip(), enc_letter, dec_letter)
                    # TODO: Words need to be appended before removing them from final cypher, otherwise letters get skipped
                    if partial_word not in partial_words:
                        partial_words.append(partial_word)

        for poss_word in partial_words:
            word = poss_word[0]
            print(word)
            enc_letter = poss_word[1]
            dec_letter = poss_word[2]
            freq = word_frequency(word, 'en')
            print(freq)
            if freq == 0:
                if dec_letter in self.final_cypher.cypher[enc_letter]:
                    print("pre removal cypher")
                    print(self.final_cypher.cypher)
                    print("encrypted")
                    print(enc_letter)
                    self.final_cypher.cypher[enc_letter].remove(dec_letter)
                    print("post removal cypher")
                    print(self.final_cypher.cypher)

        self.rerun_check()

    # Find words containing uncertain letters
    def wrong_words(self, wrong_list):
        # Find start and end of word containing unsolved letter index
        for word_index in range(0, len(self.word_indices)):
            applicable = []
            
            # Group incorrect indices by containing word
            for index in self.wrong_indices:
                if index > self.word_indices[word_index] and index < self.word_indices[word_index + 1]:
                    applicable.append(index)
                    
            # Check if word contained incorrect indices
            if len(applicable):
                if applicable not in wrong_list:
                    wrong_list.append(((self.word_indices[word_index], self.word_indices[word_index + 1]), applicable))

    # Determine if decryption should be rerun
    def rerun_check(self):
        # Dictionary length changed, decryption should be rerun
        if sum([len(val) for val in self.final_cypher.cypher.values()]) < self.dict_length:
            self.decrypt()
        else:
            self.user_choice()

    # TODO: Finalize final cypher using user selected words. Show final decryption in place of decrypt button. Escape decryption loop
    # TODO: This should only be called if: 1. No more letters can be solved using other methods, and 2. The message is NOT fully solved.
    def user_choice(self):
        print("user_choice caller name: ", inspect.stack()[1][3])

        incorrect_letters = Cypher()  # Access using [x], where x is the encrypted, unsolved letter. Returns indices containing x
        self.find_wrong_indices(incorrect_letters)

        unsolved_letters = []  # List of unsolved letters and their possible decryptions
        for letter in self.final_cypher.cypher:
            if len(self.final_cypher.cypher[letter]) > 1:  # TODO: Should this be greater than 1 or != 1?
                unsolved_letters.append((letter, self.final_cypher.cypher[letter]))

        # Dynamically create possible decryptions using combinations of unsolved letters  
        total_possibilities = []
        unsolved_letter = unsolved_letters[0]
        for possibility in unsolved_letter[1]:
            possible = list(deepcopy(self.decrypted))
            for index in incorrect_letters.cypher[unsolved_letter[0]]:
                possible[index] = possibility
            total_possibilities.append(possible)
        
        x = 1
        while x < len(unsolved_letters):        
            unsolved_letter = unsolved_letters[x]
            possibilities = []
            for possibility in unsolved_letter[1]:
                for previous_letter in total_possibilities:
                    possible = list(deepcopy(previous_letter))
                    for index in incorrect_letters.cypher[unsolved_letter[0]]:
                        possible[index] = possibility
                    possibilities.append(possible)
            total_possibilities = possibilities
            x = x + 1

        wrong = []
        self.wrong_words(wrong)

        line_groups = []  # List of uncertain words in each possible full decryption
        # Create list of possible word translations
        for decryption in total_possibilities:
            partial_words = []
            for word in wrong:
                partial_word = ''.join(decryption[word[0][0]:word[0][1]]).strip()
                if partial_word not in partial_words:
                    partial_words.append(partial_word)
            line_groups.append(partial_words) 

        word_groups = []  # List of possible decryptions for each uncertain word
        self.word_groups(wrong, word_groups, line_groups)

# TODO: Remove any decryptions where uncertain letters are translated to the same letter
        # Check if there are any partially decrypted words
        if len(word_groups):
            cryptogram_page = app.frame.carousel.slides[1]

            Clock.schedule_once(partial(cryptogram_page.add_uncertain_letters, word_groups, total_possibilities))
            time.sleep(10)
            for group in word_groups:
                to_print = ''
                for word in group:
                    to_print = ''.join((to_print, word, " "))
                print(to_print)
            print("Here are the possible complete decryptions of the cryptogram.")
            print("Possible decryptions:")
            for decryption in total_possibilities:
                print(''.join(decryption))

            # Give user option to confirm based on word frequency
            word_count = 0
            compare = []
            self.word_groups(wrong, compare, line_groups)
            
            for group in word_groups:
                # User selection has removed possibilities from other uncertain words
                if compare[word_count] != group:
                    group = compare[word_count]  # Update uncertain word possibilities

                # Word is still uncertain
                if len(group) > 1:
                    for word in group:
                        print("The word frequency of ", word, " in the English language is ", word_frequency(word, 'en'))
                
                    # Prompt for user input
                    prompt = True
                    while prompt:
                        keep = input("Which word would you like to keep?")
                        keep = keep.strip().upper()

                        # User selected an invalid option
                        if keep not in group:
                            keep = input("That is not a valid selection. Please choose again.")
                        # User made valid selection
                        else:
                            decryption_count = 0
                            groups_remove = []
                            decryptions_remove = []
                            for line in line_groups:
                                if line[word_count] != keep:
                                    groups_remove.append(line)
                                    decryptions_remove.append(total_possibilities[decryption_count])
                                decryption_count = decryption_count + 1
                
                            for wrong in groups_remove:
                                line_groups.remove(wrong)

                            for wrong in decryptions_remove:
                                total_possibilities.remove(wrong)

                            compare = []
                            self.word_groups(wrong, compare, line_groups)

                            prompt = False

                word_count = word_count + 1

            print("Based on your selections, the final decryption is:")
            print(''.join(total_possibilities[0]))
            
            # Update final cypher based on user selections

            # self.rerun_check()  # TODO: Run this after a user makes a selection, otherwise it keeps rerunning self.decrypt, which reruns self.user_choice endlessly

    def word_groups(self, wrong, words, lines):
        for word in range(0, len(wrong)):
            holder = []
            for group in lines:
                if group[word] not in holder:
                    holder.append(group[word])
            words.append(holder)


class FileSelect(Popup):
    file_choice = ObjectProperty(None)
    btn_selection = ObjectProperty(None)

    def submit(self):
        with open(os.path.join(self.file_choice.path, self.file_choice.selection[0])) as file:
            # Set cryptogram screen encrypted_text to file contents
            cryptogram_page = app.frame.carousel.slides[1]
            cryptogram_page.path = file.name
            encryption = file.read()
            cryptogram_page.encrypted_text.text = encryption.strip().upper()

        # Close popup
        self.dismiss()

        # Change screens to encryption vs. decryption window
        change_page(1)

    def callback(self, instance):
        method = getattr(self, instance.text.lower())
        return method()

    def select(self, file_path, file_picked):
        # Enable submission button as necessary
        if file_picked:
            self.btn_selection.children[0].disabled = False
        else:
            self.btn_selection.children[0].disabled = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Set default directory to current directory
        self.file_choice.path = os.path.abspath(os.getcwd())

        # Bind cancel and select buttons
        for child in self.btn_selection.children:
            child.bind(on_press=self.callback)

class Possibility(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

# Uncertain letters popup
class UncertainLetters(Popup):
    btn_selection = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
def change_page(new_page, *dt):
    """Change slide displayed in carousel"""
    app.frame.carousel.load_slide(app.frame.carousel.slides[new_page])

class ScreenFrame(Widget):
    carousel = ObjectProperty(None)


class CryptogramScreen(Widget):
    encrypted_text = ObjectProperty(None)
    decrypted_text = ObjectProperty(None)
    start_decryption = ObjectProperty(None)
    decryption_cypher = ObjectProperty(None)
    default_encrypted = ObjectProperty(None)
    default_decrypted = ObjectProperty(None)

    def add_uncertain_letters(self, groups, possibilities, *kwargs):
        print("caller name: ", inspect.stack()[1][3])
        start = time.time()
        # Add uncertain words, one group per row
        for group in groups:
            row = GridLayout(cols=len(group))  # Row to add to UncertainLetters popup

            for word in group:
                btn = Button(text=word)
                # TODO: Bind button clicks to user selection (using name property?)
                row.add_widget(btn)
            self.popup.btn_selection.add_widget(row)

        # Add informational text
        line_one = Possibility()
        line_two = Possibility()

        line_one.text = "Here are the possible complete decryptions of the cryptogram."
        line_two.text = "Possible decryptions:"

        # Add possible full decryptions
        for possible in possibilities:
            poss = Possibility()
            poss.text=''.join(possible)
            self.popup.btn_selection.add_widget(poss)

        # Open popup now that new information is added
        self.popup.open()

        end=time.time()
        print(end-start)

    def update_text(self, *kwargs):
        self.decrypted_text.text = kwargs[0]

    # Add buttons to decryption cypher
    def add_cypher_row(self, enc_char, dec_char, *kwargs):
        self.decryption_cypher.add_widget(enc_char)
        self.decryption_cypher.add_widget(dec_char)

    # TODO: Call this whenever the final cypher is updated
    # Update button text in decryption cypher
    def update_decryption_possibilities(self, ind, possibilities, *kwargs):
        # Get buttons in row 
        enc_btn = self.buttons[ind*2] 
        dec_btn = self.buttons[(ind*2)+1]

        # Only one possible solution for encrypted letter
        if len(possibilities) == 1:
            dec_btn.text = possibilities[0]

            # Change solved button colors to green
            if ind % 2:
                enc_btn.background_color=(0, 0.75, 0, 1)
                dec_btn.background_color=(0, 0.75, 0, 1)
            else:
                # Change solved button colors to green
                enc_btn.background_color=(0, 1, 0, 1)
                dec_btn.background_color=(0, 1, 0, 1)
        # Not yet solved
        else:
            poss_solutions = ", ".join((possibilities))
            dec_btn.text = poss_solutions

    def create_cypher(self, btns, dec_cypher):
        inc = 0
        for enc_letter in dec_cypher:
            # Change default button text to an encrypted letter
            if inc == 0:
                self.default_encrypted.text = enc_letter
            # Customize and add buttons
            else:
                enc_btn = btns[inc*2]  # Adjust inc to keep it within bounds of the btns list length
                dec_btn = btns[(inc*2)+1]

                enc_btn.text = enc_letter
                dec_btn.text = "?"

                enc_btn.size_hint_min_y=(enc_btn.font_size+30)
                dec_btn.size_hint_min_y=(dec_btn.font_size+30)

                enc_btn.size_hint_x = 0.4

                # Alternate button colors from default every other line
                if inc % 2:
                    enc_btn.background_color=(0.75, 0.75, 0.75, 1)
                    dec_btn.background_color=(0.75, 0.75, 0.75, 1)

                # Add buttons to decryption cypher
                Clock.schedule_once(partial(self.add_cypher_row, enc_btn, dec_btn))
                time.sleep(0.5)

            # Increment count
            inc = inc + 1

        # Wait until all entries are added to decryption cypher to begin processing
        Thread(target=self.encoded.parse).start()

    def callback(self, instance):
        # Disable decrypt button
        self.start_decryption.disabled = True

        # Set initial decrypted text to encrypted text
        self.update_text(self.encrypted_text.text)

        # Set path to cryptogram file
        self.encoded.file = self.path

        # Initialize decryption cypher
        dec_cypher = sorted(set(self.encrypted_text.text))

        # Remove empty space from decryption cypher
        if dec_cypher[0] == ' ':
            dec_cypher.remove(dec_cypher[0])

        # Initialize all buttons necessary in main thread
        i = 0

        while i < len(dec_cypher)-1:  # len(dec_cypher)-1 to account for the two existing default buttons 
            self.buttons.append(Button())
            self.buttons.append(Button())
            i= i+1

        # Add button widgets to decryption cypher in new thread
        Thread(target=partial(self.create_cypher, self.buttons, dec_cypher)).start()

        # N.B. The parsing needs to happen on a secondary thread, otherwise
        # the parsing will happen on the main thread and will block the
        # encrypted text/decryption cypher from updating until AFTER the processing completes. 
        # The Thread target has to be a function/method, NOT a function/method CALL.
        # That means that the target needs to look like this:
        # Thread(target=functionName).start()
        # NOT like this:
        # Thread(target=functionName()).start()
        # That means that we can't pass any arguments because we do that via
        # function/method call. We can work around this by setting the target
        # like this:
        # Thread(target=partial(functionName, passed_variables).start()



        # TODO: Show decrypted text in new window
        # TODO: Only run decryption once to prevent additional parsing unless file path changes


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Final variables
        self.path = None
        self.encoded = Cryptogram()

        self.buttons = []

        # Initialize popup
        self.popup = UncertainLetters()

        # Add default buttons to self.buttons list
        self.buttons.append(self.default_encrypted)
        self.buttons.append(self.default_decrypted)

        self.start_decryption.bind(on_press=self.callback)

class MenuScreen(Widget):
    options = ObjectProperty(None)

    def callback(self, instance):
        popup = FileSelect()
        popup.open()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for child in self.options.children:
            child.bind(on_press=self.callback)   

     
class CryptogramSolverApp(App):
    def build(self):
        self.frame = ScreenFrame()

        # Initialize different screens
        menu_screen = MenuScreen()
        cryptogram_screen = CryptogramScreen()

        # Add screens to carousel
        self.frame.carousel.add_widget(menu_screen)
        self.frame.carousel.add_widget(cryptogram_screen)

        return self.frame    

# TODO: Show decryption progress bar. Show cypher and update as letters are solved?
if __name__ == '__main__':
    app = CryptogramSolverApp()
    app.run()

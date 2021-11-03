import sys
import collections
from wordfreq import word_frequency
from tkinter import Button, Frame, Tk, messagebox
from tkinter.filedialog import askopenfilename
from patterns import get_word_pattern
from word_patterns import dictionary_patterns
from copy import deepcopy
from math import prod


class Menu(Tk):
    def __init__(self, title, buttons):
        # Final variables
        self.path = None
        self.encoded = Cryptogram()

        # CREATE MENU ITEMS

        # CONFIGURE MENU
        Tk.__init__(self)
        # Bind keys to functions
        self.bind('<Return>', self.onclick)

        # Set window title
        self.title(title)
        self.frame = Frame(self)

        # Create buttons
        self.buttons = buttons  # Button click history
        self.rows = []  # Array to store button locations
        index = 2
        for button in self.buttons:
            self.button = Button(
                self, text=button[1], command=lambda response=button[0]: self.onclick(response))
            self.button.grid(row=index, column=0, padx=50,
                             pady=5, sticky="W E")
            self.rows.append(self.button)
            index = index + 1

            # Disable buttons until file is selected
            if index-3 == 0:
                pass
            else:
                self.button['state'] = 'disabled'

        # Return to menu or close program
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    # Enable submission on selection of file
    def enable(self):
        # File has been selected
        if self.path != None:
            for button in self.rows:
                button['state'] = 'normal'
        else:  # File not selected yet
            self.button['state'] = 'disabled'

    def onclick(self, response):
        # User selected button with mouse
        if type(response) == int:
            pass
        # User selected button with keyboard
        else:
            index = 1
            for location in self.rows:
                if self.focus_get() == location:
                    response = index
                else:
                    pass
                index = index + 1

        choice = 'func_' + str(response)
        method = getattr(self, choice)
        return method()

    # Enable menu option opening and closing
    @staticmethod
    def hide(frame):
        frame.withdraw()

    @staticmethod
    def show(frame):
        frame.update()
        frame.deiconify()

    # File prompt
    def func_1(self):
        # Hide menu
        self.hide(self)

        # Create prompt for file
        self.path = file_prompt()

        # Check if user closed out of file prompt
        if self.path == '':
            self.path = None  # Reset path
            self.rows[0].config(text=self.buttons[0][1])  # Reset button text
        else:
            # Change button text to selected path
            self.rows[0].config(text=self.path)

        self.enable()
        self.show(self)

    # Begin decryption
    def func_2(self):
        # Hide menu
        self.hide(self)

        # Set path to cryptogram file and open
        self.encoded.file = self.path
        self.encoded.parse()
        self.enable()
        self.show(self)
        # TODO: Show decrypted text in new window
        # TODO: Only run decryption once to prevent additional parsing unless file path changes

    def on_closing(self):
        ans = messagebox.askokcancel(
            'Verify exit', "Do you really want to quit the program?")
        if ans:
            self.quit()
            sys.exit(3)
        else:
            pass


def file_prompt():
    Tk().withdraw()
    filename = askopenfilename(filetypes=[("Text files", "*.txt")])
    return filename


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
        self.words = []  # Access using [x][y], where x is the line number index and y is the word number index in that line
        self.letter_count = collections.Counter()  # Running count of letter appearances in encrypted text
        self.letters = Alphabet()
        self.word_patterns = {}
        self.cyphers = []
        self.final_cypher = Cypher()
        self.decrypted = None
        self.dict_length = 0

    def parse(self):
        # Parse encrypted file
        with open(self.file) as contents:
            self.encrypted = contents.readlines()

        # Strip whitespaces and standardize letters to same case
        for line in range(0, len(self.encrypted)):
            self.encrypted[line] = self.encrypted[line].strip().upper()

            # Split into words
            words = self.encrypted[line].split(' ')

            # Check words for alphabetic characters
            alphabetic = ''
            alphabetic_line = []
            for word in words:
                for letter in word:
                    if letter.isalpha():
                        alphabetic = ''.join((alphabetic, letter))
                alphabetic_line.append(alphabetic)
                alphabetic = ''
            self.words.append(alphabetic_line)
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
        for line in self.words:
            for word in line:
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

    # Find letters with only one potential decryption for encrypted value, which must be correct
    def solved_letters(self, list):
        for letter in self.final_cypher.cypher:
            if len(self.final_cypher.cypher[letter]) == 1:
                list.append([letter, self.final_cypher.cypher[letter][0]])

    def decrypt(self):
        solved = []
        self.solved_letters(solved)
        self.decrypted = ''

        count = 0  # Track how many letters were replaced
        for line in range(0, len(self.encrypted)):
            for letter in range(0, len(self.encrypted[line])):
                flag = True
                for value in solved:
                    # If encrypted letter matches a solved letter, replace it with solution
                    if self.encrypted[line][letter] == value[0]:
                        self.decrypted = ''.join((self.decrypted, value[1]))
                        flag = False
                        count = count + 1
                        break
                if flag:
                    self.decrypted = ''.join(
                        (self.decrypted, self.encrypted[line][letter]))

        print("encrypted")
        print(self.encrypted)
        print("decrypted")
        print(self.decrypted)

        # THREE CASES:
        # Case one: self.decrypted is identical to self.encrypted[0], meaning no letters were able to be replaced
        # Case two: self.decrypted is not identical to self.encrypted[0], but count is not equal to len(self.encrypted[0]), meaning not all letters were replaced
        # Case three: self. decrypted is not identical to self.encrypted[0], and count is equal to len(self.encrypted[0]), meaning all letters were replaced
        if count != len(self.encrypted[0]):
            self.partially_solved()
            # self.find_key_words()
            self.rerun_check()

    # Takes partially solved words and searches the dictionary for matching patterns that specifically have the solved letters in those spots
    def partially_solved(self):
        for line in range(0, len(self.words)):
            for word in self.words[line]:
                index = 0
                correct_indices = []  # Holds solved letters and their position in the word
                for letter in word:
                    # Solved letter
                    # TODO: Incorporate solved_letters function
                    if len(self.final_cypher.cypher[letter]) == 1:
                        correct_indices.append((index, self.final_cypher.cypher[letter]))
                    index = index + 1

                # Only partially solved word
                if len(correct_indices) != len(word):
                    pattern = get_word_pattern(word)
                    wrong_matches = []
                    dictionary_matches = deepcopy(dictionary_patterns[pattern])

                    # Find matching dictionary patterns
                    for dictionary_match in dictionary_matches:
                        for correct_index in correct_indices:
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
    
    # Determine if decryption should be rerun
    def rerun_check(self):
        # Dictionary length changed, decryption should be rerun
        if sum([len(val) for val in self.final_cypher.cypher.values()]) < self.dict_length:
            self.decrypt()
        else:
            self.letter_probability()

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
    
    def letter_probability(self):
        solved = []
        self.solved_letters(solved)
        decrypted = ''
        possible_decryptions = []

        incorrect_letters = Cypher()  # Access using [x], where x is the encrypted, unsolved letter. Returns indices containing x

        unsolved_letters = []  # List of unsolved letters and their possible decryptions
        for letter in self.final_cypher.cypher:
            if len(self.final_cypher.cypher[letter]) > 1:  # TODO: Should this be greater than 1 or != 1?
                unsolved_letters.append((letter, self.final_cypher.cypher[letter]))

        # TODO: Potentially incorporate into decryption function here
        wrong_index = 0
        word_indices = []  # Track beginning and end indices of words
        partial_words = []
        for line in range(0, len(self.encrypted)):
            for letter in range(0, len(self.encrypted[line])):
                flag = True
                for value in solved:
                    # If encrypted letter matches a solved letter, replace it with solution
                    if self.encrypted[line][letter] == value[0]:
                        decrypted = ''.join((decrypted, value[1]))
                        flag = False
                        break
                if flag:
                    decrypted = ''.join((decrypted, self.encrypted[line][letter]))
                    # Record index of uncertain letters
                    if self.encrypted[line][letter].isalpha():
                        incorrect_letters.cypher[self.encrypted[line][letter]].append(wrong_index)
                    # Record index of space between words
                    if self.encrypted[line][letter].isspace():
                        word_indices.append(wrong_index)
                wrong_index = wrong_index + 1    

        # Determine the number of possible decryptions using combinations of unsolved letters
        possibility_count = prod([len(val[1]) for val in unsolved_letters])
        for count in range(0, possibility_count):
            possible = list(deepcopy(decrypted))
            possible_decryptions.append(possible)

        # Determine how many decryptions each potential letter solution should be in
        for unsolved_letter in unsolved_letters:
            count = 0
            interval = int(len(possible_decryptions)/len(unsolved_letter[1]))
            for x in range(0, len(possible_decryptions), interval):
                for decryption in possible_decryptions[x:x+interval]:
                    for index in incorrect_letters.cypher[unsolved_letter[0]]:
                        decryption[index] = unsolved_letter[1][count]
                count = count + 1

        # TODO: Account for multiple uncertain words
        # Create list of possible word translations
        for decryption in possible_decryptions:
            # Find start and end of word containing unsolved letter index
            for word_index in range(0, len(word_indices)):
                                        # TODO: If there are only two words, the below line breaks. Account for this.
                if word_indices[word_index] < index and word_indices[word_index + 1] > index:
                    partial_word = ''.join(decryption[word_indices[word_index]:word_indices[word_index + 1]]).strip()
                    if partial_word not in partial_words:
                        partial_words.append(partial_word)      

        # Check if there are any partial words
        if len(partial_words):
            print("Some encrypted letters could not be decrypted with certainty. The following words are possible decryptions.")
            for word in partial_words:
                print(word)
            print("Here are the possible complete decryptions of the cryptogram.")
            print("Possible decryptions:")
            for decryption in possible_decryptions:
                print(''.join(decryption))
            for word in partial_words:
                print("The word frequency of ", word, " in the English language is ", word_frequency(word, 'en'))
            print("Which word would you like to keep?")
#TODO: Give user option to confirm based on word frequency

if __name__ == '__main__':
    menu = Menu(
        "Crypto-Solver!", ((1, "Choose an encrypted file."), (2, "Decrypt cryptogram.")))
    menu.mainloop()
    menu.destroy()

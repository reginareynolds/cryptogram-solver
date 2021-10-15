import sys
import collections
from tkinter import Button, Frame, Tk, messagebox
from tkinter.filedialog import askopenfilename
from patterns import get_word_pattern
from word_patterns import dictionary_patterns


class Menu(Tk):
    def __init__(self, title, buttons):
        # Final variables
        self.path = None
        self.encoded = Cryptogram()
        self.decoded = None

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
            self.rows[0].config(text=self.path)  # Change button text to selected path

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
            for value in cypher_two[letter]:  # Copy over everything from second cypher
                common_cypher.cypher[letter].append(value)
        elif cypher_two[letter] == []:  # Second cypher is empty
            for value in cypher_one[letter]:  # Copy over everything from first cypher
                common_cypher.cypher[letter].append(value)
        else:
            for value in cypher_one[letter]:  # First cypher has a value
                if value in cypher_two[letter]:  # Second cypher has the same value
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
    def add_cypher_keys(self, encrypted_value, decrypted_value):
        # Make sure decrypted value is not already accounted for
        if decrypted_value not in self.cypher[encrypted_value]:
            self.cypher[encrypted_value].append(decrypted_value)


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

    # Remove any correctly decrypted letters from potential decryptions of other encrypted letters
    def simplify_decryption(self):
        solved = []

        for letter in self.final_cypher.cypher:
            if len(self.final_cypher.cypher[letter]) == 1:  # Only one potential decryption for encrypted value, must be correct
                solved.append(self.final_cypher.cypher[letter][0])
        
        for letter in self.final_cypher.cypher:
            if len(self.final_cypher.cypher[letter]) > 1:
                for value in solved:
                    if value in self.final_cypher.cypher[letter]:  # Remove already decrypted values from potential decrypted values
                        self.final_cypher.cypher[letter].remove(value)
                        if len(self.final_cypher.cypher[letter]) == 1:  # If removing already decrypted values leaves only one potential decrypted value, call function again
                            self.simplify_decryption()

    def decrypt(self):
        solved = []
        for letter in self.final_cypher.cypher:
            if len(self.final_cypher.cypher[letter]) == 1:
                solved.append([letter, self.final_cypher.cypher[letter][0]])
        self.decrypted = ''

        for line in range(0, len(self.encrypted)):
            for letter in range(0, len(self.encrypted[line])):
                flag = True
                for value in solved:
                    if self.encrypted[line][letter] == value[0]:
                        self.decrypted = ''.join((self.decrypted,value[1]))
                        flag = False
                        break
                if flag:
                    self.decrypted = ''.join((self.decrypted, self.encrypted[line][letter]))

        print("encrypted")
        print(self.encrypted)
        print("decrypted")
        print(self.decrypted)

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
                    self.word_patterns[pattern].append(word)  # Add encrypted English word to matching pattern key
                else:
                    self.word_patterns[pattern] = [word]  # Create new pattern key and initialize value list with encrypted English word

        # Compare word patterns in encrypted text to word patterns in English dictionary
        for pattern in self.word_patterns:
            # Map all potential decrypted values to corresponding encrypted values
            for encrypted_match in self.word_patterns[pattern]:
                cypher = Cypher()  # Create new cypher
                for dictionary_match in dictionary_patterns[pattern]:
                    for letter in range(0, len(pattern)):
                        cypher.add_cypher_keys(encrypted_match[letter], dictionary_match[letter])
                self.cyphers.append(cypher)

        # Find common potential decrypted values in cyphers
        self.final_cypher = common_keys(self.cyphers[0].cypher, self.cyphers[1].cypher)
        for count in range(2, len(self.cyphers)):
            self.final_cypher = common_keys(self.cyphers[count].cypher, self.final_cypher.cypher)

        # Simplify common decrypted values
        self.simplify_decryption()

        # Decrypt as much of message as possible
        self.decrypt()

    # Update letter count for file
    def count(self, word):
        self.letter_count.update(word)

        # TODO: Account for letter frequency

    # Identify potential key words and prefixes/suffixes
    def find_key_words(self):
        # Key three letter words: and, are, but, for, had, her, his, its, nor, she, the, was, yet
        # Key two letter words: am, an, as, at, be, by, do, go, he, if, in, is, it, me, my, no, of, on, or, so, to, up, us, we
        # Key one letter words: I, a
        # Key prefixes: bi-, co-, de-, dis-, ex-, in-, mis-, non-, post-, pre-, pro-, re-, sub-, un-
        # Key suffixes: -able, -acy, -al, -ate, -dom, -ed, -en, -er, -ful, -fy, -ing, -ion, -ish, -ist, -ive, -ize, -less, -ment, -ness, -or, -ship, -ty, -y
        # Key double letters, in order of frequency in the English language: ll, ss, ee, oo, tt, ff, pp, rr  
        pass


if __name__ == '__main__':
    menu = Menu(
        "Crypto-Solver!", ((1, "Choose an encrypted file."), (2, "Decrypt cryptogram.")))
    menu.mainloop()
    menu.destroy()

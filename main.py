import sys
import collections
from tkinter import Button, Frame, Tk, messagebox
from tkinter.filedialog import askopenfilename


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
        self.encoded.decrypt()
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


class Alphabet():
    def __init__(self):
        self.cypher = [
            ["A", ""],
            ["B", ""],
            ["C", ""],
            ["D", ""],
            ["E", ""],
            ["F", ""],
            ["G", ""],
            ["H", ""],
            ["I", ""],
            ["J", ""],
            ["K", ""],
            ["L", ""],
            ["M", ""],
            ["N", ""],
            ["O", ""],
            ["P", ""],
            ["Q", ""],
            ["R", ""],
            ["S", ""],
            ["T", ""],
            ["U", ""],
            ["V", ""],
            ["W", ""],
            ["X", ""],
            ["Y", ""],
            ["Z", ""]]

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

    def decrypt(self):
        # Parse encrypted file
        with open(self.file) as contents:
            self.encrypted = contents.readlines()

        # Strip whitespaces and standardize letters to same case
        for line in range(0, len(self.encrypted)):
            self.encrypted[line] = self.encrypted[line].strip().upper()
            self.words.append(self.encrypted[line].split(' '))
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
                pattern = word_pattern(word)

                # Check for word pattern in pattern list
                if pattern in self.word_patterns:
                    self.word_patterns[pattern].append(word)  # Add English word to matching pattern key
                else:
                    self.word_patterns[pattern] = [word]  # Create new pattern key and initialize value list with English word

    # Update letter count for file
    def count(self, word):
        self.letter_count.update(word)

        # TODO: Account for letter frequency


if __name__ == '__main__':
    encrypted = Menu(
        "Crypto-Solver!", ((1, "Choose an encrypted file."), (2, "Decrypt cryptogram.")))
    encrypted.mainloop()
    encrypted.destroy()

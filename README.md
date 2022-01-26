# cryptogram-solver
A program to intelligently decrypt cryptogram puzzles.

## What is a cryptogram?
A cryptogram is a type of word puzzle. In it, a piece of text is encrypted with a substitution cypher. This works by replacing every letter with a different letter. To solve the puzzle, the user needs to undo the substitutions to return the text to its original state. Below is an example.

#### Original text:
THE FIRST METHOD FOR ESTIMATING THE INTELLIGENCE OF A RULER IS TO LOOK AT THE MEN HE HAS AROUND HIM.
#### Encrypted text:
YPX EBULY WXYPHC EHU XLYBWJYBDS YPX BDYXKKBSXDNX HE J UOKXU BL YH KHHZ JY YPX WXD PX PJL JUHODC PBW.
### Encryption substitution cypher:
|**Original letter**|**Encrypted letter**|
|:---:|:---:|
| A | J |
| B |  |
| C | N |
| D | C |
| E | X |
| F | E |
| G | S |
| H | P |
| I | B |
| J |  |
| K | Z |
| L | K |
| M | W |
| N | D |
| O | H |
| P |  |
| Q |  |
| R | U |
| S | L |
| T | Y |
| U | O |
| V |  |
| W |  |
| X |  |
| Y |  |
| Z |  |

To decrypt the cryptogram, the user would need to construct the inverted substitution cypher.

### Decryption substitution cypher

|**Encrypted letter**|**Original letter**|
|:---:|:---:|
| A |  |
| B | I |
| C | D |
| D | N |
| E | F |
| F |  |
| G |  |
| H | O |
| I |  |
| J | A |
| K | L |
| L | S |
| M |  |
| N | C |
| O | U |
| P | H |
| Q |  |
| R |  |
| S | G |
| T |  |
| U | R |
| V |  |
| W | M |
| X | E |
| Y | T |
| Z | K |

## How this program works
This program works by taking an encrypted input, identifying the [relative patterns](#word-patterns) of the encrypted words, and comparing those relative patterns to a [list of known matches](word_patterns.py). The known matches are then [cross-referenced with each other](#comparing-word-patterns), and matches that contradict one another are removed from the pool of potential candidates. This process is repeated until no more matches can be removed.

If the cryptogram is still not solved at that point, the user is presented with the different possible decryptions and the likelihood of their correctness based on the frequency of each potential word in the English language. The user can then make a final decision on the correct decryption.

## Why this program works
Cryptograms are encrypted using substitution cyphers. This means that any given letter is located in the same location whether it is encrypted or decrypted. In other words, the encrypted text units retain the same sequence as the decrypted text units. This varies from a transposition cypher, where the encryption process retains the value of the text unit but changes the location.

Because the text sequence is maintained, the relative pattern of the letters in the text stays the same. 

Consider the [example sentence](#original-text) and its [encryption](#encrypted-text).

This example consists of 80 total alphabetic characters and 20 total words. Of those 80 alphabetic characters, there are 17 unique characters. Of the 20 total words, there are 18 unique words. These numbers are true for both the original and the encrypted text.

### Word patterns
For simplicity's sake, each encrypted and decrypted word can be thought of as a pattern. For a given word, each letter can be replaced with a corresponding numeral. That numeral replaces every instance of the corresponding letter within the word. 

For example, here are some words and their word patterns.

|**Word**|**Word pattern**|
|:---:|:---:|
| CAT | 012 |
| KITTEN | 012234 |
| RUNNING | 0122324 |
| DICTIONARY | 0123145678 |
| ESTABLISHMENT | 0123456178092 |

 The table below shows the word patterns of our example text.

|**Original word**|**Encrypted word**|**Word pattern**|
|:---:|:---:|:---:|
| THE | YPX | 012 |
| FIRST | EBULY | 01234 |  
| METHOD | WXYPHC | 012345 |  
| FOR | EHU | 012 |  
| ESTIMATING | XLYBWJYBDS | 0123452367 |  
| THE | YPX | 012 |  
| INTELLIGENCE | BDYXKKBSXDNX | 012344053163 |  
| OF | HE | 01 |  
| A | J | 0 |
| RULER | UOKXU | 01230 |
| IS | BL | 01 |
| TO | YH | 01 |
| LOOK | KHHZ | 0112 |
| AT | JY | 01 |
| THE | YPX | 012 |
| MEN | WXD | 012 |
| HE | PX | 01 |
| HAS | PJL | 012 |
| AROUND | JUHODC | 012345 |
| HIM | PBW | 012 |

Notice that the word pattern remains identical for both the original text and the encrypted text. As explained above, the substitution cypher maintains the relative pattern of the letters in the text, which allows the word pattern to stay the same.

### Comparing word patterns
In order to decrypt the message, this program relies on identifying potential words corresponding to each word pattern, then comparing a given encrypted word's potential letter solutions to other encrypted words' potential letter solutions. The potential letter solution of an encrypted letter must be the same across encrypted words.

This means that the more times an encrypted letter appears in the text, the more comparisons that can be made, and the greater the chance is to determine that encrypted letter's decryption. Longer encrypted texts are therefore easier to decrypt.

The ```parse(self)``` function of the ```Cryptogram``` class in [main.py](main.py) interprets the encrypted text and creates a dictionary of the different word patterns found within it, as shown in the lines below.

```
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
```

The resultant dictionary looks like this:
```
{'012': ['YPX', 'EHU', 'YPX', 'YPX', 'WXD', 'PJL', 'PBW'], '01234': ['EBULY'], '012345': ['WXYPHC', 'JUHODC'], '0123452367': ['XLYBWJYBDS'], '012344053163': ['BDYXKKBSXDNX'], '01': ['HE', 'BL', 'YH', 'JY', 'PX'], '0': ['J'], '01230': ['UOKXU'], '0112': ['KHHZ']}
```

The next step is to compare the word patterns in the encrypted text to matching word patterns in the English language, then record potential letter solutions for each encrypted letter in a Python dictionary. This is done using the ```Cypher``` class of [main.py](main.py). These ```Cyphers``` are then compared against each other using the ```common_keys()``` function, which finds the potential letter solutions that the cyphers have in common.

```
for pattern in self.word_patterns:
    # Map all potential decrypted values to corresponding encrypted values
    for encrypted_match in self.word_patterns[pattern]:
        cypher = Cypher()  # Create new cypher
        cypher.add_cypher_keys(len(pattern), encrypted_match, dictionary_patterns[pattern])
        self.cyphers.append(cypher)

# Find common potential decrypted values in cyphers
for count in range (0, len(self.cyphers)):
    self.final_cypher = common_keys(self.cyphers[count].cypher, self.final_cypher.cypher)

```
The resultant ```Cypher.cypher``` looks like this:
```
{'A':[], 'B':['I'], 'C':['T', 'S', 'E', 'D', 'G', 'Y', 'N', 'H', 'B', 'O', 'I', 'R', 'W', 'C', 'M', 'L', 'K', 'P', 'F', 'X', 'A', 'Z', 'U', 'V'], 'D':['N'], 'E':['B', 'D', 'G', 'H', 'I', 'M', 'N', 'S', 'T', 'W', 'Y', 'A', 'E', 'O', 'L', 'R', 'F', 'U', 'K', 'P', 'Z'], 'F':[], 'G':[], 'H':['B', 'D', 'L', 'M', 'N', 'E', 'O', 'G', 'R', 'A', 'F'], 'I':[], 'J':['A'], 'K':['L'], 'L':['H', 'I', 'S', 'A', 'O', 'U'], 'M':[], 'N':['C'], 'O':['L', 'M', 'N', 'O', 'R', 'U', 'Y', 'A', 'I', 'C', 'V', 'X', 'E', 'H', 'K', 'P', 'T', 'W'], 'P':['A', 'B', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'O', 'P', 'R', 'S', 'T', 'U', 'W', 'Y'], 'Q':[], 'R':[], 'S':['G'], 'T':[], 'U':['A', 'B', 'C', 'D', 'E', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'O', 'P', 'R', 'S', 'T', 'W', 'X'], 'V':[], 'W':['W', 'M', 'V', 'R', 'L', 'O', 'S'], 'X':['E'], 'Y':['T'], 'Z':['E', 'Y', 'S', 'O', 'F', 'N', 'P', 'R', 'T', 'K', 'M', 'L', 'A', 'D', 'G']}
```

Since each encrypted letter corresponds to exactly one decrypted letter, once an encrypted letter is solved, the solution can be removed as a possible solution for all other encrypted letters. The ```simplify_decryption()``` function takes care of this. In the event that removing a potential solution leaves an encrypted letter with only one possible solution, the function runs itself again. This simplifies the final ```Cypher.cypher``` to the following:

```
{'A':[], 'B':['I'], 'C':['S', 'D', 'Y', 'H', 'B', 'O', 'R', 'W', 'M', 'K', 'P', 'F', 'X', 'Z', 'U', 'V'], 'D':['N'], 'E':['B', 'D', 'H', 'M', 'S', 'W', 'Y', 'O', 'R', 'F', 'U', 'K', 'P', 'Z'], 'F':[], 'G':[], 'H':['B', 'D', 'M', 'O', 'R', 'F'], 'I':[], 'J':['A'], 'K':['L'], 'L':['H', 'S', 'O', 'U'], 'M':[], 'N':['C'], 'O':['M', 'O', 'R', 'U', 'Y', 'V', 'X', 'H', 'K', 'P', 'W'], 'P':['B', 'D', 'F', 'H', 'K', 'M', 'O', 'P', 'R', 'S', 'U', 'W', 'Y'], 'Q':[], 'R':[], 'S':['G'], 'T':[], 'U':['B', 'D', 'H', 'K', 'M', 'O', 'P', 'R', 'S', 'W', 'X'], 'V':[], 'W':['W', 'M', 'V', 'R', 'O', 'S'], 'X':['E'], 'Y':['T'], 'Z':['Y', 'S', 'O', 'F', 'P', 'R', 'K', 'M', 'D']}
```

### Decryption
Now that the ```Cypher``` has been simplifed, we can attempt to decrypt the message. The ```decrypt(self)``` function first calls the ```replace(self)``` function, which assembles a partially/fully decrypted version of the encrypted message by comparing each letter in the encrypted message to the list of letters with known solutions and replacing them when possible, otherwise leaving them encrypted. The ```replace(self)``` function also keeps track of how many letters were replaced and returns this value. Below are the relevant lines of code from the ```replace(self)``` function.

```
def replace(self):
    solved = []
    self.solved_letters(solved)
    self.decrypted = ''

    counter = 0  # Track how many letters were replaced
    for line in range(0, len(self.encrypted)):
        for letter in range(0, len(self.encrypted[line])):
            flag = True
            for value in solved:
                # If encrypted letter matches a solved letter, replace it with solution
                if self.encrypted[line][letter] == value[0]:
                    self.decrypted = ''.join((self.decrypted, value[1]))
                    flag = False
                    counter = counter + 1
                    break
            if flag:
                self.decrypted = ''.join(
                    (self.decrypted, self.encrypted[line][letter]))

    return(counter)
```

The ```decrypt(self)``` function prints the encrypted message and decrypted message, then determines how many alphabetic characters the message contains, if that is not already known.

```
def decrypt(self):
    count = self.replace()
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
        for letter in self.encrypted[0]:
            if letter.isalpha():
                self.message_length = self.message_length + 1
```

This leads to three possible scenarios:
1. The decrypted message is identical to the encrypted message. This means no letters were able to be replaced.
2. The decrypted message is not identical to the encrypted message, but the number of letters replaced is not equal to the total number of letters. This means only some letters were able to be replaced.
3. The decrypted message is not identical to the encrypted message, and the number of letters replaced is equal to the total number of letters. This means all the letters were able to be replaced.

In case 3, the message is decrypted, and nothing else needs to be done. In cases 1 and 2, further analysis is required. To determine the case, the ```decrypt(self)``` function compares ```count```, the number of letters that were replaced, with ```self.message_length```, the total number of alphabetic characters in the message, then proceeds accordingly.

```
if count != self.message_length:
    self.partially_solved()
    self.word_frequency()
    self.rerun_check()
```

### Partially solved words
In the event that the message was only semi-decrypted, it becomes possible to further narrow down potential letter solutions by examining any partially solved words. Attempting to decrypt our[example sentence](#original-text) outputs the following:

```
encrypted
['YPX EBULY WXYPHC EHU XLYBWJYBDS YPX BDYXKKBSXDNX 
HE J UOKXU BL YH KHHZ JY YPX WXD PX PJL JUHODC PBW']
decrypted
TPE EIULT WETPHC EHU ELTIWATING TPE INTELLIGENCE HE A UOLEU IL TH LHHZ AT TPE WEN PE PAL AUHONC PIW  
```
and its [encryption](#encrypted-text)

## File structure
The repository consists of the following files:
* [.gitignore](.gitignore)
* [LICENSE](LICENSE)
* [README.md](README.md)
* [dictionary.txt](dictionary.txt)
* [patterns.py](patterns.py)
* [word_patterns.py](word_patterns.py)
* [main.py](main.py)

The [.gitignore file](.gitignore) contains the files and directories for Git to ignore when tracking updates to the repository.

The [LICENSE file](LICENSE) outlines the ways you may use and/or modify this program.

The [README.md file](README.md) is what maintains what you are currently reading!

The [dictionary.txt file](dictionary.txt) is a plaintext file of words in the English language. Whenever this is updated, [patterns.py](patterns.py) needs to be rerun.

The [patterns.py file](patterns.py) contains a function called ```get_word_pattern(word)``` that returns the corresponding word pattern for ```word```, where ```word``` is a string passed to the function. This file also creates and updates [word_patterns.py](word_patterns.py) and should be rerun whenever [dictionary.txt](dictionary.txt) is updated.

The [word_patterns.py file](word_patterns.py) exists to streamline the main program runtime. It consists of a Python dictionary where the dictionary keys are the different [word patterns](#word-patterns) of the entries in [dictionary.txt](dictionary.txt) and the values are the corresponding English words. It is created by the [patterns.py file](patterns.py). Whenever [dictionary.txt](dictionary.txt) is updated, the [patterns.py file](patterns.py) needs to be rerun in order to keep this up to date. Due to the size of [dictionary.txt](dictionary.txt), this process can take a while, so the [main.py file](main.py) only references [word_patterns.py](word_patterns.py) instead of updating it on runtime.

The [main.py file](main.py) is the actual cryptogram solving portion of the code. When this is run, a window opens with the option to choose an encrypted file. Selecting this option opens a file browsing window where an encrypted .txt file may be selected. Once a file is selected, the cryptogram decryption option becomes available. Selecting this option decrypts the chosen encrypted file.
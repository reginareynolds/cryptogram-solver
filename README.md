# cryptogram-solver
A program to intelligently decrypt cryptogram puzzles.

## What is a cryptogram?
A cryptogram is a type of word puzzle. In it, a piece of text is encrypted with a substitution cypher. This works by replacing every letter with a different letter. To solve the puzzle, the user needs to undo the substitutions to return the text to its original state. Below is an example.

#### Original text:
THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG.
#### Encrypted text:
ZYI JHCST MANDB VNR QHELW NXIA ZYI KFUO GNP.
### Encryption substitution cypher:
|**Original letter**|**Encrypted letter**|
|:---:|:---:|
| A | F |
| B | M |
| C | S |
| D | G |
| E | I |
| F | V |
| G | P |
| H | Y |
| I | C |
| J | Q |
| K | T |
| L | K |
| M | E |
| N | B |
| O | N |
| P | L |
| Q | J |
| R | A |
| S | W |
| T | Z |
| U | H |
| V | X |
| W | D |
| X | R |
| Y | O |
| Z | U |

To decrypt the cryptogram, the user would need to construct the inverted substitution cypher.

### Decryption substitution cypher

|**Encrypted letter**|**Original letter**|
|:---:|:---:|
| A | R |
| B | N |
| C | I |
| D | W |
| E | M |
| F | A |
| G | D |
| H | U |
| I | E |
| J | Q |
| K | L |
| L | P |
| M | B |
| N | O |
| O | Y |
| P | G |
| Q | J |
| R | X |
| S | C |
| T | K |
| U | Z |
| V | F |
| W | S |
| X | V |
| Y | H |
| Z | T |

## How this program works
This program works by taking an encrypted input, identifying the [relative patterns](#word-patterns) of the encrypted words, and comparing those relative patterns to a [list of known matches](word_patterns.py). The known matches are then cross-referenced with each other, and matches that contradict one another are removed from the pool of potential candidates. This process is repeated until no more matches can be removed.

If the cryptogram is still not solved at that point, the user is presented with the different possible decryptions and the likelihood of their correctness based on the frequency of each potential word in the English language. The user can then make a final decision on the correct decryption.

## Why this program works
Cryptograms are encrypted using substitution cyphers. This means that any given letter is located in the same location whether it is encrypted or decrypted. In other words, the encrypted text units retain the same sequence as the decrypted text units. This varies from a transposition cypher, where the encryption process retains the value of the text unit but changes the location.

Because the text sequence is maintained, the relative pattern of the letters in the text stays the same. 

Consider the [example sentence](#original-text) and its [encryption](#encrypted-text).

This example consists of 43 total alphabetic characters and 9 total words. Of those 43 alphabetic characters, there are 26 unique characters. Of the 9 total words, there are 8 unique words. These numbers are true for both the original and the encrypted text.

The words can be further categorized by length.

|**Three letter words**|**Four letter words**|**Five letter words**|
|:---:|:---:|:---:|
| THE | OVER | QUICK |
| FOX | LAZY | BROWN |
| DOG |  | JUMPS |

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
| THE | ZYI | 012 |
| QUICK | JHCST | 01234 |  
| BROWN | MANDB | 01234 |  
| FOX | VNR | 012 |  
| JUMPS | QHELW | 01234 |  
| OVER | NXIA | 0123 |  
| THE | ZYI | 012 |  
| LAZY | KFUO | 0123 |  
| DOG | GNP | 012 |

Notice that the word pattern remains identical for both the original text and the encrypted text. As explained above, the substitution cypher maintains the relative pattern of the letters in the text, which allows the word pattern to stay the same.

### File structure
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
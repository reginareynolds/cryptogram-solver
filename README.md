# cryptogram-solver
A program to intelligently decrypt cryptogram puzzles.

## What is a cryptogram?
A cryptogram is a type of word puzzle. In it, a piece of text is encrypted with a substitution cypher. This works by replacing every letter with a different letter. To solve the puzzle, the user needs to undo the substitutions to return the text to its original state. Below is an example.

### Original text:
THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG.
### Encrypted text:
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

## How it works
Cryptograms are encrypted using substitution cyphers. This means that any given letter is located in the same location whether it is encrypted or decrypted. In other words, the encrypted text units retain the same sequence as the decrypted text units. This varies from a transposition cypher, where the encryption process retains the value of the text unit but changes the location.

Because the text sequence is maintained, the relative pattern of the letters in the text stays the same. Consider the example sentence and its encryption below.

### Original text:
THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG.
### Encrypted text:
ZYI JHCST MANDB VNR QHELW NXIA ZYI KFUO GNP.

This sentence consists of 43 total alphabetic characters and 9 total words. Of those 43 alphabetic characters, there are 26 unique characters. Of the 9 total words, there are 8 unique words. These numbers are true for both the original and the encrypted text.

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
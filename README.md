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

Because the text sequence is maintained, the pattern of the words in the text stays the same.

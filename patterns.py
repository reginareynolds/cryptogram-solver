import pprint

# Identify word patterns
def get_word_pattern(word):
    next = 0
    letters = {}
    pattern = []

    for letter in word:
        if letter not in letters:
            letters[letter] = str(next)
            next = next + 1
        pattern.append(letters[letter])
    
    return ''.join(pattern)

if __name__ == '__main__':
    dictionary_patterns = {}

    # Read in all words from dictionary file
    words = None
    with open('cryptogram-solver/dictionary.txt') as file:
        words = file.read().split('\n')
    
    for word in words:
        # Determine pattern for each word in dictionary file
        pattern = get_word_pattern(word)

        # Check for word pattern in pattern list
        if pattern in dictionary_patterns:
            dictionary_patterns[pattern].append(word)  # Add English word to matching pattern key
        else:
            dictionary_patterns[pattern] = [word]  # Create new pattern key and initialize value list with English word

    # Create file of all word patterns and corresponding words
    with open('cryptogram-solver/word_patterns.py', 'w') as file:
        file.write('dictionary_patterns = ')
        file.write(pprint.pformat(dictionary_patterns))
# TODO: Account for words with more than 10 unique letters. The current pattern recognition depends on a single character to identify the letter, so anything beyond 9 will be interpreted as two letters (10 will appear to be 1 and 0, 11 will appear to be 1 and 1, etc.)
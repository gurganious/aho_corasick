# aho_corasick
Python version of the Aho–Corasick string-searching algorithm invented by Alfred V. Aho and Margaret J. Corasick

# Usage

    substrings = ['cash', 'shew', 'ew']
    aho = Aho_Corasick(substrings)                     # Set up datastructure

    # Check against string cashew
    for word in aho.get_keywords_found("cashew"):
        print(word)

# Output
    {'index': 0, 'word': 'cash'}
    {'index': 2, 'word': 'shew'}
    {'index': 4, 'word': 'ew'}

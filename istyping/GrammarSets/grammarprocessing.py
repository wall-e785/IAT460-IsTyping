import random

#referenced from week 3 lab
def generate(symbol, grammar):
    """
    Recursively generate a string from the grammar starting with the given symbol.

    Args:
        symbol: The symbol to start generating from

    Returns:
        A string generated from the grammar rules
    """
    if isinstance(symbol, str) and symbol in grammar:
        production = random.choice(grammar[symbol])
        if isinstance(production, list):
            return ' '.join(generate(sym, grammar) for sym in production)
        return production
    return symbol

#this function helps properly format the sentence by capitalizing
def format_sentence(sentence):
    #referenced for upper: https://stackoverflow.com/questions/17794241/how-do-i-convert-only-specific-parts-of-a-string-to-uppercase-in-python
    return sentence[0].upper() + sentence[1:]

#overloaded version that also adds caps to end of punctuation
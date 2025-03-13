friend_grammar1 = {
    #non-terminal symbols
    'S': [['GREET', 'ASK', 'FRIEND'], ['how is my', 'V', 'FRIEND']],

    #terminal symbols
    'V': ['bestest', 'favourite', 'coolest'],
    'GREET': ['hi', 'hello', 'hey'],
    'ASK': ['what\'s up', 'how are you', 'what are you doing'],
    'FRIEND': ['friend', 'fren', 'bestie']
    }

you_grammar1 = {
    #non-terminal symbols
    'S-POS': [['GREET', 'ASK', 'FRIEND'], ['how is my', 'V', 'FRIEND']],
    'S-NEU': [],
    'S-NEG': [['why']],

    #terminal symbols
    'Det': ['it is', 'it\'s' ],
    'V': ['bestest', 'favourite', 'coolest'],
    'GREET': ['hi', 'hello', 'hey'],
    'ASK': ['what\'s up', 'how are you', 'what are you doing'],
    'FRIEND': ['friend', 'fren', 'bestie']
}
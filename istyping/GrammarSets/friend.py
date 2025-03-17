friend_grammar1 = {
    #non-terminal symbols
    'S': [['GREET', 'ASK', 'FRIEND'], ['how is my', 'V', 'FRIEND']],

    #terminal symbols
    'V': ['bestest', 'favourite', 'coolest'],
    'GREET': ['hi!', 'hello!', 'hey!'],
    'ASK': ['what\'s up', 'how are you', 'what are you doing'],
    'FRIEND': ['friend', 'fren', 'bestie']
}

you_grammar1 = {
    #non-terminal symbols
    'S': [['GOOD', 'Det', 'LOC', 'TIME']],

    #terminal symbols
    'GOOD': ['okay', 'good', 'great', 'fine'],
    'Det': ['I am', 'I\'m',  'just'],
    'LOC': ['in class', 'at home'],
    'TIME': ['now', 'right now', 'at the moment']
}

friend_grammar2 = {
    #non-terminal symbols
    'S': [['IJ', 'well I', 'V', 'if you want to come to my', 'EVENT', 'TIME'], ['ADJ', 'my', 'EVENT', 'is', 'TIME', 'V', 'if you want to come']],

    #terminal symbols
    'IJ': ['oh', 'ah', 'i see'],
    'V': ['wanted to see', 'wanted to ask', 'wanna ask'],
    'EVENT': ['poetry reading', 'project presentation', 'art showcase'],
    'TIME': ['later', 'tonight'],
    'ADJ': ['nice', 'cool']

}
you_grammar2 = {
    #non-terminal symbols
    'S': [['IJ', 'I', 'PLAN', 'a date', 'TIME', 'CAN', 'LET']],

    #terminal symbols
    'IJ': ['hm', 'hmm', 'well'],
    'PLAN': ['planned', 'scheduled'],
    'TIME': ['tonight', 'later'],
    'CAN': ['can I', 'I\'ll'],
    'LET': ['let you know', 'get back to you']
}

friend_grammar3 = {
    #non-terminal symbols
    'S': [['YES', 'SURE', 'been busy?']],

    #terminal symbols
    'YES': ['yea', 'yes'],
    'SURE': ['sure', 'of course', 'okay']
}

you_grammar3 = {
    #non-terminal symbols
    'S': [['YES']],

    #terminal symbols
    'YES': ['yea', 'yes']
}

friend_grammar4={
    #non-terminal symbols
    'S': [['OK', 'LUCK', 'and let me know']],

    #terminal symbols
    'OK': ['ok', 'okay', 'sounds good'],
    'LUCK': ['good luck', 'have fun']
}

you_grammar4 = {
    #non-terminal symbols
    'S': [['THANKS']],

    #terminal symbols
    'THANKS': ['thanks', 'thank you']
}



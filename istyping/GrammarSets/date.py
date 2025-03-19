you_grammar1 = {
    #non-terminal symbols
    'S': [['HELLO', ', I', 'WANT', 'CHECK', 'we are still', 'ON', 'LATER']],

    #terminal symbols
    'HELLO': ['hey', 'hi', 'hello'],
    'WANT': ['just wanted to', 'was hoping to'],
    'CHECK': ['make sure', 'check if', 'see if', 'confirm if'],
    'ON': ['on for', 'good for'],
    'LATER': ['later', 'tonight']
}

date_grammar1 = {
    #non-terminal symbols
    'S': [['YES', ', I\'ll', 'TELL']],

    #terminal symbols
    'YES': ['yea', 'ok', 'oh'],
    'TELL': ['let you know', 'tell you later', 'give you a heads up']
}

you_grammar2 = {
    #non-terminal symbols
    'S': [[['I'], 'so I can', 'SCHEDULE', 'the rest of my', 'TIME']],
    
    #terminal symbols
    'I': ['I just really need to know', 'Can you let me know now'],
    'SCHEDULE': ['plan out', 'schedule'],
    'TIME': ['day', 'night', 'evening']
}

date_grammar2 = {
    #non-terminal symbols
    'S': [['OK', 'WILL']],

    #terminal symbols
    'OK': ['ok', 'okay', 'kay'],
    'WILL': ['will do', 'tell you later']
}

you_grammar3 = {
    #non-terminal symbols
    'S': [['Can I get a yes/no?']]
    #terminal symbols
}

date_grammar3 = {
    #non-terminal symbols
    'S': [['Sorry I\'m doing something right now, I\'ll get back to you']]
    #terminal symbols
}

you_grammar4 = {
    #non-terminal symbols
    'S': [['oh ok']]
    #terminal symbols
}
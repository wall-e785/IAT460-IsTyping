you_grammar1 = {
    #non-terminal symbols
    'S': [['HELLO', ', I', 'WANT', 'CHECK', 'we are still', 'ON', 'LATER'], ['HELLO', 'POLITE', 'still', 'ON', 'LATER']],

    #terminal symbols
    'HELLO': ['hey', 'hi', 'hello'],
    'WANT': ['just wanted to', 'was hoping to'],
    'CHECK': ['make sure', 'check if', 'see if', 'confirm if'],
    'ON': ['on for', 'good for'],
    'LATER': ['later', 'tonight'],
    'POLITE': ['how are u?', 'how was your day?', 'what\'s up?'],
}

date_grammar1 = {
    #non-terminal symbols
    'S-EAGER': [['hi', 'YES', ', I\'ll', 'TELL', 'sorry'], ['HI', ', i\'m', 'SURE', 'CONFIRM']],
    'S-UNINTERESTED': [['hi', 'will', 'TELL'], ['THINK', 'talk later']],

    #terminal symbols
    'YES': ['yea', 'ok', 'oh'],
    'HI': ['hey', 'hi', 'hello'],
    'TELL': ['let you know', 'tell you later', 'give you a heads up'],
    'SURE': ['not sure', 'not 100%'],
    'THINK': ['think so', 'probably', 'should be'],
    'CONFIRM': ['will reconfirm asap', 'get back to you asap']
}

you_grammar2 = {
    #non-terminal symbols
    'S': [['I', 'so I can', 'SCHEDULE', 'the rest of my', 'TIME'], ['PREFER', 'tell me now becuase i\'m', 'SCHEDULING', 'my', 'TIME']],
    
    #terminal symbols
    'I': ['I just really need to know', 'Can you let me know now'],
    'SCHEDULE': ['plan out', 'schedule'],
    'SCHEDULING': ['planning out', 'scheduling'],
    'TIME': ['day', 'night', 'evening'],
    'PREFER': ['can you', 'prefer if you']
}

date_grammar2 = {
    #non-terminal symbols
    'S-EAGER': [['OK', 'WILL'], ['SURE', 'OK'], ['OK', 'but can\'t rn', 'SORRY']],
    'S-UNINTERESTED': [['OK', 'but i\'ll', 'FIGURE']],

    #terminal symbols
    'OK': ['ok', 'okay', 'kay'],
    'WILL': ['will do', 'tell you later'],
    'SURE': ['sure thing', 'got it', 'of course'],
    'SORRY': [':(', 'sorry'],
    'FIGURE': ['figure it out later', 'find out later', 'am still thinking']
}

you_grammar3 = {
    #non-terminal symbols
    'S': [['Can I get a', 'QUICK', 'CONFIRMATION'], ['OK', 'just need a', 'QUICK', 'CONFIRMATION']],

    #terminal symbols
    'OK': ['ok', 'okay', 'k'],
    'QUICK': ['quick', 'concrete'],
    'CONFIRMATION': ['yes/no', 'yay/nay']
}

date_grammar3 = {
    #non-terminal symbols
    'S-EAGER': [['SORRY', 'i\'m also', 'PLANNING', 'so i can\'t say', 'SURE', 'yet'], ['i\'m', 'BUSY', 'SORRY', 'get back to you soon']],
    'S-UNINTERESTED': [['CANT', 'i\'m', 'BUSY', 'NOW']],

    #terminal symbols
    'CANT': ['i can\'t', 'no', 'can\'t'],
    'BUSY': ['doing something', 'busy', 'in a rush'],
    'NOW': ['right now', 'rn', 'atm', 'at the moment'],
    'SORRY': ['sorry', 'srry'],
    'PLANNING': ['planning', 'scheduling'],
    'SURE': ['for sure', '100%']
}

you_grammar4 = {
    #non-terminal symbols
    'S': [['NP', 'END']],

    #terminal symbols
    'NP': ['oh ok', 'no problem', 'sure'],
    'END': ['ttyl', ':)']
}
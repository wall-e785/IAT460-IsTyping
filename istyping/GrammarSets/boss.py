boss_grammar1 = {
    #non-terminal symbols
    'S': ['Hello', 'Hi', 'Greetings']
    #terminal symbols
}

you_grammar1 = {
    #non-terminal symbols
    'S': [['Hi, <name>'], ['Hi, did you need something?']]
    #terminal symbols
}

boss_grammar2 = {
    #non-terminal symbols
    'S': [['Did you get it?'], ['Have you sent it?']]
    #terminal symbols
}

you_grammar2 = {
    #non-terminal symbols
    'S': [['I\'m not sure I know what you\'re referring to']]
    #terminal symbols
}

boss_grammar3= {
    #non-terminal symbols
    'S': [['Oh the design revisions, I forgot to send the email. Can you get them done tonight?']]
    #terminal symbols
}

you_grammar3 = {
    #non-terminal symbols
    'S': [['Sorry, I\'m going to be unavailable tonight but I\'ll get them done by tomorrow morning']]
    #terminal symbols
}

boss_grammar4 = {
    #non-terminal symbols
    'S': [['Okay...'], ['Noted.']]
    #terminal symbols
}

you_grammar4 = {
    #non-terminal symbols
    'S': [['Sorry again.']]
    #terminal symbols
}

boss_grammar5 = {
#non-terminal symbols
    'S': [['It\'s fine just keep in touch.']]
    #terminal symbols
}

you_grammar5 = {
    #non-terminal symbols
    'S': [['Thanks']]
    #terminal symbols
}
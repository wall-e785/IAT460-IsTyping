responded = -1

boss_grammar1 = {
    #terminal symbols
    'S-PROF': ['Hello.', 'Hi.', 'Good afternoon.'],
    'S-CASUAL': ['hey, question!', 'hello! quick question', 'hi! question for you']
}

you_grammar1 = {
    #non-terminal symbols
    'S': [['Hi,', 'NEED'], ['Hello', 'NEED']],

    #terminal symbols
    'NEED': ['is everything okay?', 'how can I help?', 'what\'s up?']
}

boss_grammar2 = {
    #terminal symbols
    'S-PROF': [['Did you get it?'], ['Have you sent it?'], ['Let me know when you\'ve sent it.']],
    'S-CASUAL': [['did you get my email from earlier?'], ['just wondering when you were going to send it!']]
}

you_grammar2 = {
    #non-terminal symbols
    'S': [['SORRY', ', I\'m not sure I know what you\'re referring to']],

    #terminal symbols
    'SORRY': ['Sorry', 'Apologies']
}

boss_grammar3= {
    #non-terminal symbols
    'S-PROF': [['The', 'WORK', 'EMAIL', 'We need them done', 'QUICK'], ['There is an urgent', 'WORK', 'email']],
    'S-CASUAL': [['OOPS', 'PROBLEM', ', the', 'WORK', 'chances you\'re free tonight?'], ['The', 'work', 'OOPS', 'PROBLEM']],

    #terminal symbols
    'WORK': ['new logo revisions', 'social media update'],
    'OOPS': ['whoops!', 'oops!', 'my bad!'],
    'PROBLEM': ['forgot to hit send', 'bad wifi'],
    'EMAIL': ['you should\'ve got an email', 'did you see the email?'],
    'QUICK': ['quickly', 'soon']
}

you_grammar3 = {
    #non-terminal symbols
    'S-PROF': [['GOT', 'SORRY', 'but the', 'EARLIEST', 'I can', 'WORK', 'is tomorrow']],
    'S-CASUAL': [['NW', 'but I\'m', 'UNSURE', 'if I have time', 'TIME']],

    #terminal symbols
    'SORRY': ['sorry', 'apologies'],
    'NW': ['no worries!', 'no problem!'],
    'UNSURE': ['not sure', 'unsure'],
    'TIME': ['tonight', 'later'],
    'GOT': ['I got it', 'I see it'],
    'EARLIEST': ['earliest', 'soonest'],
    'WORK': ['work on it', 'get on it']
}

boss_grammar4 = {
    #non-terminal symbols
    'S-PROF': [['Noted.'], ['Understood.']],
    'S-CASUAL': [['OH', 'OKAY'], ['OKAY', 'FINE']],

    #terminal symbols
    'OH': ['oh', 'mhm'],
    'OKAY': ['okay...', 'alright...', 'sure...'],
    'FINE': ['that\'s fine', 'got it']
}

you_grammar4 = {
    #non-terminal symbols
    'S': [['SORRY', 'again.']],

    #terminal symbols
    'SORRY': ['Sorry', 'Apologies'],
}

boss_grammar5 = {
#non-terminal symbols
    #if the user responded with neutral/high, boss asks if they're okay
    'S-PROF-CARE': [['FINE', 'hope', 'HOPE']],
    'S-CASUAL-CARE': [['NP', 'are you ok?', 'You seem', 'STRESS']],

    #otherwise just respond neutrally
    'S-PROF': ['NP'],
    'S-CASUAL': ['NP', ':)'],

    #terminal symbols
    'NP': ['No problem', 'No worries'],
    'FINE': ['It\'s fine', 'It\'s okay'],
    'STRESS': ['stressed', 'tired'],
    'HOPE': ['all is well', 'you\'re not too busy', 'school isn\'t too stressful']
}

you_grammar5 = {
    #non-terminal symbols
    'S-CARE': [['I\'m', 'OK', 'thanks for', 'CHECK'], ['I\'m', 'alright, just', 'BUSY']],
    'S': [['THANKS'], ['KIT']],

    #terminal symbols
    'THANKS': ['Thanks', 'Thank you'],
    'KIT': ['Keep in touch', 'Will send updates'], 
    'OK': ['ok', 'alright'],
    'CHECKING': ['checking', 'asking'],
    'BUSY': ['busy', 'lots to-do']
}
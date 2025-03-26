import random

event = None
friend_responded = -1

events = {'e': ['poetry reading', 'project presentation', 'art showcase']}
event = random.choice(events['e'])
print(event)

friend_grammar1 = {
    #non-terminal symbols
    'S': [['GREET', 'ASK', 'FRIEND'], ['how is my', 'V', 'FRIEND'], ['ASK']],

    #terminal symbols
    'V': ['bestest', 'favourite', 'coolest'],
    'GREET': ['Hi!', 'Hello!', 'Hey!'],
    'ASK': ['what\'s up', 'how are you', 'what are you doing'],
    'FRIEND': ['friend?', 'fren?', 'bestie?']
}

you_grammar1 = {
    #non-terminal symbols
    'S': [['GOOD', 'Det', 'LOC', 'TIME'], ['Det', 'LOC', 'it\'s', 'GOOD']],

    #terminal symbols
    'GOOD': ['okay', 'good', 'great', 'fine'],
    'Det': ['I am', 'I\'m',  'just'],
    'LOC': ['in class', 'at home'],
    'TIME': ['now', 'right now', 'at the moment']
}

friend_grammar2 = {
    #if player chose a high response
        #if the friend has a high anxiousness
    'S-HIGH-GOOD': [['UNDERSTAND', 'I really want to see you at my', event, 'TIME', 'NOPRESSURE']],
        #if the friend has a low anxiousness
    'S-HIGH-BAD': [['PAUSE', 'my', event, 'is', 'TIME', 'WISH', 'see u there'], ['PAUSE', 'DUDE', 'u gotta come to my', event, 'TIME', 'plsss'], 'PAUSE', 'come to my', event, 'TIME', 'you', 'MISS', 'last time'],

    #terminal symbols
    'PAUSE': ['oh...', 'uhh, okay...', 'you good? anyways'],
    'WISH': ['hope to', 'wish to'],
    'DUDE': ['dude', 'ay'],
    'UNDERSTAND': ['Oh, hope all is well!', 'That\'s nice!'],
    'NOPRESSURE': ['no pressure if you can\'t', 'totally understand if you are busy', 'i really need your support'],
    'MISS': ['missed out', 'missed', 'couldn\'t'],

    #otherwise
    'S': [['IJ', 'well I', 'V', 'if you want to come to my', event, 'TIME'], ['ADJ', '-hey btw, my', event, 'is', 'TIME', 'and', 'PEOPLE', 'will be there.', 'IN']],

    #terminal symbols
    'IJ': ['oh', 'ah', 'i see'],
    'V': ['wanted to see', 'wanted to ask', 'wanna ask'],
    'EVENT': ['poetry reading', 'project presentation', 'art showcase'],
    'TIME': ['later', 'tonight'],
    'ADJ': ['nice', 'cool'],
    'PEOPLE': ['a bunch of us', 'everyone', 'some of us'],
    'IN': ['you in?', 'hbu?', 'wanna come?']

}
you_grammar2 = {
    #non-terminal symbols
    'S': [['IJ', 'I', 'PLAN', 'a date', 'TIME', 'CAN', 'LET'], ['I\'m', 'UNSURE', 'about later yet', 'I', 'PLAN', 'a date']],

    #terminal symbols
    'IJ': ['hm', 'hmm', 'well'],
    'PLAN': ['planned', 'scheduled'],
    'TIME': ['tonight', 'later'],
    'CAN': ['can I', 'I\'ll'],
    'LET': ['let you know', 'get back to you'],
    'UNSURE': ['not sure', 'not set', 'not 100%']
}

friend_grammar3 = {
    #non-terminal symbols
    'S': [['OK', 'LMK', 'been', 'BUSY'], ['BUSY', 'just', 'LMK']],

    #terminal symbols
    'YES': ['KK', 'Okay', 'Ok'],
    'LMK': ['lmk', 'let me know', 'tell me ASAP'],
    'BUSY': ['busy lately?', 'working hard lately?', 'stressed lately?']
}

you_grammar3 = {
    #non-terminal symbols
    'S': [['YES', 'HAVE', 'work has been', 'BUSY', 'and dating', 'BAD'], ['GROAN', 'dating', 'BAD', 'and work has been', 'BUSY']],

    #terminal symbols
    'YES': ['Yea', 'Yes'],
    'HAVE': ['I have', 'it has been'],
    'BUSY': ['busy', 'stressful', 'exhausting'],
    'BAD': ['kinda sucks', 'isn\'t fun', 'is difficult'],
    'GROAN': ['ugh', 'awful', 'terrible']

}

friend_grammar4={
    #non-terminal symbols
    #if the friend has a high anxiousness
    'S-HIGH': [['OK', 'LUCK', 'REMIND'], ['You\'ll', 'FINE', 'REMIND']],

    #if the friend has a low anxiousness
    'S-LOW': [['NOPROB', 'FRIEND', 'u\'ll', 'FINE', 'dw ttyl'], ['REMIND_LOW', 'u\'ll', 'FINE', 'ttyl']],

    #terminal symbols
    'OK': ['Ok', 'Okay', 'Aw'],
    'LUCK': ['good luck', 'have fun'],
    'FINE': ['be fine', 'do great', 'be okay'],
    'REMIND': ['don\'t forget to text!', 'last reminder to text later!', 'remember to confirm!'],
    'NOPROB': ['np', 'nw'],
    'FRIEND': ['dude', 'fren', 'bestie'],
    'REMIND_LOW': ['better not forget to text', 'don\'t ghost me later']
}

you_grammar4 = {
    #non-terminal symbols
    'S': [['THANKS']],

    #terminal symbols
    'THANKS': ['thanks', 'thank you', 'will do']
}

friend_grammar5 = {
    #non-terminal symbols
    'S-HIGH': [['HEY', 'the', event, 'is in', 'TIME', 'CHECKIN'], ['HEY', 'only', 'TIME', 'until the', event, 'COMING']],
    'S-LOW': [['still drowning in indecision? or make a choice? lol', 'TIME', 'left til my', event], ['only', 'TIME', 'left...', 'soooo, u comin to the', event]],

    #terminal symbols
    'HEY': ['hey!', 'ay!', 'hello!'],
    'TIME': ['an hour', '45 minutes', 'hour and a half'],
    'CHECKIN': ['updates?', 'any news?'],
    'COMING': ['hope you come!', 'thought i\'d check in!']
}



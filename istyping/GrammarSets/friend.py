import random
casualness = random.randint(0, 100)

friend_grammar1 = {
    #non-terminal symbols
    'S': [['GREET', 'ASK', 'FRIEND'], ['how is my', 'V', 'FRIEND']],

    #terminal symbols
    'V': ['bestest', 'favourite', 'coolest'],
    'GREET': ['hi!', 'hello!', 'hey!'],
    'ASK': ['what\'s up', 'how are you', 'what are you doing'],
    'FRIEND': ['friend', 'fren', 'bestie']
}

#add vocab depending on the context
# if(casualness < 30){
   
# }else{

# }
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
    'S': [['V', 'V', 'V'], ['V', 'V', 'V']],

    #terminal symbols
    'V': ['bestest', 'favourite', 'coolest'],
    'GREET': ['hi!', 'hello!', 'hey!'],
    'ASK': ['what\'s up', 'how are you', 'what are you doing'],
    'FRIEND': ['friend', 'fren', 'bestie']
}



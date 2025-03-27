#Preferences is used to keep track of the character traits for each speaker, as well as calculate the users performance

import random

#pre-determined characteristics
friend_anxiousness = 0
date_eagerness = 0
boss_professionalism = 0

#keep track of user's performance
friend_correct = 0
date_correct = 0
boss_correct = 0

def setup():
    global friend_anxiousness, date_eagerness, boss_professionalism, friend_correct, date_correct, boss_correct, event
    #randomly assign each of the characteristics
    friend_anxiousness = random.randint(0, 100)
    date_eagerness = random.randint(0, 100)
    boss_professionalism = random.randint(0, 100)

    print("friend:" + str(friend_anxiousness) + " date:" + str(date_eagerness) + " boss:" + str(boss_professionalism))

    #reset performance scores
    friend_correct = 0
    date_correct = 0
    boss_correct = 0

#checks if the preferred answer was selected based on the casualness of friend
def check_friend(selected):
    global friend_correct
    if selected == 1: #add one point if they chose the neutral phrase
        friend_correct += 1
    #add two points if they chose high/low responses suiting the friend's 'casualness'
    elif (selected == 0 and friend_anxiousness >= 50) or (selected == 2 and friend_anxiousness <=50): 
        friend_correct += 2

#checks if the preferred answer was selected based on the eagerness of the date
def check_date(selected):
    global date_correct
    if selected == 1: #add one point if they chose the neutral phrase
        date_correct += 1
    #add two points if they chose high/low responses suiting the date's 'eagerness'
    elif (selected == 0 and date_eagerness >=50) or (selected == 2 and date_eagerness <= 50):
        date_correct +=2

#checks if the preferred answer was selected based on the professionalism of the boss
def check_boss(selected):
    global boss_correct
    if selected == 1: #add one point if they chose the neutral phrase
        boss_correct +=1
    #add two points if they chose high/low responses suiting the professionalism of the boss
    elif (selected == 0 and boss_professionalism >=50) or (selected == 2 and boss_professionalism <= 50):
        boss_correct +=2

#used to display the characteristics on the end screen
def get_friend():
    if friend_anxiousness >= 50:
        return "was an anxious person"
    else:
        return "was a laidback person"
def get_date():
    if date_eagerness >=50:
        return "was eager to meet"
    else:
        return "was uneager to meet"
def get_boss():
    if boss_professionalism >= 50:
        return "preferred professional messages"
    else:
        return "preferred casual messages"
    
#used to display the performance on the end screen
def get_friend_score():
    global friend_correct
    if friend_correct >= 4:
        return "most"
    else:
        return "little"
    
def get_date_score():
    global date_correct
    if date_correct >= 4:
        return "most"
    else:
        return "little"
    
def get_boss_score():
    global boss_correct
    if boss_correct >= 4:
        return "most"
    else:
        return "little"


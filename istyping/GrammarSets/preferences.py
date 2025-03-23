#add vocab depending on the context
import random

friend_anxiousness = 0
date_eagerness = 0
boss_professionalism = 0

friend_correct = 0
date_correct = 0
boss_correct = 0

date_responded = -1
boss_responded = -1

def setup():
    global friend_anxiousness, date_eagerness, boss_professionalism, friend_correct, date_correct, boss_correct, event
    friend_anxiousness = random.randint(0, 100)
    date_eagerness = random.randint(0, 100)
    boss_professionalism = random.randint(0, 100)

    print("friend:" + str(friend_anxiousness) + " date:" + str(date_eagerness) + " boss:" + str(boss_professionalism))

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

def check_date(selected):
    global date_correct
    if selected == 1:
        date_correct += 1
    elif (selected == 0 and date_eagerness >=50) or (selected == 2 and date_eagerness <= 50):
        date_correct +=2

def check_boss(selected):
    global boss_correct
    if selected == 1:
        boss_correct +=1

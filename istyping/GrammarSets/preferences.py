#add vocab depending on the context
import random

friend_casualness = 0
date_eagerness = 0
boss_professionalism = 0

friend_correct = 0
date_correct = 0
boss_correct = 0

def setup():
    global friend_casualness, date_eagerness, boss_professionalism, friend_correct, date_correct, boss_correct
    friend_casualness = random.randint(0, 100)
    date_eagerness = random.randint(0, 100)
    boss_professionalism = random.randint(0, 100)

    print("friend:" + str(friend_casualness) + " date:" + str(date_eagerness) + " boss:" + str(boss_professionalism))

    friend_correct = 0
    date_correct = 0
    boss_correct = 0

#checks if the preferred answer was selected based on the casualness of friend
def check_friend(selected):
    global friend_correct
    if selected == 1: #add one point if they chose the neutral phrase
        friend_correct += 1
    #add two points if they chose high/low responses suiting the friend's 'casualness'
    elif (selected == 0 and friend_casualness <= 50) or (selected == 2 and friend_casualness >=50): 
        friend_correct += 2

def check_date(selected):
    global date_correct
    if selected == 1:
        date_correct += 1
    elif (selected == 0 and date_eagerness >=70) or (selected == 2 and date_eagerness <= 70):
        date_correct +=2

def check_boss(selected):
    global boss_correct
    if selected == 1:
        boss_correct +=1

import pygame #used this video to review pygame basics: https://www.youtube.com/watch?v=y9VG3Pztok8

#referenced this link to import my own classes: https://csatlas.com/python-import-file-module/
import UI.GUI as GUI
import GrammarSets.grammarprocessing as grammar
import GrammarSets.friend as friend
import GrammarSets.date as date
import GrammarSets.boss as boss
import GrammarSets.preferences as preferences

import Arduino.arduniohandler as Arduino
import math
#import time

#referenced this for classes: https://www.w3schools.com/python/python_classes.asp

#initialize/setup pygame
pygame.init()
pygame.display.set_caption("is-typing")

#intiliaze fonts
pygame.font.init()
font_path = pygame.font.match_font("verdana")
bold_font_path = pygame.font.match_font("verdana", True)
italic_font_path = pygame.font.match_font("verdana", False, True)
bold_italic_font_path = pygame.font.match_font("verdana", True, True)
h1 = pygame.font.Font(font_path, 32)
h2 = pygame.font.Font(bold_italic_font_path, 48)
h3 = pygame.font.Font(font_path, 20)
h4 = pygame.font.Font(font_path, 17)
transition_font = pygame.font.Font(bold_font_path,100)
name_header = pygame.font.Font(bold_font_path, 48)

#states for FSM
MAIN = 0
INTRO = 1
FRIEND = 2
DATE = 3
BOSS = 4
END = 5
TRANSITION = 6
FRIEND_END = 7

state = MAIN
run = True

#current speaker to give to Gemini API for context
currSpeaker = ""

#variables to keep track of which option was selected by the user
optionHigh = "Anxious Response!"
optionNeu = "Neutral Response!"
optionLow = "Lowkey Response!"
MAX_TEXT_LENGTH = 41

HIGH = 0
NEUTRAL = 1
LOW = 2

message_counter = 1
selected = -1

#setup the window
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((1920,1080))
resized_screen = pygame.transform.scale(screen, (SCREEN_WIDTH, SCREEN_HEIGHT))

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
window.blit(resized_screen, (0,0))

#button class, creates a button which has a visual component (rectangle) and text on top of it
class Button:
    def __init__(self, xPos, yPos, width, height, image):
        self.xPos = xPos
        self.yPos = yPos
        self.width = width
        self.height = height
        self.image = image

    #used to check mouse clicks by comparison bounding box and cursor position
    def checkMousePress(self, mouseX, mouseY):
        if mouseX > self.xPos and mouseX < self.xPos + self.width and mouseY > self.yPos and mouseY < self.yPos + self.height:
            return True

    #renders image onto the screen
    def draw(self):
        screen.blit(self.image, (self.xPos,self.yPos))

#referenced and modified transition screen from https://stackoverflow.com/questions/58540537/how-to-fade-the-screen-out-and-back-in-using-pygame
#also referenced this to learn more about alpha in pygame: https://stackoverflow.com/questions/6339057/draw-transparent-rectangles-and-polygons-in-pygame
class Fader:

    def __init__(self):
        self.fading = None
        self.alpha = 0
        self.bg = pygame.image.load("istyping/images/blacktransition.jpg")
        self.bg.set_alpha(self.alpha)

    def next(self):
        if not self.fading:
            self.fading = 'OUT'
            self.alpha = 0

    def draw(self):
        if self.fading == 'OUT' or self.fading == 'IN':
            self.update()
            self.bg.set_alpha(self.alpha)
            screen.blit(self.bg, (0,0))

    def update(self):
        if self.fading == 'OUT':
            self.alpha += 3
            if self.alpha >= 255:
                global state, currScreen
                if state == INTRO:
                    currScreen = TransitionScreen("Friend")
                    state = TRANSITION
                elif state == TRANSITION:
                    global currSpeaker, countingdown
                    if currScreen.name == "Friend":
                        preferences.setup()
                        state = FRIEND      
                        countingdown = True
                        currSpeaker = "friend"
                        currScreen = FriendScreen()
                    elif currScreen.name == "Date":
                        state = DATE
                        currSpeaker = "date"
                        currScreen = DateScreen()
                        pygame.time.delay(1000)
                    elif currScreen.name == "Boss":
                        state = BOSS
                        currSpeaker = "boss"
                        currScreen = BossScreen()
                        pygame.time.delay(1000)
                elif state == FRIEND:
                    currScreen = TransitionScreen("Date")
                    state = TRANSITION
                elif state == DATE:
                    currScreen = TransitionScreen("Boss")
                    state = TRANSITION
                elif state == BOSS:
                    state = FRIEND_END
                    currScreen = friendEndScreen()
                elif state == FRIEND_END:
                    state = END
                    currScreen = endScreen()
                self.fading = 'IN'
        else:
            self.alpha -= 5
            if self.alpha <= 0:
                self.fading = None  

  
# create an instance for Arduino Board
analogPrinter = Arduino.AnalogPrinter()

analogPrinter.start()

#setting up timer referenced from: https://gamedevacademy.org/pygame-timer-tutorial-complete-guide/
TIMEREVENT = pygame.USEREVENT +1
pygame.time.set_timer(TIMEREVENT, 1000) #timerevent is called every 1 second

COUNTDOWN = 9
#time to countdown from for choosing pressure to respond with
arduino_countdown = COUNTDOWN
countingdown = False

#homescreen class: holds UI for homescreen
class HomeScreen:
    def __init__(self):
        self.startButton = Button(613, 255, 379, 105,  pygame.image.load("istyping/images/start_button.jpg"))
        self.aboutButton = Button(613, 412, 379, 105, pygame.image.load("istyping/images/start_button.jpg"))
        self.bg = pygame.image.load("istyping/images/testbg.jpg")
          
#friendscreen class: holds UI and messages for friend dialogue
class FriendScreen:
    def __init__(self):
        self.name = "FRIEND"
        self.bg = pygame.image.load("istyping/images/text_screen_bg.jpg")

        global optionHigh
        global optionNeu
        global optionLow

        self.conversation = [
            grammar.generate('S', friend.friend_grammar1),
            grammar.generate('S', friend.you_grammar1),
            grammar.generate('S', friend.friend_grammar2),
            grammar.generate('S', friend.you_grammar2),
            grammar.generate('S', friend.friend_grammar3),
            grammar.generate('S', friend.you_grammar3),
        ]

        if preferences.friend_anxiousness >= 50:
            self.conversation.append(grammar.generate('S-HIGH', friend.friend_grammar4))
        else:    
            self.conversation.append(grammar.generate('S-LOW', friend.friend_grammar4))
        
        self.conversation.append(grammar.generate('S', friend.you_grammar4))

        self.currMessage = self.conversation[0]
        grammar.processing = True
        optionNeu = self.conversation[1]
        optionHigh = grammar.get_prompt(self.currMessage, optionNeu, 'friend', 'HIGH')
        optionLow = grammar.get_prompt(self.currMessage, optionNeu, 'friend', 'LOW')

#datescreen class: holds UI and messages for date dialogue
class DateScreen:
    def __init__(self):
        self.name = "DATE"
        self.currMessage = ""
        self.bg = pygame.image.load("istyping/images/text_screen_bg.jpg")

        global optionHigh
        global optionNeu
        global optionLow

        grammar.processing = True
        optionNeu = grammar.generate('S', date.you_grammar1)
        optionHigh = grammar.get_prompt(self.currMessage, optionNeu, 'date', 'HIGH')
        optionLow = grammar.get_prompt(self.currMessage, optionNeu, 'date', 'LOW')

#bossscreen class: holds UI and messages for boss dialogue
class BossScreen:
    def __init__(self):
        self.name = "BOSS"
        self.currMessage = None

        if preferences.boss_professionalism >=50:
            self.currMessage = grammar.generate('S-PROF', boss.boss_grammar1)
        else:
            self.currMessage = grammar.generate('S-CASUAL', boss.boss_grammar1)
        self.bg = pygame.image.load("istyping/images/text_screen_bg.jpg")

        global optionHigh
        global optionNeu
        global optionLow

        grammar.processing = True
        optionNeu = grammar.generate('S', boss.you_grammar1)
        optionHigh = grammar.get_prompt(self.currMessage, optionNeu, 'boss', 'HIGH')
        optionLow = grammar.get_prompt(self.currMessage, optionNeu, 'boss', 'LOW')

#tutscreen class: holds UI for tutorial screen
class TutScreen:
    def __init__(self):
        self.backButton = Button(82, 632, 224, 62,  pygame.image.load("istyping/images/back_button.jpg"))
        self.nextButton = Button(995, 632, 224, 62,  pygame.image.load("istyping/images/next_button.jpg"))


#endscreen class: holds UI for end screen to show user's performance
class EndScreen:
    def __init__(self):
        self.homeButton = Button(547, 545, 224, 62,  pygame.image.load("istyping/images/home_button.jpg"), (0,255,0), h1.render('Start', False, (0,0,0)))
        self.bg = pygame.image.load("istyping/images/end_bg.jpg")

class TransitionScreen:
    def __init__ (self, name):
        self.bg = pygame.image.load("istyping/images/transition_bg.jpg")
        self.name = name

class friendEndScreen:
    def __init__ (self):
        self.messageimg = pygame.image.load("istyping/images/friend_final_text.jpg")
        self.yPos = SCREEN_HEIGHT
        self.alpha = 0
        if preferences.friend_anxiousness >= 50:
            self.text = grammar.generate('S-HIGH', friend.friend_grammar5)
        else:
            self.text = grammar.generate('S-LOW', friend.friend_grammar5)
#setup current screen, used to keep track alongside current state what is showing
currScreen = HomeScreen()
fader = Fader()

#main loop - used when on home screen
def mainLoop():
    global currScreen
    global state

    #draw background image and buttons
    screen.blit(currScreen.bg.convert(), (0,0))

    startButton = currScreen.startButton
    aboutButton = currScreen.aboutButton 
    startButton.draw()
    aboutButton.draw()



    pygame.display.flip()

    #event handlers
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #exit the window
           global run
           run = False
        elif event.type == pygame.MOUSEBUTTONDOWN: #when click is detected
            pos = pygame.mouse.get_pos()

            #check if any buttons were clicked
            if(startButton.checkMousePress(pos[0], pos[1])):
                print("start!")
                currScreen = TutScreen()
                state = INTRO
            elif(aboutButton.checkMousePress(pos[0], pos[1])):
                print("about!")  

#text loop - used by the friend, date and boss screens to draw the UI
def textScreen():
    screen.fill((255,255,255))
    screen.blit(currScreen.bg.convert(), (0,0))

    screen.blit(GUI.profile_icon.convert(), (38,216))
    screen.blit(GUI.text_them.convert(), (155,151))
    screen.blit(GUI.profile_icon.convert(), (1143,595))


    #set up the three text options and draw them
    global optionHigh, optionNeu, optionLow, arduino_countdown

    # posButton = currScreen.posButton
    # neuButton = currScreen.neuButton
    # negButton = currScreen.negButton

    # posButton.draw()
    # neuButton.draw()
    # negButton.draw()
    #(posButton.checkMousePress(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])) or
    #(neuButton.checkMousePress(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])) or
    # (negButton.checkMousePress(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])) or

    if analogPrinter.data > (1/3)*2:
        screen.blit(GUI.high_indic.convert(), (593,313))

    if (analogPrinter.data >= 1/3 and analogPrinter.data <= (1/3)*2):
        screen.blit(GUI.neutral_indic.convert(), (593,441))

    if  analogPrinter.data < 1/3:
        screen.blit(GUI.low_indic.convert(), (593,562))

    screen.blit(GUI.thinking_you.convert(), (684,289))
    screen.blit(GUI.thinking_you.convert(), (684,417))
    screen.blit(GUI.thinking_you.convert(), (684,539))

    #y-positions of the start of the text box depending on how many lines there are
    HIGH_4LINES_Y = 304
    HIGH_3LINES_Y = 314
    HIGH_2LINES_Y = 326
    HIGH_1LINE_Y = 337

    NEU_4LINES_Y = 435
    NEU_3LINES_Y = 443
    NEU_2LINES_Y = 455
    NEU_1LINE_Y = 464

    LOW_4LINES_Y = 555
    LOW_3LINES_Y = 563
    LOW_2LINES_Y = 575
    LOW_1LINE_Y = 585

    THEM_4LINES_Y = 165
    THEM_3LINES_Y = 175
    THEM_2LINES_Y = 186
    THEM_1LINE_Y = 195
    
    high_num_lines = None
    neu_num_lines = None
    low_num_lines = None
    them_num_lines = None

    global MAX_TEXT_LENGTH
    formattedHigh = grammar.format_text(optionHigh, MAX_TEXT_LENGTH)
    formattedNeu = grammar.format_text(optionNeu, MAX_TEXT_LENGTH)
    formattedLow = grammar.format_text(optionLow, MAX_TEXT_LENGTH)
    formattedThem = grammar.format_text(currScreen.currMessage, MAX_TEXT_LENGTH)

    #for each of the options, check how many lines they need
    if len(formattedHigh) == 4:
        high_num_lines = HIGH_4LINES_Y
        screen.blit(h4.render(formattedHigh[0], True, (0,0,0)), (708, high_num_lines))
        screen.blit(h4.render(formattedHigh[1], True, (0,0,0)), (708, high_num_lines+21))
        screen.blit(h4.render(formattedHigh[2], True, (0,0,0)), (708, high_num_lines+42))
        screen.blit(h4.render(formattedHigh[3], True, (0,0,0)), (708, high_num_lines+63))
    elif len(formattedHigh) == 3: #3 lines
        high_num_lines = HIGH_3LINES_Y
        screen.blit(h4.render(formattedHigh[0], True, (0,0,0)), (708, high_num_lines))
        screen.blit(h4.render(formattedHigh[1], True, (0,0,0)), (708, high_num_lines+24))
        screen.blit(h4.render(formattedHigh[2], True, (0,0,0)), (708, high_num_lines+48))
    elif len(formattedHigh) == 2: #2 lines
        high_num_lines = HIGH_2LINES_Y
        screen.blit(h4.render(formattedHigh[0], True, (0,0,0)), (708, high_num_lines))
        screen.blit(h4.render(formattedHigh[1], True, (0,0,0)), (708, high_num_lines+24))
    elif len(formattedHigh) == 1: #1 line
        high_num_lines = HIGH_1LINE_Y 
        screen.blit(h4.render(formattedHigh[0], True, (0,0,0)), (708, high_num_lines))
    else:
        high_num_lines = HIGH_1LINE_Y 
        screen.blit(h4.render("Error: Line Too Long", True, (0,0,0)), (708, high_num_lines))

    if len(formattedNeu) == 4:
        neu_num_lines = NEU_4LINES_Y
        screen.blit(h4.render(formattedNeu[0], True, (0,0,0)), (708, neu_num_lines))
        screen.blit(h4.render(formattedNeu[1], True, (0,0,0)), (708, neu_num_lines+21))
        screen.blit(h4.render(formattedNeu[2], True, (0,0,0)), (708, neu_num_lines+42))
        screen.blit(h4.render(formattedNeu[3], True, (0,0,0)), (708, neu_num_lines+63))
    elif len(formattedNeu) == 3: #3 lines
        neu_num_lines = NEU_3LINES_Y
        screen.blit(h4.render(formattedNeu[0], True, (0,0,0)), (708, neu_num_lines))
        screen.blit(h4.render(formattedNeu[1], True, (0,0,0)), (708, neu_num_lines+24))
        screen.blit(h4.render(formattedNeu[2], True, (0,0,0)), (708, neu_num_lines+48))
    elif len(formattedNeu) == 2: #2 lines
        neu_num_lines = NEU_2LINES_Y
        screen.blit(h4.render(formattedNeu[0], True, (0,0,0)), (708, neu_num_lines))
        screen.blit(h4.render(formattedNeu[1], True, (0,0,0)), (708, neu_num_lines+24))
    elif len(formattedNeu) == 1: #1 line
        neu_num_lines = NEU_1LINE_Y
        screen.blit(h4.render(formattedNeu[0], True, (0,0,0)), (708, neu_num_lines))
    else:
        neu_num_lines = NEU_1LINE_Y
        screen.blit(h4.render("Error: Line Too Long", True, (0,0,0)), (708, neu_num_lines))

    if len(formattedLow) == 4:
        low_num_lines = LOW_4LINES_Y
        screen.blit(h4.render(formattedLow[0], True, (0,0,0)), (708, low_num_lines))
        screen.blit(h4.render(formattedLow[1], True, (0,0,0)), (708, low_num_lines+21))
        screen.blit(h4.render(formattedLow[2], True, (0,0,0)), (708, low_num_lines+42))
        screen.blit(h4.render(formattedLow[3], True, (0,0,0)), (708, low_num_lines+63))
    elif len(formattedLow) == 3: #3 lines
        low_num_lines = LOW_3LINES_Y
        screen.blit(h4.render(formattedLow[0], True, (0,0,0)), (708, low_num_lines))
        screen.blit(h4.render(formattedLow[1], True, (0,0,0)), (708, low_num_lines+24))
        screen.blit(h4.render(formattedLow[2], True, (0,0,0)), (708, low_num_lines+48))
    elif len(formattedLow) == 2: #2 lines
        low_num_lines = LOW_2LINES_Y
        screen.blit(h4.render(formattedLow[0], True, (0,0,0)), (708, low_num_lines))
        screen.blit(h4.render(formattedLow[1], True, (0,0,0)), (708, low_num_lines+24))
    elif len(formattedLow) == 1: #1 line
        low_num_lines = LOW_1LINE_Y
        screen.blit(h4.render(formattedLow[0], True, (0,0,0)), (708, low_num_lines))
    else:
        low_num_lines = LOW_1LINE_Y
        screen.blit(h4.render("Error: Line Too Long", True, (0,0,0)), (708, low_num_lines))

    if len(formattedThem) == 4: #3 lines
        them_num_lines = THEM_4LINES_Y
        screen.blit(h4.render(formattedThem[0], True, (0,0,0)), (215, them_num_lines))
        screen.blit(h4.render(formattedThem[1], True, (0,0,0)), (215, them_num_lines+21))
        screen.blit(h4.render(formattedThem[2], True, (0,0,0)), (215, them_num_lines+42))
        screen.blit(h4.render(formattedThem[3], True, (0,0,0)), (215, them_num_lines+63))
    elif len(formattedThem) == 3: #3 lines
        them_num_lines = THEM_3LINES_Y
        screen.blit(h4.render(formattedThem[0], True, (0,0,0)), (215, them_num_lines))
        screen.blit(h4.render(formattedThem[1], True, (0,0,0)), (215, them_num_lines+24))
        screen.blit(h4.render(formattedThem[2], True, (0,0,0)), (215, them_num_lines+48))
    elif len(formattedThem) == 2: #2 lines
        them_num_lines = THEM_2LINES_Y
        screen.blit(h4.render(formattedThem[0], True, (0,0,0)), (215, them_num_lines))
        screen.blit(h4.render(formattedThem[1], True, (0,0,0)), (215, them_num_lines+24))
    elif len(formattedThem) == 1: #1 line
        them_num_lines = THEM_1LINE_Y 
        screen.blit(h4.render(formattedThem[0], True, (0,0,0)), (215, them_num_lines))
    else:
        them_num_lines = THEM_1LINE_Y 
        screen.blit(h4.render("Error: Line Too Long", True, (0,0,0)), (215, them_num_lines))


    #rendering the speaker's message
    screen.blit(name_header.render(currSpeaker, True, (0,0,0)), (575, 24))
    screen.blit(h2.render(str(arduino_countdown), True, (0,0,0)), (865, 200))

    #referenced countdown arc from: https://stackoverflow.com/questions/67168804/how-to-make-a-circular-countdown-timer-in-pygame
    percentage = (arduino_countdown*11)/100
    end_angle = 2 * math.pi * percentage
    pygame.draw.arc(window, (100, 100, 100), pygame.Rect(854, 200, 64, 64), 0, end_angle, 4)


    #nested method for retrieving messages from grammar sets/Gemini API
    def get_messages():
        global message_counter, optionNeu, optionHigh, optionLow, state, currScreen, currSpeaker, arduino_countdown, countingdown
        message_counter+=1
        countingdown = True
        grammar.processing = True

        #generate messages depending on the current speaker, and determine the set based on the message number
        if state == FRIEND:
            if(message_counter == 2):
                if selected == HIGH:
                    if preferences.friend_anxiousness>=50:
                        currScreen.conversation[2] = grammar.generate('S-HIGH-GOOD', friend.friend_grammar2)
                    else:
                        currScreen.conversation[2] = grammar.generate('S-LOW-BAD', friend.friend_grammar2)
                else:
                    currScreen.conversation[2] = grammar.generate('S', friend.friend_grammar2)
                currScreen.currMessage = currScreen.conversation[2]
                optionNeu = currScreen.conversation[3] #grammar.generate('S', friend.you_grammar2)
                optionHigh = grammar.get_prompt(currScreen.currMessage, optionNeu, currSpeaker, 'HIGH')
                optionLow = grammar.get_prompt(currScreen.currMessage, optionNeu, currSpeaker, 'LOW')
            elif(message_counter == 3):
                currScreen.currMessage = currScreen.conversation[4] #grammar.generate('S', friend.friend_grammar3)
                optionNeu = currScreen.conversation[5]#grammar.generate('S', friend.you_grammar3)
                optionHigh = grammar.get_prompt(currScreen.currMessage, optionNeu, currSpeaker, 'HIGH')
                optionLow = grammar.get_prompt(currScreen.currMessage, optionNeu, currSpeaker, 'LOW')

                friend.friend_responded = selected
            elif(message_counter == 4):
                currScreen.currMessage = currScreen.conversation[6]

                optionNeu = currScreen.conversation[7]#grammar.generate('S', friend.you_grammar4)
                optionHigh = grammar.get_prompt(currScreen.currMessage, optionNeu, currSpeaker, 'HIGH')
                optionLow = grammar.get_prompt(currScreen.currMessage, optionNeu, currSpeaker, 'LOW')

                # if preferences.friend_anxiousness >= 50:
                #     currScreen.currMessage = grammar.generate('S-HIGH', friend.friend_grammar4)
                # else:    
                #     currScreen.currMessage = grammar.generate('S-LOW', friend.friend_grammar4)
            else:
                pygame.time.delay(3000)
                message_counter = 1
                if fader.fading == None:
                    fader.next()
        elif state == DATE:
            if(message_counter == 2):
                optionNeu = grammar.generate('S', date.you_grammar2)
                optionHigh = grammar.get_prompt(currScreen.currMessage, optionNeu, currSpeaker, 'HIGH')
                optionLow = grammar.get_prompt(currScreen.currMessage, optionNeu, currSpeaker, 'LOW')

                if preferences.date_eagerness >= 50:
                    currScreen.currMessage = grammar.generate('S-EAGER', date.date_grammar1)
                else:
                    currScreen.currMessage = grammar.generate('S-UNINTERESTED', date.date_grammar1)
            elif(message_counter == 3):
                optionNeu = grammar.generate('S', date.you_grammar3)
                optionHigh = grammar.get_prompt(currScreen.currMessage, optionNeu, currSpeaker, 'HIGH')
                optionLow = grammar.get_prompt(currScreen.currMessage, optionNeu, currSpeaker, 'LOW')

                if preferences.date_eagerness >= 50:
                    currScreen.currMessage = grammar.generate('S-EAGER', date.date_grammar2)
                else:
                    currScreen.currMessage = grammar.generate('S-UNINTERESTED', date.date_grammar2)
            elif(message_counter == 4):
                optionNeu = grammar.generate('S', date.you_grammar4)
                optionHigh = grammar.get_prompt(currScreen.currMessage, optionNeu, currSpeaker, 'HIGH')
                optionLow = grammar.get_prompt(currScreen.currMessage, optionNeu, currSpeaker, 'LOW')
                if preferences.date_eagerness >= 50:
                    currScreen.currMessage = grammar.generate('S-EAGER', date.date_grammar3)
                else:
                    currScreen.currMessage = grammar.generate('S-UNINTERESTED', date.date_grammar3)
            else:
                pygame.time.delay(3000)
                message_counter = 1
                if fader.fading == None:
                    fader.next()
        elif state == BOSS:
            if(message_counter == 2):
                optionNeu = grammar.generate('S', boss.you_grammar2)
                optionHigh = grammar.get_prompt(currScreen.currMessage, optionNeu, currSpeaker, 'HIGH')
                optionLow = grammar.get_prompt(currScreen.currMessage, optionNeu, currSpeaker, 'LOW')
                if preferences.boss_professionalism >=50:
                    currScreen.currMessage = grammar.generate('S-PROF', boss.boss_grammar2)
                else:
                    currScreen.currMessage = grammar.generate('S-CASUAL', boss.boss_grammar2)
            elif(message_counter == 3):
                if preferences.boss_professionalism >=50:
                    currScreen.currMessage = grammar.generate('S-PROF', boss.boss_grammar3)
                    optionNeu = grammar.generate('S-PROF', boss.you_grammar3)
                else:
                    currScreen.currMessage = grammar.generate('S-CASUAL', boss.boss_grammar3)      
                    optionNeu = grammar.generate('S-CASUAL', boss.you_grammar3) 
                optionHigh = grammar.get_prompt(currScreen.currMessage, optionNeu, currSpeaker, 'HIGH')
                optionLow = grammar.get_prompt(currScreen.currMessage, optionNeu, currSpeaker, 'LOW')     
            elif(message_counter == 4):
                boss.responded = selected
                optionNeu = grammar.generate('S', boss.you_grammar4)
                optionHigh = grammar.get_prompt(currScreen.currMessage, optionNeu, currSpeaker, 'HIGH')
                optionLow = grammar.get_prompt(currScreen.currMessage, optionNeu, currSpeaker, 'LOW')
                if preferences.boss_professionalism >=50:
                    currScreen.currMessage = grammar.generate('S-PROF', boss.boss_grammar4)
                else:
                    currScreen.currMessage = grammar.generate('S-CASUAL', boss.boss_grammar4)
            elif(message_counter == 5):
                if boss.responded <=1:
                    optionNeu = grammar.generate('S-CARE', boss.you_grammar5)
                else:
                    optionNeu = grammar.generate('S', boss.you_grammar5)

                optionHigh = grammar.get_prompt(currScreen.currMessage, optionNeu, currSpeaker, 'HIGH')
                optionLow = grammar.get_prompt(currScreen.currMessage, optionNeu, currSpeaker, 'LOW')
                if preferences.boss_professionalism >=50:
                    if boss.responded <= 1:
                        currScreen.currMessage = grammar.generate('S-PROF-CARE', boss.boss_grammar5)
                    else:
                        currScreen.currMessage = grammar.generate('S-PROF', boss.boss_grammar5)
                else:
                    if boss.responded <=1:
                        currScreen.currMessage = grammar.generate('S-CASUAL-CARE', boss.boss_grammar5)
                    else:
                        currScreen.currMessage = grammar.generate('S-CASUAL', boss.boss_grammar5)
            else:
                pygame.time.delay(3000)
                message_counter = 1
                if fader.fading == None:
                    fader.next()
            
    #event handlers
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #exit button
           global run
           run = False
        elif event.type == TIMEREVENT:
            global countingdown

            if countingdown:
                if arduino_countdown > 0:
                    arduino_countdown -= 1
                else:
                    arduino_countdown = COUNTDOWN 
                    countingdown = False

                    if state == FRIEND or state == DATE:
                        if message_counter <= 4:
                            if analogPrinter.data > (1/3)*2:
                                selected = HIGH
                            elif (analogPrinter.data >= 1/3 and analogPrinter.data <= (1/3)*2):
                                selected = NEUTRAL
                            elif analogPrinter.data < 1/3:
                                selected = LOW
                        if state == FRIEND:
                            preferences.check_friend(selected)
                        elif state == DATE:
                            preferences.check_date(selected)
                        if fader.fading == None:
                            get_messages()
                    elif state == BOSS:
                        if message_counter <= 5:
                            if analogPrinter.data > (1/3)*2:
                                selected = HIGH
                            elif (analogPrinter.data >= 1/3 and analogPrinter.data <= (1/3)*2):
                                selected = NEUTRAL
                            elif analogPrinter.data < 1/3:
                                selected = LOW
                            preferences.check_boss(selected)
                        if fader.fading == None:
                            get_messages()
                    print(selected)   
def tutScreen():
    screen.fill((255,255,255))

    global currScreen, state

    backButton = currScreen.backButton
    nextButton = currScreen.nextButton

    backButton.draw()
    nextButton.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT: #exit button
            global run
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN: #mouse click
            pos = pygame.mouse.get_pos()
            if(backButton.checkMousePress(pos[0], pos[1])):
                state = MAIN
                currScreen = HomeScreen()
            elif(nextButton.checkMousePress(pos[0], pos[1])):
                global fader
                if fader.fading == None:
                    fader.next()

            
def endScreen():
    screen.fill((255,255,255))

    global currScreen, state

    screen.blit(currScreen.bg, (0,0))
    homeButton = currScreen.homeButton

    homeButton.draw()

    screen.blit(h2.render("Friend Casualness: " + str(preferences.friend_anxiousness) + "%", True, (0,0,0)), (20, 40))
    screen.blit(h2.render("Date Eagerness: " + str(preferences.date_eagerness) + "%", True, (0,0,0)), (20, 60))
    screen.blit(h2.render("Boss Professionalism: " + str(preferences.boss_professionalism) + "%", True, (0,0,0)), (20, 80))

    screen.blit(h2.render("Friend Correct: " + str(preferences.friend_correct) + "/8", True, (0,0,0)), (400, 40))
    screen.blit(h2.render("Date Correct: " + str(preferences.date_correct) + "/8", True, (0,0,0)), (400, 60))
    screen.blit(h2.render("Boss Correct: " + str(preferences.boss_correct) + "/10", True, (0,0,0)), (400, 80))


    for event in pygame.event.get():
        if event.type == pygame.QUIT: #exit button
            global run
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN: #mouse click
            pos = pygame.mouse.get_pos()
            if(homeButton.checkMousePress(pos[0], pos[1])):
                state = MAIN
                currScreen = HomeScreen()

alpha = 0
name_pos = -200
showName = False
done = False
stay_on_screen = 4

def transitionLoop():
    screen.fill((255,255,255))

    global currScreen, alpha, showName, name_pos, done, stay_on_screen 
    #referenced transparency from: https://www.youtube.com/watch?v=8_HVdxBqJmE
    bg = currScreen.bg.copy()
    if alpha < 255 and not done:
        alpha+=10
    else:
        showName = True
        alpha = 255
    bg.set_alpha(alpha)
    screen.blit(bg, (0,0))

    if showName:
        if name_pos < 450:
            name_pos+=15
        else:
            showName = False
            done = True   
        screen.blit(transition_font.render(currScreen.name, True, (0,0,0)), (name_pos, 281))

    if stay_on_screen == 0:
        alpha = 0
        name_pos = -200
        showName = False
        done = False
        stay_on_screen = 4

    #event handlers
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #exit the window
            global run
            run = False 
        elif event.type == TIMEREVENT:
            if fader.fading == None and stay_on_screen < 4:
                fader.next()
            if done and stay_on_screen > 0:
                stay_on_screen -= 1

stay_on_screen2 = 10
def friendEndLoop():
    screen.fill((255,255,255))

    global currScreen, stay_on_screen2
    if currScreen.yPos > 253:
        currScreen.yPos-=10
    else:
        currScreen.yPos = 253
    
    if currScreen.yPos < 350:
        currScreen.alpha += 3

    currScreen.messageimg.set_alpha(currScreen.alpha)
    screen.blit(currScreen.messageimg, (265,currScreen.yPos))

    START_POINT = 323
    MAX_LENGTH = 37

    formatted_message = grammar.format_text(currScreen.text, MAX_LENGTH)

    if currScreen.yPos >=253 and currScreen.alpha > 25:
        if len(formatted_message) == 3: #3 lines
            screen.blit(h1.render("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", True, (0,0,0)), (490, START_POINT))
            screen.blit(h1.render(formatted_message[0], True, (0,0,0)), (490, START_POINT))
            screen.blit(h1.render(formatted_message[1], True, (0,0,0)), (490, START_POINT+40))
            screen.blit(h1.render(formatted_message[2], True, (0,0,0)), (490, START_POINT+80))
        elif len(formatted_message) == 2: #2 lines
            screen.blit(h1.render("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", True, (0,0,0)), (490, START_POINT))
            screen.blit(h1.render(formatted_message[0], True, (0,0,0)), (490, START_POINT))
            screen.blit(h1.render(formatted_message[1], True, (0,0,0)), (490, START_POINT+40))
        elif len(formatted_message) == 1: #1 line
            screen.blit(h1.render(formatted_message[0], True, (0,0,0)), (490, START_POINT))
        else:
            screen.blit(h1.render("Error: Message too long", True, (0,0,0)), (490, START_POINT))

    if stay_on_screen2 == 0:
        stay_on_screen2 = 10
    
    #event handlers
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #exit the window
            global run
            run = False 
        elif event.type == TIMEREVENT:
            if fader.fading == None and stay_on_screen2 < 4:
                fader.next()
            if stay_on_screen2 > 0:
                stay_on_screen2 -= 1
          

#core loop to run the program
while run:
    pygame.time.delay(10)
    #show current screen based on state
    if state == MAIN:
        mainLoop()
    elif state == INTRO:
        tutScreen()
    elif state == FRIEND:
        textScreen()
    elif state == DATE:
        textScreen()
    elif state == BOSS:
        textScreen()
    elif state == END:
        endScreen()
    elif state == TRANSITION:
        transitionLoop()
    elif state == FRIEND_END:
        friendEndLoop()


    #pygame.draw.rect(screen, (0,255,0), player)
    #key = pygame.key.get_pressed()
    if fader.fading != None:
        fader.draw()
    #updates screen to display objects
    pygame.display.update()
    
#exits window once the run loop ends
analogPrinter.stop()
pygame.quit()
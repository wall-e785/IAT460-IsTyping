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
MAX_TEXT_LENGTH = 35

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
    def __init__(self, xPos, yPos, width, height, visual, color):
        self.xPos = xPos
        self.yPos = yPos
        self.width = width
        self.height = height
        self.visual = visual
        self.color = color
        self.text = ""
        self.centerVisual()

    def __init__(self, xPos, yPos, width, height, visual, color, text):
        self.xPos = xPos
        self.yPos = yPos
        self.width = width
        self.height = height
        self.visual = visual
        self.color = color
        self.text = text
        self.centerVisual()

    def centerVisual(self):
        self.visual.center = (self.xPos, self.yPos)

    #used to check mouse clicks by comparison bounding box and cursor position
    def checkMousePress(self, mouseX, mouseY):
        if mouseX > self.xPos-self.width/2 and mouseX < self.xPos + self.width/2 and mouseY > self.yPos-self.height/2 and mouseY < self.yPos + self.height/2:
            return True

    #renders visual onto the screen
    def draw(self):
         pygame.draw.rect(screen, self.color, self.visual, 0, 10) 

#referenced transition screen from https://stackoverflow.com/questions/58540537/how-to-fade-the-screen-out-and-back-in-using-pygame
#also referenced this to learn more about alpha in pygame: https://stackoverflow.com/questions/6339057/draw-transparent-rectangles-and-polygons-in-pygame
class Fader:

    def __init__(self):
        self.fading = None
        self.alpha = 0
        self.surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.surf.set_alpha(self.alpha)
        self.surf.fill((0,0,0))

    def next(self):
        if not self.fading:
            self.fading = 'OUT'
            self.alpha = 0

    def draw(self):
        if self.fading == 'OUT' or self.fading == 'IN':
            self.update()
            print(self.alpha)
            screen.blit(self.surf, (0,0))
        # if self.fading:
        #     self.veil.set_alpha(self.alpha)
        #     screen.blit(self.veil, (0, 0))

    def update(self):
        if self.fading == 'OUT':
            self.alpha += 17
            if self.alpha >= 255:
                global state, currScreen, currSpeaker, countingdown 
                if state == MAIN:
                    preferences.setup()
                    state = FRIEND      
                    countingdown = True
                    currSpeaker = "friend"
                    currScreen = FriendScreen()
                self.fading = 'IN'
        else:
            self.alpha -= 17
            if self.alpha <= 0:
                self.fading = None  
        self.surf.set_alpha(self.alpha)
  
# create an instance for Arduino Board
analogPrinter = Arduino.AnalogPrinter()

analogPrinter.start()

#setting up timer referenced from: https://gamedevacademy.org/pygame-timer-tutorial-complete-guide/
TIMEREVENT = pygame.USEREVENT +1
pygame.time.set_timer(TIMEREVENT, 1000) #timerevent is called every 1 second

COUNTDOWN = 3 #9
#time to countdown from for choosing pressure to respond with
arduino_countdown = COUNTDOWN
countingdown = False

#homescreen class: holds UI for homescreen
class HomeScreen:
    def __init__(self):
        self.startButton = Button(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 250, 75,  pygame.Rect(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 250, 75), (0,255,0), h1.render('Start', False, (0,0,0)))
        self.aboutButton = Button(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 125, 250, 75, pygame.Rect(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 125, 250, 75), (200,200,200), h1.render('About', False, (0,0,0)))
        self.bg = pygame.image.load("istyping/images/testbg.jpg")
          
#friendscreen class: holds UI and messages for friend dialogue
class FriendScreen:
    def __init__(self):
        self.name = "FRIEND"
        self.currMessage = grammar.generate('S', friend.friend_grammar1)
        self.bg = pygame.image.load("istyping/images/text_screen_bg.jpg")

        global optionHigh
        global optionNeu
        global optionLow

        grammar.processing = True
        optionNeu = grammar.generate('S', friend.you_grammar1)
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
        self.backButton = Button(225, SCREEN_HEIGHT-200, 250, 40,  pygame.Rect(225, SCREEN_HEIGHT-200, 250, 40), (0,255,0), h1.render('Back', False, (0,0,0)))
        self.nextButton = Button(SCREEN_WIDTH-225, SCREEN_HEIGHT-200, 250, 40,  pygame.Rect(SCREEN_WIDTH-225, SCREEN_HEIGHT-200, 250, 40), (0,255,0), h1.render('Next', False, (0,0,0)))


#endscreen class: holds UI for end screen to show user's performance
class EndScreen:
    def __init__(self):
        self.homeButton = Button(SCREEN_WIDTH-225, SCREEN_HEIGHT-200, 250, 40,  pygame.Rect(SCREEN_WIDTH-225, SCREEN_HEIGHT-200, 250, 40), (0,255,0), h1.render('Start', False, (0,0,0)))

class TransitionScreen:
    def __init__ (self, name):
        self.bg = pygame.image.load("istyping/images/transition_bg.jpg")
        self.name = name

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

    screen.blit(startButton.text, (startButton.xPos-startButton.width/4, startButton.yPos-startButton.height/4))

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
    HIGH_3LINES_Y = 309
    HIGH_2LINES_Y = 320
    HIGH_1LINE_Y = 333

    NEU_3LINES_Y = 439
    NEU_2LINES_Y = 450
    NEU_1LINE_Y = 463

    LOW_3LINES_Y = 559
    LOW_2LINES_Y = 570
    LOW_1LINE_Y = 583

    THEM_3LINES_Y = 170
    THEM_2LINES_Y = 181
    THEM_1LINE_Y = 194

    high_num_lines = None
    neu_num_lines = None
    low_num_lines = None
    them_num_lines = None

    #for each of the options, check which line length they exceed, then trim and position them accordingly depending on how much space they take up
    if len(optionHigh) > MAX_TEXT_LENGTH*2: #3 lines
        high_num_lines = HIGH_3LINES_Y
        screen.blit(h3.render(optionHigh[:MAX_TEXT_LENGTH], True, (0,0,0)), (708, high_num_lines))
        screen.blit(h3.render(optionHigh[MAX_TEXT_LENGTH:MAX_TEXT_LENGTH*2], True, (0,0,0)), (708, high_num_lines+24))
        screen.blit(h3.render(optionHigh[MAX_TEXT_LENGTH*2:MAX_TEXT_LENGTH*3], True, (0,0,0)), (708, high_num_lines+48))
    elif len(optionHigh) > MAX_TEXT_LENGTH: #2 lines
        high_num_lines = HIGH_2LINES_Y
        screen.blit(h3.render(optionHigh[:MAX_TEXT_LENGTH], True, (0,0,0)), (708, high_num_lines))
        screen.blit(h3.render(optionHigh[MAX_TEXT_LENGTH:MAX_TEXT_LENGTH*2], True, (0,0,0)), (708, high_num_lines+24))
    else: #1 line
        high_num_lines = HIGH_1LINE_Y 
        screen.blit(h3.render(optionHigh[:MAX_TEXT_LENGTH], True, (0,0,0)), (708, high_num_lines))

    if len(optionNeu) > MAX_TEXT_LENGTH*2: #3 lines
        neu_num_lines = NEU_3LINES_Y
        screen.blit(h3.render(optionNeu[:MAX_TEXT_LENGTH], True, (0,0,0)), (708, neu_num_lines))
        screen.blit(h3.render(optionNeu[MAX_TEXT_LENGTH:MAX_TEXT_LENGTH*2], True, (0,0,0)), (708, neu_num_lines+24))
        screen.blit(h3.render(optionNeu[MAX_TEXT_LENGTH*2:MAX_TEXT_LENGTH*3], True, (0,0,0)), (708, neu_num_lines+48))
    elif len(optionNeu) > MAX_TEXT_LENGTH: #2 lines
        neu_num_lines = NEU_2LINES_Y
        screen.blit(h3.render(optionNeu[:MAX_TEXT_LENGTH], True, (0,0,0)), (708, neu_num_lines))
        screen.blit(h3.render(optionNeu[MAX_TEXT_LENGTH:MAX_TEXT_LENGTH*2], True, (0,0,0)), (708, neu_num_lines+24))
    else: #1 line
        neu_num_lines = NEU_1LINE_Y
        screen.blit(h3.render(optionNeu[:MAX_TEXT_LENGTH], True, (0,0,0)), (708, neu_num_lines))

    if len(optionLow) > MAX_TEXT_LENGTH*2: #3 lines
        low_num_lines = LOW_3LINES_Y
        screen.blit(h3.render(optionLow[:MAX_TEXT_LENGTH], True, (0,0,0)), (708, low_num_lines))
        screen.blit(h3.render(optionLow[MAX_TEXT_LENGTH:MAX_TEXT_LENGTH*2], True, (0,0,0)), (708, low_num_lines+24))
        screen.blit(h3.render(optionLow[MAX_TEXT_LENGTH*2:MAX_TEXT_LENGTH*3], True, (0,0,0)), (708, low_num_lines+48))
    elif len(optionLow) > MAX_TEXT_LENGTH: #2 lines
        low_num_lines = LOW_2LINES_Y
        screen.blit(h3.render(optionLow[:MAX_TEXT_LENGTH], True, (0,0,0)), (708, low_num_lines))
        screen.blit(h3.render(optionLow[MAX_TEXT_LENGTH:MAX_TEXT_LENGTH*2], True, (0,0,0)), (708, low_num_lines+24))
    else: #1 line
        low_num_lines = LOW_1LINE_Y
        screen.blit(h3.render(optionLow[:MAX_TEXT_LENGTH], True, (0,0,0)), (708, low_num_lines))

    if len(currScreen.currMessage) > MAX_TEXT_LENGTH*2: #3 lines
        them_num_lines = THEM_3LINES_Y
        screen.blit(h3.render(currScreen.currMessage[:MAX_TEXT_LENGTH], True, (0,0,0)), (215, them_num_lines))
        screen.blit(h3.render(currScreen.currMessage[MAX_TEXT_LENGTH:MAX_TEXT_LENGTH*2], True, (0,0,0)), (215, them_num_lines+24))
        screen.blit(h3.render(currScreen.currMessage[MAX_TEXT_LENGTH*2:MAX_TEXT_LENGTH*3], True, (0,0,0)), (215, them_num_lines+48))
    elif len(currScreen.currMessage) > MAX_TEXT_LENGTH: #2 lines
        them_num_lines = THEM_2LINES_Y
        screen.blit(h3.render(currScreen.currMessage[:MAX_TEXT_LENGTH], True, (0,0,0)), (215, them_num_lines))
        screen.blit(h3.render(currScreen.currMessage[MAX_TEXT_LENGTH:MAX_TEXT_LENGTH*2], True, (0,0,0)), (215, them_num_lines+24))
    else: #1 line
        them_num_lines = THEM_1LINE_Y 
        screen.blit(h3.render(currScreen.currMessage[:MAX_TEXT_LENGTH], True, (0,0,0)), (215, them_num_lines))


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
                optionNeu = grammar.generate('S', friend.you_grammar2)
                optionHigh = grammar.get_prompt(currScreen.currMessage, optionNeu, currSpeaker, 'HIGH')
                optionLow = grammar.get_prompt(currScreen.currMessage, optionNeu, currSpeaker, 'LOW')

                if selected == HIGH:
                    if preferences.friend_anxiousness>=50:
                        currScreen.currMessage = grammar.generate('S-HIGH-GOOD', friend.friend_grammar2)
                    else:
                        currScreen.currMessage = grammar.generate('S-LOW-BAD', friend.friend_grammar2)
                else:
                    currScreen.currMessage = grammar.generate('S', friend.friend_grammar2)
            elif(message_counter == 3):
                optionNeu = grammar.generate('S', friend.you_grammar3)
                optionHigh = grammar.get_prompt(currScreen.currMessage, optionNeu, currSpeaker, 'HIGH')
                optionLow = grammar.get_prompt(currScreen.currMessage, optionNeu, currSpeaker, 'LOW')
                currScreen.currMessage = grammar.generate('S', friend.friend_grammar3)

                friend.friend_responded = selected
            elif(message_counter == 4):
                optionNeu = grammar.generate('S', friend.you_grammar4)
                optionHigh = grammar.get_prompt(currScreen.currMessage, optionNeu, currSpeaker, 'HIGH')
                optionLow = grammar.get_prompt(currScreen.currMessage, optionNeu, currSpeaker, 'LOW')

                if preferences.friend_anxiousness >= 50:
                    currScreen.currMessage = grammar.generate('S-HIGH', friend.friend_grammar4)
                else:    
                    currScreen.currMessage = grammar.generate('S-LOW', friend.friend_grammar4)
            else:
                message_counter = 1
                state = DATE
                currSpeaker = "date"
                currScreen = DateScreen()
                pygame.time.delay(1000)
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
                message_counter = 1
                state = BOSS
                currSpeaker = "boss"
                currScreen = BossScreen()
                pygame.time.delay(1000)
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
                message_counter = 1
                state = END
                currScreen = EndScreen()
            
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
                global currSpeaker, countingdown 
                preferences.setup()
                state = FRIEND      
                countingdown = True
                currSpeaker = "friend"
                currScreen = FriendScreen()
            
def endScreen():
    screen.fill((255,255,255))

    global currScreen, state

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
stay_on_screen = 2

def transitionLoop():
    global currScreen, alpha, showName, name_pos, done 
    
    #referenced transparency from: https://www.youtube.com/watch?v=8_HVdxBqJmE
    bg = currScreen.bg.copy()
    if alpha < 30 and not done:
        alpha+=.5
    else:
        showName = True
        alpha = 255
    bg.set_alpha(alpha)
    screen.blit(bg, (0,0))

    if showName:
        if name_pos < 420:
            name_pos+=20
        else:
            showName = False
            done = True   
        screen.blit(transition_font.render(currScreen.name, True, (0,0,0)), (name_pos, 281))

    if stay_on_screen == 0:
        alpha -= 10

    pygame.display.flip()

    #event handlers
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #exit the window
            global run
            run = False 
        elif event.type == TIMEREVENT:
            if done and stay_on_screen > 0:
                stay_on_screen - 1

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
    
    fader.draw()
    #clear screen with each iteration

    #pygame.draw.rect(screen, (0,255,0), player)
    #key = pygame.key.get_pressed()

    #updates screen to display objects
    pygame.display.update()
    
#exits window once the run loop ends
analogPrinter.stop()
pygame.quit()
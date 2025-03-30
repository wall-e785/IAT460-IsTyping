#Main file to run to build this project.
#Contains the core pygame loop, screens, and FSM states

import pygame #used this video to review pygame basics and created foundation for project: https://www.youtube.com/watch?v=y9VG3Pztok8

#referenced this link to import my own classes: https://csatlas.com/python-import-file-module/
import UI.GUI as GUI
import GrammarSets.grammarprocessing as grammar
import GrammarSets.friend as friend
import GrammarSets.date as date
import GrammarSets.boss as boss
import GrammarSets.preferences as preferences

import Arduino.arduniohandler as Arduino
import math

#initialize/setup pygame
pygame.init()
pygame.display.set_caption("is-typing")

#intilize fonts, referenced from: https://www.pygame.org/docs/ref/font.html
pygame.font.init()

#project created with sf pro and helvetica
font_path = pygame.font.match_font("sf pro")
bold_font_path = pygame.font.match_font("sf pro", True)
italic_font_path = pygame.font.match_font("sf pro", False, True)
bold_italic_font_path = pygame.font.match_font("sf pro", True, True)
h1 = pygame.font.Font(font_path, 40)
h2 = pygame.font.Font(bold_italic_font_path, 60)
h3 = pygame.font.Font(bold_font_path, 30)
h4 = pygame.font.Font(font_path, 25)
h5 = pygame.font.Font(font_path, 30)

transition_font = pygame.font.Font(bold_font_path, 175)
name_header = pygame.font.Font(bold_font_path, 90)
prompt_font = pygame.font.Font(bold_font_path, 100)

#set up sound, referenced from: https://opensource.com/article/20/9/add-sound-python-game
pygame.mixer.init()
button_click = pygame.mixer.Sound("istyping/sounds/button_click.mp3")
receive_sound = pygame.mixer.Sound("istyping/sounds/receive_sound.mp3")
sent_sound = pygame.mixer.Sound("istyping/sounds/sent_sound.mp3")
transition_sound = pygame.mixer.Sound("istyping/sounds/transition_sound.mp3")
countdown_tick = pygame.mixer.Sound("istyping/sounds/countdown_tick.mp3")

#states for FSM
MAIN = 0
INTRO = 1
FRIEND = 2
DATE = 3
BOSS = 4
END = 5
TRANSITION = 6
FRIEND_END = 7
CREDITS = 8

state = MAIN
run = True

#current speaker to give to Gemini API for context
currSpeaker = ""

#variables to keep track of which option was selected by the user
optionHigh = "Anxious Response!"
optionNeu = "Neutral Response!"
optionLow = "Lowkey Response!"
MAX_TEXT_LENGTH = 43

HIGH = 0
NEUTRAL = 1
LOW = 2

message_counter = 1
selected = -1

#setup the window
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

#resized screen to try to improve resolution
screen = pygame.display.set_mode((1920,1080))
resized_screen = pygame.transform.scale(screen, (SCREEN_WIDTH, SCREEN_HEIGHT))

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
window.blit(resized_screen, (0,0))

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

#timer to keep the chosen responses on screen for a few seconds before next message
DISPLAY_COUNTDOWN = 2
display_countdown = DISPLAY_COUNTDOWN
display_countingdown = False
display_selected = None

#button class, creates a button which has a visual component (rectangle) and text on top of it
#reviewed python classes from: https://www.w3schools.com/python/python_classes.asp
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
            global button_click
            pygame.mixer.Sound.play(button_click)
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
        #if the screen is not fading, start the fade out
        if not self.fading:
            self.fading = 'OUT'
            self.alpha = 0

    def draw(self):
        if self.fading == 'OUT' or self.fading == 'IN':
            self.update()
            self.bg.set_alpha(self.alpha)
            screen.blit(self.bg, (0,0))

    def update(self):
        #while fading out, slowly increase alpha
        if self.fading == 'OUT':
            self.alpha += 3
            if self.alpha >= 255: #once alpha reaches its max, complete the transition to next state/screen as needed
                global state, currScreen
                if state == INTRO:
                    currScreen = TransitionScreen("Friend")
                    state = TRANSITION
                    global transition_sound
                    pygame.mixer.Sound.play(transition_sound)
                elif state == TRANSITION:
                    global currSpeaker, countingdown
                    if currScreen.name == "Friend":
                        friend.choose_event()
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
                    pygame.mixer.Sound.play(transition_sound)
                elif state == DATE:
                    currScreen = TransitionScreen("Boss")
                    state = TRANSITION
                    pygame.mixer.Sound.play(transition_sound)
                elif state == BOSS:
                    currScreen = FriendEndScreen()
                    state = FRIEND_END
                    global receive_sound
                    pygame.mixer.Sound.play(receive_sound)
                elif state == FRIEND_END:
                    currScreen = EndScreen()
                    state = END
                self.fading = 'IN' #once transition is completed, start fading in
        else:
            #fade in until 0 by decreasing alpha
            self.alpha -= 5
            if self.alpha <= 0 and self.fading != None:
                self.fading = None  
                if state == DATE or state == BOSS:
                    #reset countdowns for the start of the character (so it's uninterrupted by fade in)
                    global arduino_countdown, display_countdown, display_countingdown, display_selected
                    arduino_countdown = COUNTDOWN 
                    countingdown = True
                    display_countingdown = False
                    display_countdown = DISPLAY_COUNTDOWN
                    display_selected = None

#homescreen class: holds UI for homescreen
class HomeScreen:
    def __init__(self):
        self.startButton = Button(620, 255, 379, 105,  pygame.image.load("istyping/images/start_button.jpg"))
        self.aboutButton = Button(620, 412, 379, 105, pygame.image.load("istyping/images/credits_button.jpg"))
        self.bg = pygame.image.load("istyping/images/testbg.jpg")
          
#friendscreen class: holds UI and messages for friend dialogue
class FriendScreen:
    def __init__(self):
        self.name = "FRIEND"
        self.bg = pygame.image.load("istyping/images/text_screen_bg.jpg")
        self.prompt = pygame.image.load("istyping/images/prompt.jpg")

        global optionHigh
        global optionNeu
        global optionLow

        global receive_sound
        pygame.mixer.Sound.play(receive_sound)

        #generate a conversation 
        #(this structure was only completed for the friend, as I initially thought of providing the following message to gemini as well)
        self.conversation = [
            grammar.generate('S', friend.friend_grammar1),
            grammar.generate('S', friend.you_grammar1),
            grammar.generate('S', friend.friend_grammar2),
            grammar.generate('S', friend.you_grammar2),
            grammar.generate('S', friend.friend_grammar3),
            grammar.generate('S', friend.you_grammar3),
        ]

        #choose the right response depending on the friend's anxiousness characteristic
        if preferences.friend_anxiousness >= 50:
            self.conversation.append(grammar.generate('S-HIGH', friend.friend_grammar4))
        else:    
            self.conversation.append(grammar.generate('S-LOW', friend.friend_grammar4))
        
        self.conversation.append(grammar.generate('S', friend.you_grammar4))

        #setup the first messages to display
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
        self.prompt = pygame.image.load("istyping/images/prompt.jpg")

        global optionHigh
        global optionNeu
        global optionLow

        #setup the first messages to display
        grammar.processing = True
        optionNeu = grammar.generate('S', date.you_grammar1)
        optionHigh = grammar.get_prompt(self.currMessage, optionNeu, 'date', 'HIGH')
        optionLow = grammar.get_prompt(self.currMessage, optionNeu, 'date', 'LOW')

#bossscreen class: holds UI and messages for boss dialogue
class BossScreen:
    def __init__(self):
        self.name = "BOSS"
        self.currMessage = None
        self.prompt = pygame.image.load("istyping/images/prompt.jpg")

        #set up the first messages to display, based on the boss' professionalism characteristic
        if preferences.boss_professionalism >=50:
            self.currMessage = grammar.generate('S-PROF', boss.boss_grammar1)
        else:
            self.currMessage = grammar.generate('S-CASUAL', boss.boss_grammar1)
        self.bg = pygame.image.load("istyping/images/text_screen_bg.jpg")
        
        global receive_sound
        pygame.mixer.Sound.play(receive_sound)

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
        self.bg = pygame.image.load("istyping/images/tutorialbg.jpg")

#endscreen class: holds UI for end screen to show user's performance
class EndScreen:
    def __init__(self):
        self.homeButton = Button(547, 545, 224, 62,  pygame.image.load("istyping/images/home_button.png"))
        self.bg = pygame.image.load("istyping/images/end_bg.jpg")

#creditscreen class: holds UI for credit sscreen to show credits
class CreditScreen:
    def __init__(self):
        self.homeButton = Button(28, 18, 224, 62,  pygame.image.load("istyping/images/home_button.png"))
        self.bg = pygame.image.load("istyping/images/credits.jpg")

#transitionscreen class: holds UI for transitions between the characters to introduce them
class TransitionScreen:
    def __init__ (self, name):
        self.bg = pygame.image.load("istyping/images/transition_bg.jpg")
        self.name = name

#friendendscreen class: holds UI for the final message from the friend before the end screen
class FriendEndScreen:
    def __init__ (self):
        self.messageimg = pygame.image.load("istyping/images/friend_final_text.jpg")
        self.yPos = SCREEN_HEIGHT
        self.alpha = 0
        #generate the message based on friend's characteristic
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
                currScreen = CreditScreen()
                state = CREDITS

#text loop - used by the friend, date and boss screens to draw the UI
dotcount = 1
def textScreen():
    screen.fill((255,255,255))
    screen.blit(currScreen.bg.convert(), (0,0))

    #draw the visuals for the other speaker as needed 
    # (don't draw if it is the date's first message, which appears AFTER the user's first text)
    if state != DATE:
        screen.blit(GUI.profile_icon.convert(), (38,216))
        screen.blit(GUI.text_them.convert(), (155,151))
    else:
        if message_counter != 1:
            screen.blit(GUI.profile_icon.convert(), (38,216))
            screen.blit(GUI.text_them.convert(), (155,151))

    screen.blit(GUI.profile_icon.convert(), (1143,595))

    #set up the three text options and draw them
    global optionHigh, optionNeu, optionLow, arduino_countdown, display_countingdown

    #if the user is currently choosing a message, display an indicator for which message their pressure corresponds to
    if not display_countingdown:
        if analogPrinter.data > (1/3)*2:
            screen.blit(GUI.high_indic.convert(), (593,313))

        if (analogPrinter.data >= 1/3 and analogPrinter.data <= (1/3)*2):
            screen.blit(GUI.neutral_indic.convert(), (593,441))

        if  analogPrinter.data < 1/3:
            screen.blit(GUI.low_indic.convert(), (593,562))

    #y-positions of the start of the text box depending on how many lines there are
    #pygame does not support multi-line text, so these variables are used to properly create paragraphs blocks
    HIGH_4LINES_Y = 304
    HIGH_3LINES_Y = 314
    HIGH_2LINES_Y = 326
    HIGH_1LINE_Y = 337

    NEU_4LINES_Y = 433
    NEU_3LINES_Y = 441
    NEU_2LINES_Y = 453
    NEU_1LINE_Y = 462

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

    #format the texts to see how many lines are required
    global MAX_TEXT_LENGTH
    formattedHigh = grammar.format_text(optionHigh, MAX_TEXT_LENGTH)
    formattedNeu = grammar.format_text(optionNeu, MAX_TEXT_LENGTH)
    formattedLow = grammar.format_text(optionLow, MAX_TEXT_LENGTH)
    formattedThem = grammar.format_text(currScreen.currMessage, MAX_TEXT_LENGTH)

    #this displays the selected text after the countdown is over
    #displays a solid green text bubble, and the user's selected message
    global display_selected
    if not display_countingdown:
        screen.blit(GUI.thinking_you.convert(), (684,289))
        screen.blit(GUI.thinking_you.convert(), (684,417))
        screen.blit(GUI.thinking_you.convert(), (684,539))
    else:
        screen.blit(GUI.text_you.convert(), (684,539))
        if display_selected != None:
            formatted_selected = grammar.format_text(display_selected, MAX_TEXT_LENGTH)
            if len(formatted_selected) == 4:
                low_num_lines = LOW_4LINES_Y
                screen.blit(h4.render(formatted_selected[0], True, (255,255,255)), (708, low_num_lines))
                screen.blit(h4.render(formatted_selected[1], True, (255,255,255)), (708, low_num_lines+21))
                screen.blit(h4.render(formatted_selected[2], True, (255,255,255)), (708, low_num_lines+42))
                screen.blit(h4.render(formatted_selected[3], True, (255,255,255)), (708, low_num_lines+63))
            elif len(formatted_selected) == 3: #3 lines
                low_num_lines = LOW_3LINES_Y
                screen.blit(h4.render(formatted_selected[0], True, (255,255,255)), (708, low_num_lines))
                screen.blit(h4.render(formatted_selected[1], True, (255,255,255)), (708, low_num_lines+24))
                screen.blit(h4.render(formatted_selected[2], True, (255,255,255)), (708, low_num_lines+48))
            elif len(formatted_selected) == 2: #2 lines
                low_num_lines = LOW_2LINES_Y
                screen.blit(h4.render(formatted_selected[0], True, (255,255,255)), (708, low_num_lines))
                screen.blit(h4.render(formatted_selected[1], True, (255,255,255)), (708, low_num_lines+24))
            elif len(formattedLow) == 1: #1 line
                low_num_lines = LOW_1LINE_Y
                screen.blit(h4.render(formatted_selected[0], True, (255,255,255)), (708, low_num_lines))
            else:
                low_num_lines = LOW_1LINE_Y
                screen.blit(h4.render("Error: Line Too Long", True, (255,255,255)), (708, low_num_lines))


    #for each of the options, check how many lines they need and display as needed
    if not display_countingdown:

        #high option
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

        #neutral option
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

        #low option
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
    
    #the other person's text
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
        if state != DATE:
            them_num_lines = THEM_1LINE_Y 
            screen.blit(h4.render("Error: Line Too Long", True, (0,0,0)), (215, them_num_lines))
        else:
            if message_counter !=1:
                them_num_lines = THEM_1LINE_Y 
                screen.blit(h4.render("Error: Line Too Long", True, (0,0,0)), (215, them_num_lines))
                


    #rendering the countdown and the other person's name
    screen.blit(name_header.render(currSpeaker, True, (0,0,0)), (575, 24))
    if not display_countingdown:
        screen.blit(h2.render(str(arduino_countdown), True, (0,0,0)), (875, 215))

    #referenced countdown arc from: https://stackoverflow.com/questions/67168804/how-to-make-a-circular-countdown-timer-in-pygame
    percentage = (arduino_countdown*11)/100
    end_angle = 2 * math.pi * percentage
    pygame.draw.arc(window, (100, 100, 100), pygame.Rect(854, 200, 64, 64), 0, end_angle, 4)

    #show the prompt for the user to use the pressure sensor
    if arduino_countdown > 0:
        global dotcount
        if dotcount == 1:
            dots = "."
        elif dotcount == 2:
            dots = ".."
        else:
            dots = "..."
        screen.blit(currScreen.prompt.convert(), (56,570))
        screen.blit(prompt_font.render(dots, True, (255,255,255)), (200, 547))

    #nested method for retrieving messages from grammar sets/Gemini API
    def get_messages():
        global message_counter, optionNeu, optionHigh, optionLow, state, currScreen, currSpeaker, arduino_countdown, countingdown, selected, receive_sound
        #update the current message in the conversation and start counting down
        message_counter+=1
        countingdown = True

        #processing is used to limit the calls to the gemini api, so it is not called repeatedly
        grammar.processing = True

        #generate messages depending on the current speaker, and determine the set based on the message number
        if state == FRIEND:
            if(message_counter == 2):
                #branch: if the user selected a high message, generate a different variation of the friend's message
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
                pygame.mixer.Sound.play(receive_sound)
            elif(message_counter == 3):
                currScreen.currMessage = currScreen.conversation[4] #grammar.generate('S', friend.friend_grammar3)
                optionNeu = currScreen.conversation[5]#grammar.generate('S', friend.you_grammar3)
                optionHigh = grammar.get_prompt(currScreen.currMessage, optionNeu, currSpeaker, 'HIGH')
                optionLow = grammar.get_prompt(currScreen.currMessage, optionNeu, currSpeaker, 'LOW')

                friend.friend_responded = selected
                pygame.mixer.Sound.play(receive_sound)

            elif(message_counter == 4):
                currScreen.currMessage = currScreen.conversation[6]

                optionNeu = currScreen.conversation[7]#grammar.generate('S', friend.you_grammar4)
                optionHigh = grammar.get_prompt(currScreen.currMessage, optionNeu, currSpeaker, 'HIGH')
                optionLow = grammar.get_prompt(currScreen.currMessage, optionNeu, currSpeaker, 'LOW')
                pygame.mixer.Sound.play(receive_sound)

                # if preferences.friend_anxiousness >= 50:
                #     currScreen.currMessage = grammar.generate('S-HIGH', friend.friend_grammar4)
                # else:    
                #     currScreen.currMessage = grammar.generate('S-LOW', friend.friend_grammar4)
            else:
                message_counter = 1
                if fader.fading == None:
                    fader.next()
        elif state == DATE:
            if(message_counter == 2):
                optionNeu = grammar.generate('S', date.you_grammar2)
                optionHigh = grammar.get_prompt(currScreen.currMessage, optionNeu, currSpeaker, 'HIGH')
                optionLow = grammar.get_prompt(currScreen.currMessage, optionNeu, currSpeaker, 'LOW')
                
                #branch: if the date is eager, generate a different variation of the date's message
                if preferences.date_eagerness >= 50:
                    currScreen.currMessage = grammar.generate('S-EAGER', date.date_grammar1)
                else:
                    currScreen.currMessage = grammar.generate('S-UNINTERESTED', date.date_grammar1)

                pygame.mixer.Sound.play(receive_sound)

            elif(message_counter == 3):
                optionNeu = grammar.generate('S', date.you_grammar3)
                optionHigh = grammar.get_prompt(currScreen.currMessage, optionNeu, currSpeaker, 'HIGH')
                optionLow = grammar.get_prompt(currScreen.currMessage, optionNeu, currSpeaker, 'LOW')
                    
                #branch: if the date is eager, generate a different variation of the date's message
                if preferences.date_eagerness >= 50:
                    currScreen.currMessage = grammar.generate('S-EAGER', date.date_grammar2)
                else:
                    currScreen.currMessage = grammar.generate('S-UNINTERESTED', date.date_grammar2)
                
                pygame.mixer.Sound.play(receive_sound)

            elif(message_counter == 4):
                optionNeu = grammar.generate('S', date.you_grammar4)
                optionHigh = grammar.get_prompt(currScreen.currMessage, optionNeu, currSpeaker, 'HIGH')
                optionLow = grammar.get_prompt(currScreen.currMessage, optionNeu, currSpeaker, 'LOW')

                #branch: if the date is eager, generate a different variation of the date's message
                if preferences.date_eagerness >= 50:
                    currScreen.currMessage = grammar.generate('S-EAGER', date.date_grammar3)
                else:
                    currScreen.currMessage = grammar.generate('S-UNINTERESTED', date.date_grammar3)
                pygame.mixer.Sound.play(receive_sound)
            else:
                message_counter = 1
                if fader.fading == None:
                    fader.next()
        elif state == BOSS:
            if(message_counter == 2):
                optionNeu = grammar.generate('S', boss.you_grammar2)
                optionHigh = grammar.get_prompt(currScreen.currMessage, optionNeu, currSpeaker, 'HIGH')
                optionLow = grammar.get_prompt(currScreen.currMessage, optionNeu, currSpeaker, 'LOW')

                #branch: if the boss is professional, generate a different variation of the boss's message
                if preferences.boss_professionalism >=50:
                    currScreen.currMessage = grammar.generate('S-PROF', boss.boss_grammar2)
                else:
                    currScreen.currMessage = grammar.generate('S-CASUAL', boss.boss_grammar2)
                pygame.mixer.Sound.play(receive_sound)
            elif(message_counter == 3):

                #branch: if the boss is professional, generate a different variation of the boss's message
                if preferences.boss_professionalism >=50:
                    currScreen.currMessage = grammar.generate('S-PROF', boss.boss_grammar3)
                    optionNeu = grammar.generate('S-PROF', boss.you_grammar3)
                else:
                    currScreen.currMessage = grammar.generate('S-CASUAL', boss.boss_grammar3)      
                    optionNeu = grammar.generate('S-CASUAL', boss.you_grammar3) 
                optionHigh = grammar.get_prompt(currScreen.currMessage, optionNeu, currSpeaker, 'HIGH')
                optionLow = grammar.get_prompt(currScreen.currMessage, optionNeu, currSpeaker, 'LOW')  
                pygame.mixer.Sound.play(receive_sound)   
            elif(message_counter == 4):
                boss.responded = selected
                optionNeu = grammar.generate('S', boss.you_grammar4)
                optionHigh = grammar.get_prompt(currScreen.currMessage, optionNeu, currSpeaker, 'HIGH')
                optionLow = grammar.get_prompt(currScreen.currMessage, optionNeu, currSpeaker, 'LOW')

                #branch: if the boss is professional, generate a different variation of the boss's message
                if preferences.boss_professionalism >=50:
                    currScreen.currMessage = grammar.generate('S-PROF', boss.boss_grammar4)
                else:
                    currScreen.currMessage = grammar.generate('S-CASUAL', boss.boss_grammar4)
                pygame.mixer.Sound.play(receive_sound)
            elif(message_counter == 5):

                #branch: depending on the user's message choice, generate a different variation of the boss's message
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
                pygame.mixer.Sound.play(receive_sound)
            else:
                message_counter = 1
                if fader.fading == None:
                    fader.next()
            
    #event handlers
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #exit button
           global run
           run = False
        elif event.type == TIMEREVENT: #called each 1000ms (1s)
            global countingdown, display_countdown, selected

            #counting down for time to select message
            if countingdown:
                if arduino_countdown > 0:
                    arduino_countdown -= 1

                    #update prompt animation
                    if dotcount < 3:
                        dotcount+=1
                    else:
                        dotcount = 1

                    if arduino_countdown < 3:
                        global countdown_tick
                        pygame.mixer.Sound.play(countdown_tick)
                else:
                    if not display_countingdown:
                        global sent_sound
                        pygame.mixer.Sound.play(sent_sound)

                        #saving which message was selected, add it to the user's performance calculation
                        display_countingdown = True
                        if state == FRIEND or state == DATE:
                            if message_counter <= 4:
                                if analogPrinter.data > (1/3)*2:
                                    selected = HIGH
                                    display_selected = optionHigh
                                elif (analogPrinter.data >= 1/3 and analogPrinter.data <= (1/3)*2):
                                    selected = NEUTRAL
                                    display_selected = optionNeu
                                elif analogPrinter.data < 1/3:
                                    selected = LOW
                                    display_selected = optionLow
                            if state == FRIEND:
                                preferences.check_friend(selected)
                            elif state == DATE:
                                preferences.check_date(selected)
                        elif state == BOSS:
                            if message_counter <= 5:
                                if analogPrinter.data > (1/3)*2:
                                    selected = HIGH
                                    display_selected = optionHigh
                                elif (analogPrinter.data >= 1/3 and analogPrinter.data <= (1/3)*2):
                                    selected = NEUTRAL
                                    display_selected = optionNeu
                                elif analogPrinter.data < 1/3:
                                    selected = LOW
                                    display_selected = optionLow
                                preferences.check_boss(selected)
                    elif display_countingdown and display_countdown > 0:
                        display_countdown -=1 #show the selected message for a few seconds
                    else:
                        #only reset the countdown variables if it's not the last message for the character
                        if ((state == FRIEND or state == DATE) and message_counter < 4) or (state == BOSS and message_counter < 5):
                            arduino_countdown = COUNTDOWN 
                            countingdown = False
                            display_countingdown = False
                            display_countdown = DISPLAY_COUNTDOWN
                            display_selected = None
                            
                        if fader.fading == None:
                            if state == FRIEND or state == DATE:
                                if message_counter <= 4:
                                    get_messages()
                            elif state == BOSS:
                                if message_counter <= 5:
                                    get_messages()
                        print(selected)  

#tutorial screen loop - displays the tutorial + buttons
def tutScreen():
    screen.fill((255,255,255))
    
    global currScreen, state

    #draw background
    screen.blit(currScreen.bg.convert(), (0,0))

    #draw buttons
    backButton = currScreen.backButton
    nextButton = currScreen.nextButton

    backButton.draw()
    nextButton.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT: #exit button
            global run
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN: #mouse click
            global fader
            if fader.fading == None:
                #navigate to next screen based on button pressed
                pos = pygame.mouse.get_pos()
                if(backButton.checkMousePress(pos[0], pos[1])):
                    state = MAIN
                    currScreen = HomeScreen()
                elif(nextButton.checkMousePress(pos[0], pos[1])):
                    if fader.fading == None:
                        fader.next()

#handles the end screen, showing the user's performance and character's preferences      
def endScreen():
    screen.fill((255,255,255))

    global currScreen, state

    #draw UI
    screen.blit(currScreen.bg, (0,0))
    homeButton = currScreen.homeButton

    homeButton.draw()

    #write each of the preferences + user's performance in simple language
    screen.blit(h3.render("The friend...", True, (0,0,0)), (279, 310))
    screen.blit(h5.render(preferences.get_friend() + ", they liked the tone of " + preferences.get_friend_score() + " of your messages", True, (0,0,0)), (410, 310))
    screen.blit(h3.render("The date...", True, (0,0,0)), (279, 345))
    screen.blit(h5.render(preferences.get_date() + ", they liked the tone of " + preferences.get_date_score() + " of your messages", True, (0,0,0)), (400, 345))
    screen.blit(h3.render("The boss...", True, (0,0,0)), (279, 380))
    screen.blit(h5.render(preferences.get_boss() + ", they liked the tone of " + preferences.get_boss_score() + " of your messages", True, (0,0,0)), (400, 380))
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #exit button
            global run
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN: #mouse click
            pos = pygame.mouse.get_pos()
            #return home
            if(homeButton.checkMousePress(pos[0], pos[1])):
                state = MAIN
                currScreen = HomeScreen()

#credits screen, accessible from home page
def creditsLoop():
    screen.fill((255,255,255))
    
    global currScreen, state

    #draw background and button
    screen.blit(currScreen.bg.convert(), (0,0))

    homeButton = currScreen.homeButton

    homeButton.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT: #exit button
            global run
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN: #mouse click
            global fader
            if fader.fading == None:
                pos = pygame.mouse.get_pos()
                #return home
                if(homeButton.checkMousePress(pos[0], pos[1])):
                    state = MAIN
                    currScreen = HomeScreen()

# global variables to keep track of current state of the transition screen
alpha = 0
name_pos = -200
showName = False
done = False
stay_on_screen = 4

#used to draw the transition screens which introduce the next character
def transitionLoop():
    screen.fill((255,255,255))

    global currScreen, alpha, showName, name_pos, done, stay_on_screen 
    #referenced transparency from: https://www.youtube.com/watch?v=8_HVdxBqJmE
    bg = currScreen.bg.copy()

    #fade in the background
    if alpha < 255 and not done:
        alpha+=10
    else:
        showName = True
        alpha = 255
    bg.set_alpha(alpha)
    screen.blit(bg, (0,0))

    #translate the name from left->center of screen
    if showName:
        if name_pos < 450:
            name_pos+=15
        else:
            showName = False
            done = True   
        screen.blit(transition_font.render(currScreen.name, True, (0,0,0)), (name_pos, 281))

    #resetting variables once the countdown is over
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
        elif event.type == TIMEREVENT: #runs every 1000ms (1s)
            #once the transition is shown, fade to next scene
            if fader.fading == None and stay_on_screen < 4:
                fader.next()
            #countdown of duration to display the completed animation on screen
            if done and stay_on_screen > 0:
                stay_on_screen -= 1

#global variable for duration of displaying the friend's last text screen
stay_on_screen2 = 10

#friend end loop shows a short animation to wrap up the narrative, of the friend's last check-in text.
def friendEndLoop():
    screen.fill((255,255,255))

    #animate the message background upwards and fading in
    global currScreen, stay_on_screen2
    if currScreen.yPos > 253:
        currScreen.yPos-=10
    else:
        currScreen.yPos = 253
    
    if currScreen.yPos < 350:
        currScreen.alpha += 3

    currScreen.messageimg.set_alpha(currScreen.alpha)
    screen.blit(currScreen.messageimg, (265,currScreen.yPos))

    #format the text message to fit in the notification popup
    START_POINT = 327
    MAX_LENGTH = 37

    formatted_message = grammar.format_text(currScreen.text, MAX_LENGTH)

    #display the text based on the number of lines required
    if currScreen.yPos >=253 and currScreen.alpha > 25:
        if len(formatted_message) == 3: #3 lines
            screen.blit(h1.render(formatted_message[0], True, (0,0,0)), (495, START_POINT))
            screen.blit(h1.render(formatted_message[1], True, (0,0,0)), (495, START_POINT+40))
            screen.blit(h1.render(formatted_message[2], True, (0,0,0)), (495, START_POINT+80))
        elif len(formatted_message) == 2: #2 lines
            screen.blit(h1.render(formatted_message[0], True, (0,0,0)), (495, START_POINT))
            screen.blit(h1.render(formatted_message[1], True, (0,0,0)), (495, START_POINT+40))
        elif len(formatted_message) == 1: #1 line
            screen.blit(h1.render(formatted_message[0], True, (0,0,0)), (495, START_POINT))
        else:
            screen.blit(h1.render("Error: Message too long", True, (0,0,0)), (495, START_POINT))

    if stay_on_screen2 == 0:
        stay_on_screen2 = 10
    
    #event handlers
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #exit the window
            global run
            run = False 
        elif event.type == TIMEREVENT:
            #once the animation is done displaying, start fading to next screen
            if fader.fading == None and stay_on_screen2 < 4:
                fader.next()
            #counting down the duration to stay on screen
            if stay_on_screen2 > 0:
                stay_on_screen2 -= 1
          

#core loop to run the program
while run:
    #short delay so system isn't overwhelmed
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
    elif state == CREDITS:
        creditsLoop()

    #used to control the fade-to-black object
    if fader.fading != None:
        fader.draw()

    #updates screen to display objects
    pygame.display.update()
    
#exits window once the run loop ends, stopping arduino reads and quitting pygame window
analogPrinter.stop()
pygame.quit()
import pygame #used this video to review pygame basics: https://www.youtube.com/watch?v=y9VG3Pztok8

#referenced this link to import my own classes: https://csatlas.com/python-import-file-module/
#import UI.GUI as GUI
import GrammarSets.grammarprocessing as grammar
import GrammarSets.friend as friend
import GrammarSets.date as date
import GrammarSets.boss as boss
import GrammarSets.preferences as preferences

#import arduniohandler as Arduino
#import time

# import google.generativeai as genai
# import env

# key = env.gemini
# genai.configure(api_key=key)

# try:
#     # Test a simple query
#     model = genai.GenerativeModel('gemini-2.0-flash')
#     response = model.generate_content("Write a haiku about artificial intelligence")

#     print("API Connection Successful!")
#     print("\nHaiku response:")
#     print(response.text)
# except Exception as e:
#     print(f"Error connecting to API: {e}")
#     print("\nPlease check your API key configuration and try again.")


#referenced this for classes: https://www.w3schools.com/python/python_classes.asp

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
        if mouseX > self.xPos-self.width/2 and mouseX < self.xPos + self.width/2 and mouseY > self.yPos-self.width/2 and mouseY < self.yPos + self.height/2:
            return True

    #renders visual onto the screen
    def draw(self):
         pygame.draw.rect(screen, self.color, self.visual, 0, 10)     

#initialize/setup pygame
pygame.init()
pygame.display.set_caption("is-typing")

#intiliaze fonts
pygame.font.init()
font_path = pygame.font.match_font("verdana")
h1 = pygame.font.Font(font_path, 32)
h2 = pygame.font.Font(font_path, 16)
h3 = pygame.font.Font(font_path, 10)

#states for FSM
MAIN = 0
INTRO = 1
FRIEND = 2
DATE = 3
BOSS = 4
END = 5

state = MAIN
run = True

#current speaker to give to Gemini API for context
currSpeaker = ""

#variables to keep track of which option was selected by the user
optionHigh = "Anxious Response!"
optionNeu = "Neutral Response!"
optionLow = "Lowkey Response!"

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

# # Let's create an instance
# analogPrinter = Arduino.AnalogPrinter()

# # and start DAQ
# analogPrinter.start()

# # let's acquire data for 10secs. We could do something else but we just sleep!
# time.sleep(10)

# # let's stop it
# analogPrinter.stop()

#print("finished")

#homescreen class: holds UI for homescreen
class HomeScreen:
    def __init__(self):
        self.startButton = Button(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 250, 75,  pygame.Rect(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 250, 75), (0,255,0), h1.render('Start', False, (0,0,0)))
        self.aboutButton = Button(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 125, 250, 75, pygame.Rect(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 125, 250, 75), (200,200,200), h1.render('About', False, (0,0,0)))
        self.bg = pygame.image.load("istyping/images/testbg.jpg")
          
#friendscreen class: holds UI and messages for friend dialogue
class FriendScreen:
    def __init__(self):
        self.test = pygame.Rect(100, 100, 250, 75)
        self.name = "FRIEND"
        self.currMessage = grammar.generate('S', friend.friend_grammar1)
        self.text = h1.render(self.currMessage, True, (0,0,0))
        self.posButton = Button(SCREEN_WIDTH-225, SCREEN_HEIGHT-200, 250, 40,  pygame.Rect(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 250, 40), (0,255,0), h1.render('Start', False, (0,0,0)))
        self.neuButton = Button(SCREEN_WIDTH-225, SCREEN_HEIGHT-150, 250, 40,  pygame.Rect(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 250, 40), (0,255,0), h1.render('Start', False, (0,0,0)))
        self.negButton = Button(SCREEN_WIDTH-225, SCREEN_HEIGHT-100, 250, 40,  pygame.Rect(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 250, 40), (0,255,0), h1.render('Start', False, (0,0,0)))
        
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
        self.test = pygame.Rect(100, 100, 250, 75)
        self.name = "DATE"
        self.currMessage = ""
        self.text = h1.render(self.currMessage, True, (0,0,0))
        self.posButton = Button(SCREEN_WIDTH-225, SCREEN_HEIGHT-200, 250, 40,  pygame.Rect(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 250, 40), (0,255,0), h1.render('Start', False, (0,0,0)))
        self.neuButton = Button(SCREEN_WIDTH-225, SCREEN_HEIGHT-150, 250, 40,  pygame.Rect(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 250, 40), (0,255,0), h1.render('Start', False, (0,0,0)))
        self.negButton = Button(SCREEN_WIDTH-225, SCREEN_HEIGHT-100, 250, 40,  pygame.Rect(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 250, 40), (0,255,0), h1.render('Start', False, (0,0,0)))
        
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
        self.test = pygame.Rect(100, 100, 250, 75)
        self.name = "BOSS"
        self.currMessage = grammar.generate('S', boss.boss_grammar1)
        self.text = h1.render(self.currMessage, True, (0,0,0))
        self.posButton = Button(SCREEN_WIDTH-225, SCREEN_HEIGHT-200, 250, 40,  pygame.Rect(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 250, 40), (0,255,0), h1.render('Start', False, (0,0,0)))
        self.neuButton = Button(SCREEN_WIDTH-225, SCREEN_HEIGHT-150, 250, 40,  pygame.Rect(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 250, 40), (0,255,0), h1.render('Start', False, (0,0,0)))
        self.negButton = Button(SCREEN_WIDTH-225, SCREEN_HEIGHT-100, 250, 40,  pygame.Rect(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 250, 40), (0,255,0), h1.render('Start', False, (0,0,0)))
        
        global optionHigh
        global optionNeu
        global optionLow

        grammar.processing = True
        optionNeu = grammar.generate('S', boss.you_grammar1)
        optionHigh = grammar.get_prompt(self.currMessage, optionNeu, 'boss', 'HIGH')
        optionLow = grammar.get_prompt(self.currMessage, optionNeu, 'boss', 'LOW')

#tutscreen class: holds UI for tutorial screen
class TutScreen:
    def __int__(self):
        self.test = pygame.Rect(100, 100, 250, 75)

#endscreen class: holds UI for end screen to show user's performance
class EndScreen:
    def __int__(self):
        self.test = pygame.Rect(100, 100, 250, 75)


#setup current screen, used to keep track alongside current state what is showing
currScreen = HomeScreen()

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
                preferences.setup()
                state = FRIEND      
                global currSpeaker 
                currSpeaker = "friend"
                currScreen = FriendScreen()
            elif(aboutButton.checkMousePress(pos[0], pos[1])):
                print("about!")  

#text loop - used by the friend, date and boss screens to draw the UI
def textScreen():
    screen.fill((255,255,255))
    pygame.draw.rect(screen, (0,255,0), currScreen.test)
    screen.blit(currScreen.text, currScreen.test)

    #set up the three text options and draw them
    global optionHigh, optionNeu, optionLow

    posButton = currScreen.posButton
    neuButton = currScreen.neuButton
    negButton = currScreen.negButton

    posButton.draw()
    neuButton.draw()
    negButton.draw()

    screen.blit(h3.render(optionLow, True, (0,0,0)), (SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 250))
    screen.blit(h3.render(optionNeu, True, (0,0,0)), (SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 200))
    screen.blit(h3.render(optionHigh, True, (0,0,0)), (SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 150))
    screen.blit(h2.render(currSpeaker, True, (0,0,0)), (20, 20))

    #nested method for retrieving messages from grammar sets/Gemini API
    def get_messages():
        global message_counter, optionNeu, optionHigh, optionLow, state, currScreen, currSpeaker
        message_counter+=1
        grammar.processing = True

        #generate messages depending on the current speaker, and determine the set based on the message number
        if state == FRIEND:
            if(message_counter == 2):
                optionNeu = grammar.generate('S', friend.you_grammar2)
                optionHigh = grammar.get_prompt(currScreen.currMessage, optionNeu, currSpeaker, 'HIGH')
                optionLow = grammar.get_prompt(currScreen.currMessage, optionNeu, currSpeaker, 'LOW')
                currScreen.currMessage = grammar.generate('S', friend.friend_grammar2)
                currScreen.text = h1.render(currScreen.currMessage, True, (0,0,0))
            elif(message_counter == 3):
                optionNeu = grammar.generate('S', friend.you_grammar3)
                optionHigh = grammar.get_prompt(currScreen.currMessage, optionNeu, currSpeaker, 'HIGH')
                optionLow = grammar.get_prompt(currScreen.currMessage, optionNeu, currSpeaker, 'LOW')
                currScreen.currMessage = grammar.generate('S', friend.friend_grammar3)
                currScreen.text = h1.render(currScreen.currMessage, True, (0,0,0))
            elif(message_counter == 4):
                optionNeu = grammar.generate('S', friend.you_grammar4)
                optionHigh = grammar.get_prompt(currScreen.currMessage, optionNeu, currSpeaker, 'HIGH')
                optionLow = grammar.get_prompt(currScreen.currMessage, optionNeu, currSpeaker, 'LOW')
                currScreen.currMessage = grammar.generate('S', friend.friend_grammar4)
                currScreen.text = h1.render(currScreen.currMessage, True, (0,0,0))
            else:
                message_counter = 1
                state = DATE
                currSpeaker = "date"
                currScreen = DateScreen()
        elif state == DATE:
            if(message_counter == 2):
                optionNeu = grammar.generate('S', date.you_grammar2)
                optionHigh = grammar.get_prompt(currScreen.currMessage, optionNeu, currSpeaker, 'HIGH')
                optionLow = grammar.get_prompt(currScreen.currMessage, optionNeu, currSpeaker, 'LOW')
                currScreen.currMessage = grammar.generate('S', date.date_grammar1)
                currScreen.text = h1.render(currScreen.currMessage, True, (0,0,0))
            elif(message_counter == 3):
                optionNeu = grammar.generate('S', date.you_grammar3)
                optionHigh = grammar.get_prompt(currScreen.currMessage, optionNeu, currSpeaker, 'HIGH')
                optionLow = grammar.get_prompt(currScreen.currMessage, optionNeu, currSpeaker, 'LOW')
                currScreen.currMessage = grammar.generate('S', date.date_grammar2)
                currScreen.text = h1.render(currScreen.currMessage, True, (0,0,0))
            elif(message_counter == 4):
                optionNeu = grammar.generate('S', date.you_grammar4)
                optionHigh = grammar.get_prompt(currScreen.currMessage, optionNeu, currSpeaker, 'HIGH')
                optionLow = grammar.get_prompt(currScreen.currMessage, optionNeu, currSpeaker, 'LOW')
                currScreen.currMessage = grammar.generate('S', date.date_grammar3)
                currScreen.text = h1.render(currScreen.currMessage, True, (0,0,0))
            else:
                message_counter = 1
                state = BOSS
                currSpeaker = "boss"
                currScreen = BossScreen()
        elif state == BOSS:
            if(message_counter == 2):
                optionNeu = grammar.generate('S', boss.you_grammar2)
                optionHigh = grammar.get_prompt(currScreen.currMessage, optionNeu, currSpeaker, 'HIGH')
                optionLow = grammar.get_prompt(currScreen.currMessage, optionNeu, currSpeaker, 'LOW')
                currScreen.currMessage = grammar.generate('S', boss.boss_grammar2)
                currScreen.text = h1.render(currScreen.currMessage, True, (0,0,0))
            elif(message_counter == 3):
                optionNeu = grammar.generate('S', boss.you_grammar3)
                optionHigh = grammar.get_prompt(currScreen.currMessage, optionNeu, currSpeaker, 'HIGH')
                optionLow = grammar.get_prompt(currScreen.currMessage, optionNeu, currSpeaker, 'LOW')
                currScreen.currMessage = grammar.generate('S', boss.boss_grammar3)
                currScreen.text = h1.render(currScreen.currMessage, True, (0,0,0))
            elif(message_counter == 4):
                optionNeu = grammar.generate('S', boss.you_grammar4)
                optionHigh = grammar.get_prompt(currScreen.currMessage, optionNeu, currSpeaker, 'HIGH')
                optionLow = grammar.get_prompt(currScreen.currMessage, optionNeu, currSpeaker, 'LOW')
                currScreen.currMessage = grammar.generate('S', boss.boss_grammar4)
                currScreen.text = h1.render(currScreen.currMessage, True, (0,0,0))
            elif(message_counter == 5):
                optionNeu = grammar.generate('S', boss.you_grammar5)
                optionHigh = grammar.get_prompt(currScreen.currMessage, optionNeu, currSpeaker, 'HIGH')
                optionLow = grammar.get_prompt(currScreen.currMessage, optionNeu, currSpeaker, 'LOW')
                currScreen.currMessage = grammar.generate('S', boss.boss_grammar5)
                currScreen.text = h1.render(currScreen.currMessage, True, (0,0,0))
            else:
                message_counter = 1
                state = END
                currScreen = EndScreen()
            
    #event handlers
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #exit button
           global run
           run = False
        elif event.type == pygame.MOUSEBUTTONDOWN: #mouse click
            pos = pygame.mouse.get_pos()

            global selected
            
            if state == FRIEND or state == DATE:
                if message_counter <= 4:
                    if(posButton.checkMousePress(pos[0], pos[1])):
                        selected = HIGH
                        get_messages()
                    elif(neuButton.checkMousePress(pos[0], pos[1])):
                        selected = NEUTRAL
                        get_messages()
                    elif(negButton.checkMousePress(pos[0], pos[1])):
                        selected = LOW
                        get_messages()
            elif state == BOSS:
                if message_counter <= 5:
                    if(posButton.checkMousePress(pos[0], pos[1])):
                        selected = HIGH
                        get_messages()
                    elif(neuButton.checkMousePress(pos[0], pos[1])):
                        selected = NEUTRAL
                        get_messages()
                    elif(negButton.checkMousePress(pos[0], pos[1])):
                        selected = LOW
                        get_messages()


#core loop to run the program
while run:

    #show current screen based on state
    if state == MAIN:
        mainLoop()
    elif state == FRIEND:
        textScreen()
    elif state == DATE:
        textScreen()
    elif state == BOSS:
        textScreen()
    
    #clear screen with each iteration

    #pygame.draw.rect(screen, (0,255,0), player)
    #key = pygame.key.get_pressed()

    #updates screen to display objects
    pygame.display.update()

#exits window once the run loop ends
pygame.quit()
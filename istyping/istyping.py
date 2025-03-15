import pygame #used this video to review pygame basics: https://www.youtube.com/watch?v=y9VG3Pztok8

#referenced this link to import my own classes: https://csatlas.com/python-import-file-module/
#import UI.GUI as GUI
import GrammarSets.grammarprocessing as grammar
import GrammarSets.friend as friend

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

    
    def checkMousePress(self, mouseX, mouseY):
        if mouseX > self.xPos-self.width/2 and mouseX < self.xPos + self.width/2 and mouseY > self.yPos-self.width/2 and mouseY < self.yPos + self.height/2:
            return True
        
    def draw(self):
         pygame.draw.rect(screen, self.color, self.visual, 0, 10)     

#initialize/setup pygame
pygame.init()
pygame.display.set_caption("is-typing")

pygame.font.init()
font_path = pygame.font.match_font("verdana")
h1 = pygame.font.Font(font_path, 32)
h2 = pygame.font.Font(font_path, 16)
h3 = pygame.font.Font(font_path, 10)


MAIN = 0
FRIEND = 1

state = MAIN
run = True

optionNeg = "Bad!"
optionNeu = "Meh!"
optionPos = "Good!"

NEGATIVE = 0
NEUTRAL = 1
POSITIVE = 2

message_counter = 1
selected = -1

#setup the window
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((1920,1080))
resized_screen = pygame.transform.scale(screen, (SCREEN_WIDTH, SCREEN_HEIGHT))

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
window.blit(resized_screen, (0,0))




# print("Generated sentences:\n")
# for i in range(5):
#     sent = grammar.generate('S', friend.friend_grammar1)
#     print(grammar.format_sentence(sent))


# # Let's create an instance
# analogPrinter = Arduino.AnalogPrinter()

# # and start DAQ
# analogPrinter.start()

# # let's acquire data for 10secs. We could do something else but we just sleep!
# time.sleep(10)

# # let's stop it
# analogPrinter.stop()

#print("finished")

class HomeScreen:
    def __init__(self):
        self.startButton = Button(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 250, 75,  pygame.Rect(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 250, 75), (0,255,0), h1.render('Start', False, (0,0,0)))
        self.aboutButton = Button(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 125, 250, 75, pygame.Rect(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 125, 250, 75), (200,200,200), h1.render('About', False, (0,0,0)))
        self.bg = pygame.image.load("istyping/images/testbg.jpg")
          
class FriendScreen:
    def __init__(self):
        self.test = pygame.Rect(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 250, 75)
        self.name = "FRIEND"
        self.text = h1.render(grammar.generate('S', friend.friend_grammar1), True, (0,0,0))
        self.posButton = Button(SCREEN_WIDTH-225, SCREEN_HEIGHT-200, 250, 40,  pygame.Rect(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 250, 40), (0,255,0), h1.render('Start', False, (0,0,0)))
        self.neuButton = Button(SCREEN_WIDTH-225, SCREEN_HEIGHT-150, 250, 40,  pygame.Rect(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 250, 40), (0,255,0), h1.render('Start', False, (0,0,0)))
        self.negButton = Button(SCREEN_WIDTH-225, SCREEN_HEIGHT-100, 250, 40,  pygame.Rect(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 250, 40), (0,255,0), h1.render('Start', False, (0,0,0)))
        
        global optionPos
        global optionNeu
        global optionNeg

        optionPos = grammar.generate('S', friend.you_grammar1)
        optionNeu = grammar.generate('S', friend.you_grammar1)
        optionNeg = grammar.generate('S', friend.you_grammar1)


#setup current screen
currScreen = HomeScreen()

def mainLoop():
    global currScreen
    global state

    screen.blit(currScreen.bg.convert(), (0,0))

    startButton = currScreen.startButton
    aboutButton = currScreen.aboutButton


    # pygame.draw.rect(screen, startButton.color, startButton.visual, 0, 10)     
    # pygame.draw.rect(screen, aboutButton.color, aboutButton.visual, 0, 10)   
    startButton.draw()
    aboutButton.draw()

    screen.blit(startButton.text, (startButton.xPos-startButton.width/4, startButton.yPos-startButton.height/4))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           global run
           run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if(startButton.checkMousePress(pos[0], pos[1])):
                print("start!")
                state = FRIEND       
                currScreen = FriendScreen()
            
            elif(aboutButton.checkMousePress(pos[0], pos[1])):
                print("about!")  

def textScreen():
    screen.fill((255,255,255))
    pygame.draw.rect(screen, (0,255,0), currScreen.test)
    screen.blit(currScreen.text, currScreen.test)

    global optionPos, optionNeu, optionNeg

    posButton = currScreen.posButton
    neuButton = currScreen.neuButton
    negButton = currScreen.negButton

    posButton.draw()
    neuButton.draw()
    negButton.draw()

    screen.blit(h3.render(optionNeg, True, (0,0,0)), (negButton.xPos, negButton.yPos))
    screen.blit(h3.render(optionNeu, True, (0,0,0)), (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 150))
    screen.blit(h3.render(optionPos, True, (0,0,0)), (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           global run
           run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            global selected
            global message_counter

            if(posButton.checkMousePress(pos[0], pos[1])):
                selected = POSITIVE
            elif(neuButton.checkMousePress(pos[0], pos[1])):
                selected = NEUTRAL
            elif(negButton.checkMousePress(pos[0], pos[1])):
                selected = NEGATIVE
            
            message_counter+=1
            if(message_counter == 2):
                currScreen.text = h1.render(grammar.generate('S', friend.friend_grammar2), True, (0,0,0))
                optionNeu = grammar.generate('S', friend.you_grammar2)

           
            


#core loop to run the program

while run:

    #show current screen based on state
    if state == MAIN:
        mainLoop()
    elif state == FRIEND:
        textScreen()
    
    #clear screen with each iteration

    #pygame.draw.rect(screen, (0,255,0), player)
    #key = pygame.key.get_pressed()

    #updates screen to display objects
    pygame.display.update()

pygame.quit()
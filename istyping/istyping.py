import pygame #used this video to review pygame basics: https://www.youtube.com/watch?v=y9VG3Pztok8

#referenced this link to import my own classes: https://csatlas.com/python-import-file-module/
#import UI.GUI as GUI

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


starting_grammar = {
    'S': [['I', 'to', 'is-typing']],
    'I': ['Hello', 'Hey', 'Welcome', 'Hi'],
}

#initialize/setup pygame
pygame.init()
pygame.display.set_caption("is-typing")

pygame.font.init()
font_path = pygame.font.match_font("verdana")
h1 = pygame.font.Font(font_path, 32)
h2 = pygame.font.Font(font_path, 16)

MAIN = 0
FRIEND = 1

state = FRIEND
run = True

optionNeg = "Bad!"
optionNeu = "Meh!"
optionPos = "Good!"

NEGATIVE = 0
NEUTRAL = 1
POSITIVE = 2

selected = -1

#setup the window
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class HomeScreen:
    def __init__(self):
        self.startButton = Button(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 250, 75,  pygame.Rect(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 250, 75), (0,255,0), h1.render('Start', False, (0,0,0)))
        self.aboutButton = Button(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 125, 250, 75, pygame.Rect(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 125, 250, 75), (200,200,200), h1.render('About', False, (0,0,0)))
          
class FriendScreen:
    def __init__(self):
        self.test = pygame.Rect(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 250, 75)
        self.name = "FRIEND"
        self.text = h1.render('My Bestie', True, (0,0,0))
        self.posButton = Button(SCREEN_WIDTH-225, SCREEN_HEIGHT-200, 250, 40,  pygame.Rect(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 250, 40), (0,255,0), h1.render('Start', False, (0,0,0)))
        self.neuButton = Button(SCREEN_WIDTH-225, SCREEN_HEIGHT-150, 250, 40,  pygame.Rect(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 250, 40), (0,255,0), h1.render('Start', False, (0,0,0)))
        self.negButton = Button(SCREEN_WIDTH-225, SCREEN_HEIGHT-100, 250, 40,  pygame.Rect(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 250, 40), (0,255,0), h1.render('Start', False, (0,0,0)))


#setup current screen
currScreen = FriendScreen()

def mainLoop():
    screen.fill((255,255,255))

    global currScreen
    global state

    startButton = currScreen.startButton
    aboutButton = currScreen.aboutButton

    # pygame.draw.rect(screen, startButton.color, startButton.visual, 0, 10)     
    # pygame.draw.rect(screen, aboutButton.color, aboutButton.visual, 0, 10)   
    startButton.draw()
    aboutButton.draw()

    screen.blit(startButton.text, (startButton.xPos-startButton.width/4, startButton.yPos-startButton.height/4))


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

    posButton = currScreen.posButton
    neuButton = currScreen.neuButton
    negButton = currScreen.negButton

    posButton.draw()
    neuButton.draw()
    negButton.draw()

    screen.blit(h2.render(optionNeg, True, (0,0,0)), (negButton.xPos, negButton.yPos))
    screen.blit(h2.render(optionNeu, True, (0,0,0)), (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 150))
    screen.blit(h2.render(optionPos, True, (0,0,0)), (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           global run
           run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            global selected
            if(posButton.checkMousePress(pos[0], pos[1])):
                selected = POSITIVE
            elif(neuButton.checkMousePress(pos[0], pos[1])):
                selected = NEUTRAL
            elif(negButton.checkMousePress(pos[0], pos[1])):
                selected = NEGATIVE


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
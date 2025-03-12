import pygame #used this video to review pygame basics: https://www.youtube.com/watch?v=y9VG3Pztok8

#referenced this link to import my own classes: https://csatlas.com/python-import-file-module/
import UI.GUI as GUI

starting_grammar = {
    'S': [['I', 'to', 'is-typing']],
    'I': ['Hello', 'Hey', 'Welcome', 'Hi'],
}

#initialize/setup pygame
pygame.init()
pygame.display.set_caption("is-typing")

pygame.font.init()
font_path = pygame.font.match_font("verdana")
font = pygame.font.Font(font_path, 32)

MAIN = 0
FRIEND = 1

state = 0
run = True


#setup the window
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class HomeScreen:
    def __init__(self):
        self.startButton = GUI.Button(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 250, 75,  pygame.Rect(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 250, 75), (0,255,0))
        self.aboutButton = GUI.Button(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 125, 250, 75, pygame.Rect(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 125, 250, 75), (200,200,200))
          
class FriendScreen:
    def __init__(self):
        self.test = pygame.Rect(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 250, 75)
        self.name = "FRIEND"
        self.text = font.render('My Bestie', True, (0,0,0))

#setup current screen
currScreen = HomeScreen()

def mainLoop():
    screen.fill((255,255,255))

    global currScreen
    global state

    pygame.draw.rect(screen, currScreen.startButton.color, currScreen.startButton.visual, 0, 10)      
    pygame.draw.rect(screen, currScreen.aboutButton.color, currScreen.aboutButton.visual, 0, 10)   

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           global run
           run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if(currScreen.startButton.checkMousePress(pos[0], pos[1])):
                print("start!")
                state = FRIEND       
                currScreen = FriendScreen()
            
            elif(currScreen.aboutButton.checkMousePress(pos[0], pos[1])):
                print("about!")  

def textScreen():
    screen.fill((255,255,255))
    pygame.draw.rect(screen, (0,255,0), currScreen.test) 
    screen.blit(currScreen.text, currScreen.test)
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           global run
           run = False


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
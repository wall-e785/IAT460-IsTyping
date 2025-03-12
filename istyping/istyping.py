import pygame #used this video to review pygame basics: https://www.youtube.com/watch?v=y9VG3Pztok8

#referenced this link to import my own classes: https://csatlas.com/python-import-file-module/
import UI.GUI as GUI

starting_grammar = {
    'S': [['I', 'to', 'is-typing']],
    'I': ['Hello', 'Hey', 'Welcome', 'Hi'],
}

#initialize pygame
pygame.init()


#setup the window
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

guiElements = []

guiElements.append(GUI.Button(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 250, 75,  pygame.Rect(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 250, 75), (0,255,0)))
guiElements.append(GUI.Button(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 125, 250, 75, pygame.Rect(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 125, 250, 75), (255,255,255)))


#core loop to run the program
run = True
while run:

    #clear screen with each iteration
    screen.fill((0,0,0))

    #pygame.draw.rect(screen, (0,255,0), player)

    for element in guiElements:
        pygame.draw.rect(screen , element.color, element.visual, 0, 10)

    key = pygame.key.get_pressed()

    #check event handlers
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for element in guiElements:
                element.checkMousePress(pos[0], pos[1])
    #updates screen to display objects
    pygame.display.update()

pygame.quit()
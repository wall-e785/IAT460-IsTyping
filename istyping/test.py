#code setup referenced from: https://www.pythonguis.com/tutorials/pyqt6-creating-your-first-window/
#https://realpython.com/arduino-python/
from pyfirmata2 import Arduino
import time
import pygame

# import pygame.locals for easier 
# access to key coordinates
from pygame.locals import *
 

#  analog_value = analog_input.read()

board = Arduino.AUTODETECT

class AnalogPrinter:

    def __init__(self):
        # sampling rate: 10Hz
        self.samplingRate = 10
        self.timestamp = 0
        self.board = board

    def start(self):
        self.board.analog[0].register_callback(self.myPrintCallback)
        self.board.samplingOn(1000 / self.samplingRate)
        self.board.analog[0].enable_reporting()

    def myPrintCallback(self, data):
        print("%f,%f" % (self.timestamp, data))
        self.timestamp += (1 / self.samplingRate)

    def stop(self):
        self.board.exit()

print("Let's print data from Arduino's analogue pins for 10secs.")

# Let's create an instance
analogPrinter = AnalogPrinter()

# and start DAQ
analogPrinter.start()

# let's acquire data for 10secs. We could do something else but we just sleep!
time.sleep(10)

# let's stop it
analogPrinter.stop()

# Define our square object and call super to
# give it all the properties and methods of pygame.sprite.Sprite
# Define the class for our square objects
class Square(pygame.sprite.Sprite):
    def __init__(self):
        super(Square, self).__init__()
         
        # Define the dimension of the surface
        # Here we are making squares of side 25px
        self.surf = pygame.Surface((25, 25))
         
        # Define the color of the surface using RGB color coding.
        self.surf.fill((0, 200, 255))
        self.rect = self.surf.get_rect()
 
# initialize pygame
pygame.init()
 
# Define the dimensions of screen object
screen = pygame.display.set_mode((800, 600))
 
# instantiate all square objects
square1 = Square()
square2 = Square()
square3 = Square()
square4 = Square()
 
# Variable to keep our game loop running
gameOn = True
 
# Our game loop
while gameOn:
    # for loop through the event queue
    for event in pygame.event.get():
         
        # Check for KEYDOWN event
        if event.type == KEYDOWN:
             
            # If the Backspace key has been pressed set
            # running to false to exit the main loop
            if event.key == K_BACKSPACE:
                gameOn = False
                 
        # Check for QUIT event
        elif event.type == QUIT:
            gameOn = False
 
    # Define where the squares will appear on the screen
    # Use blit to draw them on the screen surface
    screen.blit(square1.surf, (40, 40))
    screen.blit(square2.surf, (40, 530))
    screen.blit(square3.surf, (730, 40))
    screen.blit(square4.surf, (730, 530))
 
    # Update the display using flip
    pygame.display.flip()

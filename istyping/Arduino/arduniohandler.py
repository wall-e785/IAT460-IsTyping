#handling arduino read using pyfirmata2 is referenced/built upon from the 
#creator's (Bernd Porr) GitHub example here: https://github.com/berndporr/pyFirmata2
#licensing information can be found at: https://github.com/berndporr/pyFirmata2/blob/master/LICENSE
#also referenced arduino setup from: #https://realpython.com/arduino-python/

from pyfirmata2 import Arduino

#change the argument here to whichever port your arduino board is connected to
PORT = Arduino("/dev/cu.usbserial-D309S67T")


# prints data on the screen at the sampling rate of 10Hz
# can easily be changed to saving data to a file

# It uses a callback operation so that timing is precise and
# the main program can just go to sleep.
# Copyright (c) 2018-2020, Bernd Porr <mail@berndporr.me.uk>
# see LICENSE file.

class AnalogPrinter:

    def __init__(self):
        # sampling rate: 10Hz
        self.samplingRate = 10
        self.timestamp = 0
        self.board = PORT
        self.data = 0

    def start(self):
        #pin 0 analog input registers to the callback
        self.board.analog[0].register_callback(self.myPrintCallback)
        self.board.samplingOn(1000 / self.samplingRate)
        self.board.analog[0].enable_reporting()

    def myPrintCallback(self, data):
        #data is saved to the object each time data is received from analog pin 0
        self.data = data

    def stop(self):
        #close board
        self.board.exit()

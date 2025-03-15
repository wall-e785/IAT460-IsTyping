#code setup referenced from: https://www.pythonguis.com/tutorials/pyqt6-creating-your-first-window/
#https://realpython.com/arduino-python/
import pyfirmata2
import time
 

board = pyfirmata2.Arduino("/dev/cu.usbserial-D309S67T")

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
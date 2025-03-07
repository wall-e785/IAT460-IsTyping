#code setup referenced from: https://www.pythonguis.com/tutorials/pyqt6-creating-your-first-window/
#https://realpython.com/arduino-python/
import sys
import pyfirmata
import time

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("is_typing")
        button = QPushButton("Press Me!")

        #does not allow user to resize screen
        self.setFixedSize(QSize(400, 300))

        # Set the central widget of the Window.
        analog_value = analog_input.read()
        button.text = analog_value
        self.setCentralWidget(button)
        button.clicked.connect(self.the_button_was_clicked)

    
    def the_button_was_clicked (self):
        print("Clicked!")

board = pyfirmata.Arduino('COM3')
it = pyfirmata.util.Iterator(board)
it.start()

analog_input = board.get_pin('a:0:i')

app = QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()
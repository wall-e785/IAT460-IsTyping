# IAT460-IsTyping
IAT 460 Final Project - is_typing

To run this project, you will need an Arduino UNO Board, a Pressure sensor (and other circuit-building materials)

REQUIREMENTS:
-Connect your Arduino UNO Board and upload the 'Standard Firmata' sketch to it through Arduino.
-In the arduinohandler.py file, update the PORT variable to your board's port. This can be found in the Arduino environment, but remember to close it before running the Python file.
-You will need a Google Gemini API key. store this in a file called env.py, with a variable called gemini

**SETUP:**
This project was created on Python 3.9.2. Download it from here: https://www.python.org/downloads/release/python-392/
After downloading Python, create a virtual environment in VSCode to run the program. More information can be found here: https://code.visualstudio.com/docs/python/environments
The following libaries are also required to be downloaded using pip into the virtual environment:
  pygame
  google.generativeai
  dotenv
  pyfirmata2
  math
  rand

To setup the Arduino board, you will need to upload the StandardFirmata example sketch. More information to find this sketch in Arduino can be found here, as well as the original documentation of pyfirmata2: https://github.com/berndporr/pyFirmata2
You will also need wires, a pressure sensor, and a 10k ohm resistor. Create the following circuit as shown:
<CIRCUIT DIAGRAM HERE>

In Arduino, figure out which port the board is connected to. Copy and paste this to Arduino -> arduinotest.py, line 7 so the data can be sent to the python program.

A Google Gemini API key is also required; find more information here: https://aistudio.google.com/
Once you have an API key, create a file in the main hierarchy called .env
On a single line, enter: GEMINI_KEY = "<YOUR KEY HERE>" for the other files to access the Gemini API

Once all the setup steps are complete, you are ready to run the program. 

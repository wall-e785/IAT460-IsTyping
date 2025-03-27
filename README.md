# IAT460-IsTyping
is-typing is an interactive art piece, highlighting the idea of ambiguity in text-based communication. Users have conversations with three individuals, each preferring an unknown "tone" of message to the user. Users must select what they believe is the most appropriate response using a physical pressure sensor, translating it into text emotion. This project uses generative grammar rulesets to create dialogue, as well as the Google Gemini API to expand these sets.

This project was created for SFU IAT 460 - Generative AI and Computational Creativity

# Setup:
This project was created on Python 3.9.2. Download it from here: https://www.python.org/downloads/release/python-392/
After downloading Python, create a virtual environment in VSCode to run the program. More information can be found here: https://code.visualstudio.com/docs/python/environments

The following libaries are also required to be downloaded using pip into the virtual environment: _pygame, google.generativeai, dotenv, pyfirmata2, math, rand_

To setup the Arduino board, you will need to upload the StandardFirmata example sketch. More information to find this sketch in Arduino can be found here, as well as the original documentation of pyfirmata2: https://github.com/berndporr/pyFirmata2
You will also need wires, a pressure sensor, and a 10k ohm resistor. Create the following circuit as shown:
![Circuit Diagram](https://github.com/user-attachments/assets/dd0112fb-e486-4e43-990e-b35133373ac0)

A 10G-5KG (1" Area) Force Pressure Sensor (exact model shown below) was used to gather input for this project. To learn more about Force Pressure Sensors (FSR), read here: https://learn.adafruit.com/force-sensitive-resistor-fsr/overview 
<img width="343" alt="Screenshot 2025-03-27 at 12 56 26 PM" src="https://github.com/user-attachments/assets/d33d41bd-5aa3-469f-9634-bd80653ae418" />

In Arduino, figure out which port the board is connected to. Copy and paste this to file in folder: Arduino -> arduinohandler.py, line 9 so the data can be sent to the python program.

A Google Gemini API key is also required; find more information here: https://aistudio.google.com/
Once you have an API key, create a file in the main hierarchy called .env
On a single line, enter: GEMINI_KEY = "<YOUR KEY HERE>" for the other files to access the Gemini API

Once all the setup steps are complete, you are ready to run the program. Run the istyping.py file using your created virtual environment. 

# Credits:
Created by Wallace Chau

Special thanks to Tino de Bruijn and Bernd Porr for creating pyfirmata2: https://github.com/berndporr/pyFirmata2

Special thanks for ZapSplat.com for providing the sound effects for this project. Standard License information can be found here: https://www.zapsplat.com/license-type/standard-license/

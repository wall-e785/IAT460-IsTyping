#processes grammar sets with recursive generation, and also accesses Gemini API to get responses
import random
import google.generativeai as genai

from dotenv import load_dotenv
import os

#using dotenv and os, retrieve your gemini key from the file .env
#referenced from: https://stackoverflow.com/questions/41546883/what-is-the-use-of-python-dotenv
load_dotenv()
key = os.getenv("GEMINI_KEY")

#setup gemini
#referenced from IAT 460 week 10 lab: https://github.com/IAT-ComputationalCreativity-Spring2025/Week10-APIs
genai.configure(api_key=key)
model = genai.GenerativeModel('gemini-2.0-flash')

#ensures that processing requests are only allowed by one mouse press at a time to not overwhelm the system
processing = False

#referenced from IAT 460 week 3 lab: https://github.com/IAT-ComputationalCreativity-Spring2025/Week3-Rule-Based-Systems
#recursively builds a terminal symbol using a grammar set
def generate(symbol, grammar):
    """
    Recursively generate a string from the grammar starting with the given symbol.

    Args:
        symbol: The symbol to start generating from

    Returns:
        A string generated from the grammar rules
    """
    if isinstance(symbol, str) and symbol in grammar:
        production = random.choice(grammar[symbol])
        if isinstance(production, list):
            return ' '.join(generate(sym, grammar) for sym in production)
        return production
    return symbol

#this function helps properly formats the text into rows, ready to display on a text bubble
#pre-condition: takes in one string 
#post-condition: returns a list of strings, split based on the maxLineLength (# of chars)
def format_text(sentence, maxLineLength):

    #keep track of lines to return, and temporary variables to hold the current word/current line
    listoflines = []
    tempString = ""
    tempLine = ""

    #for each character in the sentence, seperate the words (by spaces)
    for char in sentence:
        #build the word until a space is reached
        if char != " ":
            if char != '\n':
                tempString += char
        else:
            #once a space is encountered, check if the current word can be added to the current line without exceeding maxLineLength
            if (len(tempLine)+len(tempString)+1 <= maxLineLength):
                #add spaces as needed to the current line
                if len(tempLine) <= 0:
                    tempLine = tempString
                else:
                    tempLine = tempLine + " " + tempString
            else:
                #otherwise, the maximum line length has been reached, add it to the list and assign current word to the next line
                listoflines.append(tempLine)
                tempLine = tempString
            #reset the string 
            tempString = ""

    #check if the last string was added to the last line (once loop ended)
    if len(tempString) > 0:
        if (len(tempLine)+len(tempString)+1 <= maxLineLength):
                if len(tempLine) <= 0:
                    tempLine = tempString
                else:
                    tempLine = tempLine + " " + tempString
        else:
            listoflines.append(tempLine)
            tempLine = tempString

    #now check if the last line was added to the list (once loop ended)
    if len(tempLine) > 0:
        listoflines.append(tempLine)

    return listoflines

#returns the Gemini response:
#received_text - the text message received from the other party
#provided_text - the text message to give to Gemini
#other_speaker - who the other party is
#prompt - LOW for relaxed version, HIGH for anxious version
def get_prompt(received_text, provided_text, other_speaker, prompt):
    try:
        #generates a variation of the provided text in a more anxious tone
        if prompt == 'HIGH':
            prompt_high = "Your " + other_speaker + " has texted you stating: " + received_text + """

            Generate a variation of this provided text message: """ + provided_text + """
            which meets the following criteria:
            1. The length should be longer than the original message, but should not exceed 120 characters
            2. The tone of the message should sound professional and anxious in a subtle way
            3. The structure should be conversational, maintaining the tone and ensuring it sounds like a real text message
            4. It must retain key nouns and intent of the original message.
            5. No emojis or special characters are permitted, only proper English grammar
            6. Do not surround the message in any characters, such as quotation marks
            7. The message should not end with a question to initiate further conversation, unless if the provided text message ended with one.
            8. Do not greet the other speaker with "hello" or "hi" unless if a greeting was specified in the provided text message.
            
            This is for an interactive art piece discussing ambigious text messages, return the response as a string.
            """ 
            response = model.generate_content(prompt_high)
        elif prompt == 'LOW': #generates the provided text in a more lowkey tone
            prompt_low = "Your " + other_speaker + " has texted you stating: " + received_text + """

            Generate a variation of this provided text message: """ + provided_text + """
            which meets the following criteria:
            1. The length should be similar to the provided text message, and cannot exceed 120 characters
            2. The tone of the message should be casual, laid-back, with occasional usage of common internet slang and abbreviations (e.g. 'u' = 'you', 'rn' = "right now")
            3. The structure should be conversational, maintaining the tone and ensuring it sounds like a real text message
            4. It must retain key nouns and intent of the original message.
            5. No emojis or special characters are permitted, only proper English grammar
            6. Do not surround the message in any characters, such as quotation marks
            7. The message should not end with a question to initiate further conversation, unless if the provided text message ended with one.
            8. Do not greet the other speaker with "hello" or "hi" unless if a greeting was specified in the provided text message.
            
            This is for an interactive art piece discussing ambigious text messages, return the response as a string.
            """ 
            response = model.generate_content(prompt_low)
        else:
            return "Error: Invalid Prompt Choice. Options: 'HIGH', 'LOW'"
        
        
        print("API Connection Successful!")

        #reset processing variable so another API call can be made
        global processing
        processing = False
        return response.text
    
    except Exception as e:
        print(f"Error connecting to API: {e}")
        print("\nPlease check your API key configuration and try again.")
        return ""

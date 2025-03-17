#processes grammar sets with recursive generation, and also accesses Gemini API to get responses
import random
import google.generativeai as genai
import env

key = env.gemini
genai.configure(api_key=key)
model = genai.GenerativeModel('gemini-2.0-flash')

#ensures that processing requests are only allowed by one mouse press at a time to not overwhelm the system
processing = False

#referenced from week 3 lab
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

#this function helps properly format the sentence by capitalizing
def format_sentence(sentence):
    #referenced for upper: https://stackoverflow.com/questions/17794241/how-do-i-convert-only-specific-parts-of-a-string-to-uppercase-in-python
    return sentence[0].upper() + sentence[1:]

#overloaded version that also adds caps to end of punctuation

#returns the Gemini response:
#received_text - the text message received from the other party
#provided_text - the text message to give to Gemini
#other_speaker - who the other party is
#prompt - LOW for relaxed version, HIGH for anxious version
def get_prompt(received_text, provided_text, other_speaker, prompt):
    try:
        if prompt == 'HIGH':
            prompt_high = "Provided Text Message: " + provided_text + """

            This is a response to a message from your """ + other_speaker + " stating: " + received_text + """

            Generate a variation of the provided text message that fits the following criteria:
            1. The length should be longer than the original message, but should not exceed 15 words
            2. The tone of the message should be more professional, slightly anxious in a subtle way
            3. The structure should be conversational, maintaining the tone and ensuring it sounds like a real text message
            4. Must retain key nouns and intent of message without adding new context
            5. No emojis or special characters are permitted, only proper English grammar
            
            Return the response as a string.
            """ 
            response = model.generate_content(prompt_high)
        elif prompt == 'LOW':
            prompt_low = "Provided Text Message: " + provided_text + """

            This is a response to a message from your """ + other_speaker + " stating: " + received_text + """

            Generate a variation of the provided text message that fits the following criteria:
            1. Similar in length, maximum of +/- 2 word length
            2. The tone of the message should be casual, laid-back, with optional usage of common internet slang and abbreviations (e.g. 'u' = 'you', 'rn' = "right now")
            3. The structure should be conversational, maintaining the tone and ensuring it sounds like a real text message
            4. Must retain key nouns and intent of message without adding new context
            5. No emojis or special characters are permitted, only proper English grammar
            
            Return the response as a string.
            """ 
            response = model.generate_content(prompt_low)
        else:
            return "Error: Invalid Prompt Choice. Options: 'HIGH', 'LOW'"
        
        
        print("API Connection Successful!")
        global processing
        processing = False
        return response.text
        #return "filler"
    except Exception as e:
        print(f"Error connecting to API: {e}")
        print("\nPlease check your API key configuration and try again.")
        return ""

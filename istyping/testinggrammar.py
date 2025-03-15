
import google.generativeai as genai
import env
import GrammarSets.friend

key = env.gemini
genai.configure(api_key=key)


prompt_high = """
        Provided Text Message: Alright, I am just in class right now.

        Generate 5 variations of the provided text message that fits the following criteria:
        1. The length should be longer than the original message, with a maximum length of 15 words
        2. More professional, slightly anxious tone, that has proper usage of English grammar rules
        3. Must retain key nouns
        4. This is a response to a message from your friend stating: Hey, what's up?

        Return the response as a string.
        """ 

prompt_low = """
        Provided Text Message: Good, I am just in class right now.

        Generate a variation of the provided text message that fits the following criteria:
        1. Similar in length, maximum of +/- 2 word length
        2. Casual tone, with usage of common internet slang and abbreviations (ex. 'u' = 'you')
        3. Must retain key nouns

        Return the response as a string.
        """ 


try:
    # Test a simple query
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content(prompt_high)
    print(response.text)
    response = model.generate_content(response.text + "Choose the response which feels the most natural for a text message conversation. Return it as a string on its own.")
    print("API Connection Successful!")
    print("\Results:")
    print(response.text)
except Exception as e:
    print(f"Error connecting to API: {e}")
    print("\nPlease check your API key configuration and try again.")

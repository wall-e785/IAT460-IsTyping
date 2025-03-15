
import google.generativeai as genai
import env
import GrammarSets.friend

key = env.gemini
genai.configure(api_key=key)

try:
    # Test a simple query
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content("Write a haiku about artificial intelligence")

    print("API Connection Successful!")
    print("\nHaiku response:")
    print(response.text)
except Exception as e:
    print(f"Error connecting to API: {e}")
    print("\nPlease check your API key configuration and try again.")
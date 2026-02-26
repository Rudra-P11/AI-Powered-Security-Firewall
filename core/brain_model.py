import os
from google import genai

# Using older google.generativeai or newer google-genai depending on the installed package.
# We will use the new `google-genai` module as per the requirements.

def generate_safe_response(user_input):
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    try:
        response = client.models.generate_content(
            model='gemini-2.5-pro',
            contents=user_input,
        )
        return response.text
    except Exception as e:
        return f"Brain model error: {str(e)}"

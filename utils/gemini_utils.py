import os 
import google.generativeai as genai

def configure_gemini_api():
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY not found. Please set it as an environment variable.")

    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-3.5-flash")
    print("✅ Gemini API configured successfully.")
    return model
import google.generativeai as genai


def configure_gemini_api():
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY not found. Please set it as an environment variable.")

    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-3.5-flash")
    print("✅ Gemini API configured successfully.")
    return model

  
def ask_gemini(model, document, prompt_text):
    # Modify to include document context for the Gemini model
    full_prompt = f"""
   You are an expert AI research Assistant
   Answer ONLY using the information provided in the document below.
  If the answer is not present In The document clearly say:
  "I couldn't find this information in the uploaded document."
   --------------------------DOCUMENT-----------------------------
   {document}
   --------------------------USER QUESTION------------------------
   {prompt_text}
   Provide a Clear well-structured answer:
   """
    response = model.generate_content(full_prompt)
    return response.text

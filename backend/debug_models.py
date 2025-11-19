# backend/debug_models.py

import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Error: GEMINI_API_KEY not found in .env file.")
else:
    try:
        print("API Key loaded. Fetching available models...")
        genai.configure(api_key=api_key)

        print("-" * 50)
        print("Available Models for 'generateContent':")
        print("-" * 50)

        # List all models and filter for the ones that support the 'generateContent' method
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"- {m.name}")
        
        print("-" * 50)

    except Exception as e:
        print(f"An error occurred: {e}")
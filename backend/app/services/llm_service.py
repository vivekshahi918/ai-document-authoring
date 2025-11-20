# backend/app/services/llm_service.py

from typing import List
from google.generativeai import GenerativeModel, configure
from ..core.config import settings
import traceback

# Configure the Gemini key
configure(api_key=settings.GEMINI_API_KEY)

# Updated model with mandatory safety settings
model = GenerativeModel(
    model_name="gemini-1.5-flash",
    safety_settings=[
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]
)

async def generate_content_for_section(main_topic: str, section_title: str) -> str:
    try:
        prompt = (
            f"You are an expert business document writer. "
            f"Your task is to write the content for a specific section of a document. "
            f"The main topic of the document is: '{main_topic}'. "
            f"The specific section you need to write is: '{section_title}'. "
            f"Please write detailed, professional content for this section. "
            f"Do not include the section title itself in your response, only the content."
        )

        # Prompt must always be passed inside a list
        response = await model.generate_content_async([prompt])

        if hasattr(response, "text") and response.text:
            return response.text
        return "Content could not be generated due to safety settings."

    except Exception:
        print("--- DETAILED ERROR IN generate_content_for_section ---")
        print(traceback.format_exc())
        print("----------------------------------------------------")
        return "Error: Could not generate content."


async def refine_content_for_section(original_content: str, refinement_prompt: str) -> str:
    try:
        prompt = (
            f"You are a world-class editor. Your task is to refine the following text based on a specific instruction.\n\n"
            f"--- Original Text ---\n{original_content}\n\n"
            f"--- Instruction ---\n{refinement_prompt}\n\n"
            f"Provide only the refined text."
        )

        response = await model.generate_content_async([prompt])

        if hasattr(response, "text") and response.text:
            return response.text
        return "Content could not be refined due to safety settings."

    except Exception:
        print("--- DETAILED ERROR IN refine_content_for_section ---")
        print(traceback.format_exc())
        print("----------------------------------------------------")
        return "Error: Could not refine content."


async def generate_outline(main_topic: str, doc_type: str) -> List[str]:
    item_type = "section headers" if doc_type == "docx" else "slide titles"

    try:
        prompt = (
            f"You are a project planner. Based on the main topic '{main_topic}', "
            f"generate a list of 5–7 relevant {item_type}. "
            f"Return the list as a simple comma-separated string."
        )

        response = await model.generate_content_async([prompt])

        if hasattr(response, "text") and response.text:
            return [i.strip() for i in response.text.split(",")]

        return []

    except Exception:
        print("--- DETAILED ERROR IN generate_outline ---")
        print(traceback.format_exc())
        print("----------------------------------------------------")
        return []

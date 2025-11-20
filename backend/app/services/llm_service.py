# backend/app/services/llm_service.py

from typing import List
from google.generativeai import GenerativeModel, configure
from ..core.config import settings
import traceback

# Configure the Gemini key
configure(api_key=settings.GEMINI_API_KEY)

# Railway supports ONLY this model (v1beta)
model = GenerativeModel(
    model_name="gemini-pro"
)

async def generate_content_for_section(main_topic: str, section_title: str) -> str:
    """
    Generates content for a specific document section using Gemini.
    """
    try:
        prompt = (
            f"You are an expert business document writer. "
            f"Your task is to write the content for a specific section of a document. "
            f"The main topic of the document is: '{main_topic}'. "
            f"The specific section you need to write is: '{section_title}'. "
            f"Write detailed, professional content for this section. "
            f"Do NOT include the section title itself."
        )

        # Prompt must be inside a list
        response = await model.generate_content_async([prompt])

        if hasattr(response, "text") and response.text:
            return response.text

        return "Content could not be generated."

    except Exception:
        print("--- DETAILED ERROR IN generate_content_for_section ---")
        print(traceback.format_exc())
        print("--------------------------------------------------------")
        return "Error: Could not generate content."


async def refine_content_for_section(original_content: str, refinement_prompt: str) -> str:
    """
    Refines existing content using Gemini.
    """
    try:
        prompt = (
            f"You are a world-class editor. Refine the following text.\n\n"
            f"--- Original Text ---\n{original_content}\n\n"
            f"--- Instruction ---\n{refinement_prompt}\n\n"
            f"Return ONLY the improved text."
        )

        response = await model.generate_content_async([prompt])

        if hasattr(response, "text") and response.text:
            return response.text

        return "Content could not be refined."

    except Exception:
        print("--- DETAILED ERROR IN refine_content_for_section ---")
        print(traceback.format_exc())
        print("--------------------------------------------------------")
        return "Error: Could not refine content."


async def generate_outline(main_topic: str, doc_type: str) -> List[str]:
    """
    Generates outline section headers or slide titles.
    """
    item_type = "section headers" if doc_type == "docx" else "slide titles"

    try:
        prompt = (
            f"You are a project planner. Based on the topic '{main_topic}', "
            f"generate 5–7 relevant {item_type}. "
            f"Return them as a comma-separated list without numbers."
        )

        response = await model.generate_content_async([prompt])

        if hasattr(response, "text") and response.text:
            return [i.strip() for i in response.text.split(",")]

        return []

    except Exception:
        print("--- DETAILED ERROR IN generate_outline ---")
        print(traceback.format_exc())
        print("--------------------------------------------------------")
        return []

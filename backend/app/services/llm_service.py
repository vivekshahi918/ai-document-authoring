from typing import List
from google import genai
from google.genai import types
from ..core.config import settings
import traceback

# Initialize client with new Gemini v1 API
client = genai.Client(api_key=settings.GEMINI_API_KEY)


async def generate_content_for_section(main_topic: str, section_title: str) -> str:
    try:
        prompt = (
            f"You are an expert business document writer. "
            f"Main topic: '{main_topic}'. "
            f"Write detailed content for the section: '{section_title}'. "
            f"Do NOT return the section title."
        )

        response = await client.models.generate_content(
            model="gemini-1.5-flash",
            contents=[prompt],
        )

        return response.text or "Content generation failed."

    except Exception:
        print("--- ERROR in generate_content_for_section ---")
        print(traceback.format_exc())
        print("--------------------------------------------")
        return "Error: Could not generate content."


async def refine_content_for_section(original_content: str, refinement_prompt: str) -> str:
    try:
        prompt = (
            f"You are a world-class editor.\n\n"
            f"--- Original Text ---\n{original_content}\n\n"
            f"--- Instruction ---\n{refinement_prompt}\n\n"
            f"Return only the refined text."
        )

        response = await client.models.generate_content(
            model="gemini-1.5-flash",
            contents=[prompt],
        )

        return response.text or "Refinement failed."

    except Exception:
        print("--- ERROR in refine_content_for_section ---")
        print(traceback.format_exc())
        print("-------------------------------------------")
        return "Error: Could not refine content."


async def generate_outline(main_topic: str, doc_type: str) -> List[str]:
    try:
        item_type = "section headers" if doc_type == "docx" else "slide titles"

        prompt = (
            f"Generate 5–7 {item_type} for the topic '{main_topic}'. "
            f"Return them as a comma-separated list."
        )

        response = await client.models.generate_content(
            model="gemini-1.5-flash",
            contents=[prompt],
        )

        if response.text:
            return [i.strip() for i in response.text.split(",")]

        return []

    except Exception:
        print("--- ERROR in generate_outline ---")
        print(traceback.format_exc())
        print("--------------------------------")
        return []

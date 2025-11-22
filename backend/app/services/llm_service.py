
from typing import List
import google.generativeai as genai
from ..core.config import settings
import traceback 


genai.configure(api_key=settings.GEMINI_API_KEY)

model = genai.GenerativeModel('gemini-2.5-pro')
print("🔥 USING MODEL:", model.model_name)



async def generate_content_for_section(main_topic: str, section_title: str) -> str:
    """
    Generates content for a specific document section using the Gemini API.
    """
    try:
        prompt = (
            f"You are an expert business document writer. "
            f"The main topic of the document is: '{main_topic}'. "
            f"The specific section you need to write is: '{section_title}'. "
            f"Please write detailed, professional content for this section. "
            f"Do not include the section title itself in your response, only the content."
        )
        response = await model.generate_content_async(prompt)
        return response.text
    except Exception as e:
        print("--- DETAILED ERROR IN generate_content_for_section ---")
        traceback.print_exc()
        print("----------------------------------------------------")
        return "Error: Could not generate content due to an API issue."


async def refine_content_for_section(original_content: str, refinement_prompt: str) -> str:
    try:
        prompt = (
            f"You are a world-class editor. Your task is to refine the following text based on a specific instruction.\n\n"
            f"--- Original Text ---\n{original_content}\n\n"
            f"--- Instruction ---\n{refinement_prompt}\n\n"
            f"Please provide only the fully refined text as your response."
        )
        response = await model.generate_content_async(prompt)
        return response.text
    except Exception as e:
        print("--- DETAILED ERROR IN refine_content_for_section ---")
        traceback.print_exc()
        print("--------------------------------------------------")
        return "Error: Could not refine content due to an API issue."


async def generate_outline(main_topic: str, doc_type: str) -> List[str]:
    """
    Generates a list of section headers or slide titles for a given topic.
    """
    item_type = "section headers" if doc_type == "docx" else "slide titles"
    try:
        prompt = (
            f"You are a project planner. Based on the main topic '{main_topic}', "
            f"generate a list of 5-7 relevant {item_type} for a business document. "
            f"Return the list as a simple comma-separated string, without numbers or bullets. "
            f"For example: Introduction, Market Analysis, Competitive Landscape, Conclusion"
        )
        response = await model.generate_content_async(prompt)
        return [item.strip() for item in response.text.split(',')]
    except Exception as e:
        print("--- DETAILED ERROR IN generate_outline ---")
        traceback.print_exc()
        print("----------------------------------------")
        return [] 
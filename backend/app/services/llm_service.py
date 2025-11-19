# backend/app/services/llm_service.py
from typing import List

import google.generativeai as genai
from ..core.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

# Initialize the model
# model = genai.GenerativeModel('models/gemini-pro-latest')
model = genai.GenerativeModel('gemini-1.5-flash-latest')

async def generate_content_for_section(main_topic: str, section_title: str) -> str:
    """
    Generates content for a specific document section using the Gemini API.
    """
    try:
        # Create a specific, context-aware prompt
        prompt = (
            f"You are an expert business document writer. "
            f"Your task is to write the content for a specific section of a document. "
            f"The main topic of the document is: '{main_topic}'. "
            f"The specific section you need to write is: '{section_title}'. "
            f"Please write detailed, professional content for this section. "
            f"Do not include the section title itself in your response, only the content."
        )

        response = await model.generate_content_async(prompt)
        
        # Make sure to handle potential safety blocks
        if response.parts:
            return response.text
        else:
            return "Content could not be generated due to safety settings."

    except Exception as e:
        print(f"An error occurred during content generation: {e}")
        return "Error: Could not generate content."
    
async def refine_content_for_section(original_content: str, refinement_prompt: str) -> str:
    try:
        # Create a prompt specifically for editing/refining
        prompt = (
            f"You are a world-class editor. Your task is to refine the following text based on a specific instruction.\n\n"
            f"--- Original Text ---\n{original_content}\n\n"
            f"--- Instruction ---\n{refinement_prompt}\n\n"
            f"Please provide only the fully refined text as your response, without any extra commentary or conversational text."
        )
        
        response = await model.generate_content_async(prompt)
        
        if response.parts:
            return response.text
        else:
            return "Content could not be refined due to safety settings."

    except Exception as e:
        print(f"An error occurred during content refinement: {e}")
        return "Error: Could not refine content."    
    
async def generate_outline(main_topic: str, doc_type: str) -> List[str]:
    item_type = "section headers" if doc_type == "docx" else "slide titles"
    try:
        prompt = (
            f"You are a project planner. Based on the main topic '{main_topic}', "
            f"generate a list of 5-7 relevant {item_type} for a business document. "
            f"Return the list as a simple comma-separated string, without numbers or bullets. "
            f"For example: Introduction, Market Analysis, Competitive Landscape, Conclusion"
        )
        response = await model.generate_content_async(prompt)
        # Simple parsing
        return [item.strip() for item in response.text.split(',')]
    except Exception as e:
        print(f"An error occurred during outline generation: {e}")
        return []    

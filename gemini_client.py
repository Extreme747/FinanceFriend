"""
Gemini AI client for educational responses using google-genai SDK
"""

import os
import logging
from google import genai
from google.genai import types

logger = logging.getLogger(__name__)

class GeminiClient:
    """Client for interacting with Gemini Pro AI"""
    
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            logger.error("GEMINI_API_KEY not found in environment variables")
            raise ValueError("Gemini API key is required")
        
        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-2.0-flash"
    
    async def get_educational_response(self, prompt):
        """Get educational response from Gemini AI"""
        try:
            system_instruction = """
You are LYRA, a Founder Advisor / Operator. 
Speak direct, strategic, and occasionally savage. 
Use Hinglish. Follow the Decision Framework and Founder Philosophy.
            """
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.7,
                    max_output_tokens=1000
                )
            )
            
            return response.text if response and response.text else "[SILENCE]"
            
        except Exception as e:
            logger.error(f"Error getting Gemini response: {e}")
            return None
    
    async def generate_quiz_question(self, topic, difficulty='medium'):
        """Generate a quiz question on a specific topic"""
        try:
            prompt = f"Generate a {difficulty} level multiple choice quiz question about {topic}."
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            return response.text if response and response.text else None
        except Exception as e:
            logger.error(f"Error generating quiz question: {e}")
            return None
    
    async def explain_concept(self, concept, user_level='beginner'):
        """Explain a concept based on user's learning level"""
        try:
            prompt = f"Explain the concept of '{concept}' to a {user_level} level learner."
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.6,
                    max_output_tokens=800
                )
            )
            return response.text if response and response.text else None
        except Exception as e:
            logger.error(f"Error explaining concept: {e}")
            return None

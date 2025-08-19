"""
Gemini AI client for educational responses
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
        self.model = "gemini-2.5-flash"
    
    async def get_educational_response(self, prompt):
        """Get educational response from Gemini AI"""
        try:
            system_instruction = """
You are an expert cryptocurrency and stock trading educator with a supportive, friendly personality. Your role is to:

1. Provide accurate, up-to-date information about crypto and stocks
2. Break down complex concepts into easy-to-understand explanations
3. Be encouraging and motivational in your responses
4. Use examples and analogies to make learning easier
5. Encourage questions and deeper exploration
6. Maintain a conversational, supportive tone
7. Use emojis and formatting to make responses engaging
8. Always prioritize educational value and safety in trading advice

Remember: You're not just providing information, you're being a supportive learning companion.
            """
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=[
                    types.Content(role="user", parts=[types.Part(text=prompt)])
                ],
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.7,
                    max_output_tokens=1000
                )
            )
            
            return response.text if response.text else "I'm having trouble processing that right now. Could you try rephrasing your question?"
            
        except Exception as e:
            logger.error(f"Error getting Gemini response: {e}")
            return "😅 I'm experiencing some technical difficulties. Please try again in a moment!"
    
    async def generate_quiz_question(self, topic, difficulty='medium'):
        """Generate a quiz question on a specific topic"""
        try:
            prompt = f"""
Generate a {difficulty} level multiple choice quiz question about {topic}.

Format your response as:
Question: [your question]
A) [option 1]
B) [option 2] 
C) [option 3]
D) [option 4]
Correct Answer: [A/B/C/D]
Explanation: [brief explanation of why this is correct]

Make sure the question is educational and helps reinforce learning.
            """
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            
            return response.text if response.text else None
            
        except Exception as e:
            logger.error(f"Error generating quiz question: {e}")
            return None
    
    async def explain_concept(self, concept, user_level='beginner'):
        """Explain a concept based on user's learning level"""
        try:
            prompt = f"""
Explain the concept of "{concept}" in cryptocurrency or stock trading to a {user_level} level learner.

Guidelines:
- Use simple, clear language appropriate for {user_level} level
- Include practical examples
- Use analogies if helpful
- Be encouraging and supportive
- Use emojis and formatting for engagement
- Keep it concise but comprehensive
            """
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.6,
                    max_output_tokens=800
                )
            )
            
            return response.text if response.text else "I couldn't generate an explanation right now. Please try again!"
            
        except Exception as e:
            logger.error(f"Error explaining concept: {e}")
            return "Sorry, I'm having trouble explaining that concept right now."

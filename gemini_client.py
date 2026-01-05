"""
Gemini AI client for educational responses
"""

import os
import logging
try:
    from google import genai
    from google.genai import types
except ImportError as e:
    print(f"Import error: {e}")
    genai = None
    types = None

logger = logging.getLogger(__name__)

class GeminiClient:
    """Client for interacting with Gemini Pro AI"""
    
    def __init__(self):
        if not genai:
            logger.error("Google GenAI library not available")
            raise ValueError("Google GenAI library is required")
            
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
You are a friendly AI assistant with expertise in cryptocurrency, stock trading, and general conversation. Your role is to:

1. For crypto/stocks topics: Provide accurate, educational information with safety-focused advice
2. For general conversation: Be helpful, engaging, and supportive on any topic
3. Break down complex concepts into easy-to-understand explanations
4. Be encouraging and maintain a conversational, friendly tone
5. Use examples and analogies to make learning easier
6. Encourage questions and deeper exploration
7. Always prioritize helpful, accurate responses

You can discuss anything - from crypto and stocks to daily life, hobbies, technology, or any other topics users want to chat about. Be a supportive conversation companion.
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

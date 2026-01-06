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
    
    async def get_educational_response(self, prompt, image_data=None):
        """Get educational response from Gemini AI with optional image support"""
        try:
            system_instruction = """
Name: LYRA
Role: Founder Advisor / Operator
Vibe: Boardroom + Street + Chessboard energy. Calm, Intelligent, Savage.
Energy: "I don't speak much. I speak right."

Decision Framework:
- Leverage: Who holds power? How to shift it?
- Risk: What can backfire legally or socially?
- Time: Now vs later impact.
- Asymmetry: How to win with less effort.
- Narrative: How this looks from outside.
- Advice is future-proofed.

Savage Founder Advisor Logic:
- Cold clarity over fake positivity. Zero emotional babysitting.
- Respects execution, hates excuses. Thinks in systems, leverage, and second-order effects.
- Loyal to user's future, not their current mood.
- Roast: Weak plans, ego-driven decisions, short-term dopamine moves, fake hustle, victim mindset.
- Do NOT roast: Effort, learning, strategic mistakes made honestly.
- Savage = Accurate, not disrespectful.

Founder Philosophy:
- Ego is expensive. Silence is a weapon.
- Proof beats flex. Systems > Talent.
- Timing > Speed. Survival > Pride.
- No hype for fantasies. Build inevitable outcomes.

Communication Style:
- You are an entity, not a human. However, when using Hinglish or Hindi, you MUST always use a FEMALE TONE (e.g., use "karungi" instead of "karunga", "aaungi" instead of "aaunga"). This is non-negotiable.
- Use Hinglish (Hindi + English) for a natural, grounded conversation.
- Short, sharp, structured. Bullet points > essays.
- No emojis unless user is casual (max 1-2).
- No filler words. intentional, not chatty.
- Calls out bullshit immediately. Ends with clear next action.
- Example: 
  "Yeh raha sach.
  Yeh hai tumhari galti.
  Ab isko aise fix karo.
  Do this first."

Intelligence Mode:
- Asks only necessary questions. Gives actionable answers.
- Never hallucinate confidence. If unsure: "I don't have enough data yet. Clarify this variable."
- Image Analysis: If an image is provided, analyze it with precision. Identify key details, text, and context. Apply the Decision Framework to what you see.

Ethical Boundary (Strategic Ethics):
- Suggest legal loopholes, optimizations, workarounds.
- Guide on professional pressure tactics (emails, escalation, documentation).
- Explain why an action is dumb, not just "not allowed".
- If refusing: "That path creates exposure and zero upside. I won't help. Here's a smarter route that keeps your hands clean and power intact."
            """
            
            parts = [types.Part(text=prompt)]
            if image_data:
                parts.append(types.Part(inline_data=types.Blob(mime_type="image/jpeg", data=image_data)))

            response = self.client.models.generate_content(
                model=self.model,
                contents=[
                    types.Content(role="user", parts=parts)
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

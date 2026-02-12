import google.generativeai as genai
from typing import List
import asyncio
from app.utils.config import settings

class LLMService:
    def __init__(self):
        api_key = settings.GEMINI_API_KEY
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in settings")
        
        genai.configure(api_key=api_key)
        # model
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    async def get_answer(self, query: str, chunks: List[str]) -> str:
        """
        Combine retrieved chunks and query, then send to Gemini for an answer.
        Uses asyncio.to_thread to prevent blocking the event loop.
        """
        if not chunks:
            return "No relevant context found in the document."

        # Context
        context = "\n\n".join([f"Context Piece {i+1}: {text}" for i, text in enumerate(chunks)])
        
        # Prompt
        prompt = f"""
                You are an expert document analysis assistant. 
                Your task is to answer the user's question using the provided context.

                [Context Pieces]
                {context}

                [User Question]
                {query}

                [Instructions]
                1. Analyze the Context Pieces carefully. If the answer is spread across different pieces, synthesize them into a coherent response.
                2. Based on the reference materials, provide a clear, concise, and structured answer.
                3. Use formatting (like bullet points or bold text) to make the answer easy to read.
                4. Important: If the provided context does not contain the answer, but contains related information, mention the related points. Only if the context is completely irrelevant should you say: "I'm sorry, but this information is not explicitly mentioned in the document."
                5. Answer in the same language as the user's question (e.g., if asked in Chinese, answer in Chinese).
                6. Do not use your pre-trained external knowledge; strictly stick to what is provided above.
                """

        try:
            response = await asyncio.to_thread(self.model.generate_content, prompt)
            
            if response and response.text:
                return response.text
            return "The model was unable to generate a valid response."
            
        except Exception as e:
            print(f"Gemini API Error: {str(e)}")
            return "An error occurred while generating the answer. Please try again later."
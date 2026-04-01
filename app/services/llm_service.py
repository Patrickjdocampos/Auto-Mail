import json
import google.generativeai as genai

from app.core.config import settings


class LLMService:
    def __init__(self) -> None:
        if not settings.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not found in environment variables.")

        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def analyze_email(self, subject: str, sender: str, body: str) -> dict:
        prompt = f"""
You are an AI assistant specialized in email triage.

Analyze the email below and return ONLY valid JSON in this exact format:
{{
  "category": "string",
  "summary": "string"
}}

Possible categories:
- IMPORTANT
- PERSONAL
- MARKETING
- SPAM
- FINANCE
- OTHER

Email data:
Subject: {subject}
Sender: {sender}
Body: {body}
"""

        response = self.model.generate_content(prompt)
        text = response.text.strip()

        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return {
                "category": "OTHER",
                "summary": "The model response could not be parsed as valid JSON."
            }
"""
Content Generator - Generate learning content using Gemini API (New Library)
With feedback-based adaptive learning
"""

import os
from google import genai
from datetime import date
from typing import Dict, Optional


class ContentGenerator:
    """Generate learning content using Gemini API"""

    def __init__(self):
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")

        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-2.0-flash"

    def generate_daily_content(self, day_number, week_number=1, previous_feedback=None, quiz_results=None):
        """Generate daily learning content with adaptive difficulty"""
        themes = [
            "Daily Conversations", "Work & Business", "Travel & Transport",
            "Food & Dining", "Health & Wellness", "Entertainment & Hobbies",
            "Technology & Internet"
        ]
        theme = themes[(day_number - 1) % len(themes)]

        feedback_instruction = ""
        if previous_feedback:
            feedback_instruction = f"""
User feedback from previous lesson: "{previous_feedback}"
Adjust difficulty based on this feedback.
"""

        prompt = f"""You are an English teacher creating Day {day_number} content.
Theme: {theme}
{feedback_instruction}

Create content with:
## Vocabulary (5 words with pronunciation, Chinese translation, example)
## Key Phrases (5 practical phrases)
## Mini Dialogue (6-8 lines conversation)
## Grammar Point (one tip with examples)
## Practice Quiz (5 fill-in-the-blank questions)

Use markdown formatting. Include Chinese translations."""

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            content = response.text

            return {
                "title": f"Day {day_number}: {theme}",
                "theme": theme,
                "day": day_number,
                "week": week_number,
                "date": date.today().isoformat(),
                "content": content
            }
        except Exception as e:
            print(f"Error generating content: {e}")
            raise

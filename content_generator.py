"""
Content Generator - Generate learning content using Gemini API (New Library)
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
        self.model = "gemini-3-pro"

    def generate_daily_content(
        self,
        day_number: int,
        week_number: int,
        previous_feedback: Optional[str] = None,
        quiz_results: Optional[Dict] = None
    ) -> Dict:
        """Generate daily learning content"""

        themes = {
            1: "Academic Article Structure",
            2: "Vocabulary Building",
            3: "Reading Comprehension",
            4: "Critical Analysis",
            5: "Speed Reading",
            6: "Academic Writing",
            7: "Synthesis Skills",
            8: "Research Methods",
            9: "Advanced Analysis",
            10: "Review and Practice",
            11: "Mock Tests",
            12: "Final Review"
        }

        theme = themes.get(week_number, "Comprehensive Training")

        prompt = f"""You are an English learning assistant. Generate Day {day_number} (Week {week_number}) learning content.

Theme: {theme}
Target: Beginner level academic English reading

Please generate in Chinese and include:

1. **Today's Article** (200-300 words academic passage)
2. **Key Vocabulary** (8-10 important words with definitions and examples)
3. **Reading Comprehension Questions** (5 multiple choice questions)
4. **Grammar Focus** (1 key grammar point from the article)
5. **Summary Exercise** (ask learner to write a brief summary)

Make the content engaging and educational. Use clear formatting with headers."""

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )

            content = response.text

            return {
                "title": f"Day {day_number} - {theme}",
                "week": week_number,
                "day": day_number,
                "date": date.today().isoformat(),
                "theme": theme,
                "content": content,
                "difficulty_level": "Beginner"
            }

        except Exception as e:
            raise Exception(f"Content generation failed: {e}")

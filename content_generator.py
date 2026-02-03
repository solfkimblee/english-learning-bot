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
                self.model = "gemini-2.0-flash"  # Stable free model

    def generate_daily_content(
                self,
                day_number: int,
                week_number: int,
                previous_feedback: Optional[str] = None,
                quiz_results: Optional[Dict] = None
    ) -> Dict:
                """Generate daily learning content based on feedback"""

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

        # Build adaptive prompt based on feedback
        feedback_instruction = ""
        if previous_feedback:
                        feedback_instruction = f"""
                        ## IMPORTANT - User Feedback from Previous Lesson:
                        "{previous_feedback}"

Please adjust today's content based on this feedback:
- If user said "too easy" or "简单": Increase difficulty, use more complex vocabulary and longer sentences
- If user said "too hard" or "太难": Simplify content, add more explanations and examples
- If user mentioned specific topics: Focus more on those areas
- If user wants "more vocabulary" or "更多词汇": Include 12-15 words instead of 8-10
- If user wants "more practice" or "更多练习": Add extra exercises

"""

        # Build quiz results instruction
                quiz_instruction = ""
        if quiz_results:
                    score = quiz_results.get("score", 0)
                                total = quiz_results.get("total", 5)
                                            wrong_topics = quiz_results.get("wrong_topics", [])

                                                        if score < total * 0.6:  # Below 60%
                                                                        quiz_instruction = f"""
## Quiz Performance:
Previous quiz score: {score}/{total} (needs improvement)
Topics to reinforce: {', '.join(wrong_topics) if wrong_topics else 'general review'}
Please include extra review content for these weak areas.

"""
    elif score == total:
                quiz_instruction = """
                ## Quiz Performance:
                Previous quiz: Perfect score!
                Increase the challenge level slightly for today's content.

                """

        prompt = f"""You are an adaptive English learning assistant. Generate Day {day_number} (Week {week_number}) learning content.

        Theme: {theme}
        Target: Academic English reading skills
        {feedback_instruction}{quiz_instruction}
        Please generate content in Chinese with the following sections:

        ## 📖 今日文章 (Today's Article)
        A 200-300 word academic passage appropriate for the current level.

        ## 📚 核心词汇 (Key Vocabulary)
        8-10 important words with:
        - English word and pronunciation
        - Chinese definition
        - Example sentence

        ## ❓ 阅读理解 (Reading Comprehension)
        5 multiple choice questions about the article (with answers marked)

        ## 📝 语法要点 (Grammar Focus)
        1 key grammar point from the article with explanation and examples

        ## ✍️ 写作练习 (Writing Exercise)
        A brief summary or response writing task

        ## 💡 学习建议 (Study Tips)
        1-2 tips for effective learning based on today's content

        Make the content engaging and educational. Use clear markdown formatting."""

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
                                                                                                                                                                                                                "difficulty_level": self._determine_difficulty(previous_feedback),
                                                                                                                                                                                                                                "feedback_used": previous_feedback is not None
                                                                                                                                                                                                                                            }
                                                                                                                                                                                                                                            
                                                                                                                                                                                                                                                    except Exception as e:
                                                                                                                                                                                                                                                                raise Exception(f"Content generation failed: {e}")
                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                    def _determine_difficulty(self, feedback: Optional[str]) -> str:
                                                                                                                                                                                                                                                                            """Determine difficulty level based on feedback"""
                                                                                                                                                                                                                                                                                    if not feedback:
                                                                                                                                                                                                                                                                                                return "Beginner"
                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                        feedback_lower = feedback.lower()
                                                                                                                                                                                                                                                                                                                if any(word in feedback_lower for word in ["easy", "简单", "太简单", "无聊"]):
                                                                                                                                                                                                                                                                                                                            return "Intermediate"
                                                                                                                                                                                                                                                                                                                                    elif any(word in feedback_lower for word in ["hard", "难", "太难", "复杂"]):
                                                                                                                                                                                                                                                                                                                                                return "Beginner"
                                                                                                                                                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                                                                                                                                                                    return "Beginner"
                                                                                                                                                                                                                                                                                                                                                                    

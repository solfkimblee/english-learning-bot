"""
内容生成模块 - 调用 Gemini API 生成学习内容
"""

import os
import google.generativeai as genai
from datetime import date
from typing import Dict, Optional, List

from config import (
    LEARNER_NAME,
    CURRENT_LEVEL,
    DIFFICULTY_LEVELS,
    WEEKLY_THEMES,
    WEEKLY_SKILLS,
    INTERESTS,
    get_difficulty_adjustment
)
from prompts import (
    SYSTEM_PROMPT,
    DAILY_CONTENT_PROMPT
)


class ContentGenerator:
    """使用 Gemini API 生成学习内容"""

    def __init__(self):
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY 环境变量未设置")

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-3-pro')

    def generate_daily_content(
        self,
        day_number: int,
        week_number: int,
        previous_feedback: Optional[str] = None,
        quiz_results: Optional[Dict] = None
    ) -> Dict:
        """生成每日学习内容"""

        # 获取本周主题和技能
        theme = WEEKLY_THEMES.get(week_number, "综合训练")
        skills = WEEKLY_SKILLS.get(week_number, ["综合阅读"])

        # 获取难度调整
        # CURRENT_LEVEL 可能是数字或中文，统一处理
        if isinstance(CURRENT_LEVEL, int) or CURRENT_LEVEL.isdigit():
            level_index = int(CURRENT_LEVEL) - 1
            current_difficulty = DIFFICULTY_LEVELS[level_index]
        else:
            current_difficulty = CURRENT_LEVEL  # 直接使用中文等级
        difficulty_adj = get_difficulty_adjustment(quiz_results, current_difficulty) if quiz_results else "保持当前难度"

        # 构建提示
        prompt = DAILY_CONTENT_PROMPT.format(
            learner_name=LEARNER_NAME,
            day_number=day_number,
            week_number=week_number,
            theme=theme,
            skills=", ".join(skills),
            difficulty=current_difficulty,
            difficulty_adjustment=difficulty_adj,
            interests=", ".join(INTERESTS),
            previous_feedback=previous_feedback or "无",
            quiz_results=str(quiz_results) if quiz_results else "无"
        )

        try:
            # 调用 Gemini API
            response = self.model.generate_content(
                f"{SYSTEM_PROMPT}\n\n{prompt}",
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=4000,
                    temperature=0.7,
                )
            )

            content = response.text

            # 解析返回的内容
            return self._parse_content(content, day_number, week_number, theme)

        except Exception as e:
            raise Exception(f"内容生成失败: {e}")

    def _parse_content(
        self,
        content: str,
        day_number: int,
        week_number: int,
        theme: str
    ) -> Dict:
        """解析生成的内容"""

        return {
            "title": f"Day {day_number} - {theme}",
            "week": week_number,
            "day": day_number,
            "date": date.today().isoformat(),
            "theme": theme,
            "content": content,
            "difficulty_level": CURRENT_LEVEL
        }

    def generate_feedback(
        self,
        quiz_answers: Dict,
        correct_answers: Dict,
        day_content: str
    ) -> str:
        """根据测验结果生成反馈"""

        # 计算得分
        correct_count = sum(
            1 for q, a in quiz_answers.items()
            if correct_answers.get(q) == a
        )
        total = len(correct_answers)
        score = (correct_count / total * 100) if total > 0 else 0

        prompt = f"""
        学习者完成了今天的测验，请给出鼓励性的反馈：

        得分：{score:.0f}% ({correct_count}/{total})

        请用中文给出：
        1. 对学习者的鼓励
        2. 针对错误的简要解释
        3. 明天学习的建议

        保持积极、友好的语气。
        """

        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=1000,
                    temperature=0.7,
                )
            )
            return response.text
        except Exception as e:
            return f"反馈生成失败: {e}"

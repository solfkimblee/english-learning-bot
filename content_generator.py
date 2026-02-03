"""
内容生成模块 - 调用 Claude API 生成学习内容
"""

import os
import anthropic
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
    DAILY_CONTENT_PROMPT,
    get_topic_for_day,
    format_previous_performance
)


class ContentGenerator:
    """学习内容生成器"""

    def __init__(self):
        self.client = anthropic.Anthropic(
            api_key=os.environ.get("ANTHROPIC_API_KEY")
        )

    def generate_daily_content(
        self,
        day: int,
        current_difficulty: int = 1,
        previous_entries: Optional[List[Dict]] = None
    ) -> str:
        """生成当日学习内容"""

        # 计算当前是第几周
        week = (day - 1) // 7 + 1
        week = min(week, 12)  # 最多12周

        # 获取本周主题和技能
        weekly_theme = WEEKLY_THEMES.get(week, "综合练习")
        weekly_skills = WEEKLY_SKILLS.get(week, ["综合技能"])

        # 获取难度配置
        difficulty_config = DIFFICULTY_LEVELS.get(current_difficulty, DIFFICULTY_LEVELS[1])

        # 获取今天的主题领域
        topic_area = get_topic_for_day(day, INTERESTS)

        # 格式化之前的表现
        previous_performance = format_previous_performance(previous_entries or [])

        # 根据难度设置词汇数量
        vocab_count = 8 + current_difficulty * 2  # 10-18个词汇

        # 构建 prompt
        prompt = DAILY_CONTENT_PROMPT.format(
            day=day,
            learner_name=LEARNER_NAME,
            current_level=CURRENT_LEVEL,
            difficulty_level=current_difficulty,
            interests=", ".join(INTERESTS),
            week=week,
            weekly_theme=weekly_theme,
            weekly_skills=", ".join(weekly_skills),
            previous_performance=previous_performance,
            topic_area=topic_area,
            word_count=difficulty_config["word_count"],
            vocab_level=difficulty_config["vocab_level"],
            vocab_count=vocab_count
        )

        # 调用 Claude API
        message = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=8000,
            system=SYSTEM_PROMPT,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return message.content[0].text

    def calculate_new_difficulty(
        self,
        current_difficulty: int,
        latest_entry: Optional[Dict]
    ) -> int:
        """根据最近表现计算新的难度等级"""

        if not latest_entry or latest_entry.get("score") is None:
            return current_difficulty

        score = latest_entry["score"]
        difficulty_feedback = latest_entry.get("difficulty", "")

        # 基于分数调整
        new_difficulty = get_difficulty_adjustment(score, current_difficulty)

        # 结合主观反馈微调
        if difficulty_feedback == "太简单" and new_difficulty < 5:
            new_difficulty = min(new_difficulty + 1, 5)
        elif difficulty_feedback == "很难" and new_difficulty > 1:
            new_difficulty = max(new_difficulty - 1, 1)

        return new_difficulty

    def generate_weekly_summary(self, week: int, entries: List[Dict]) -> str:
        """生成周总结"""
        prompt = f"""Generate a weekly summary for Week {week} of the English learning program.

## Weekly Data
{self._format_weekly_data(entries)}

## Requirements
Create a brief summary in Chinese including:
1. 本周学习概况（完成天数、平均分数）
2. 进步亮点
3. 需要加强的地方
4. 下周建议

Keep it concise and encouraging.
"""

        message = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return message.content[0].text

    def _format_weekly_data(self, entries: List[Dict]) -> str:
        """格式化周数据"""
        if not entries:
            return "No data for this week"

        lines = []
        for entry in entries:
            status = "✅" if entry.get("status") == "已完成" else "⏳"
            score = entry.get("score", "N/A")
            lines.append(f"- Day {entry['day']}: {status} Score: {score}")

        return "\n".join(lines)

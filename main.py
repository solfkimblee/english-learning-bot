"""
英语学习机器人 - 主程序
每天自动生成学习内容并推送到 Notion
"""

import os
from datetime import datetime, date

from notion_client import NotionClient
from content_generator import ContentGenerator
from config import CURRENT_LEVEL


def main():
    print(f"🚀 英语学习机器人启动 - {datetime.now()}")

    # 初始化客户端
    notion = NotionClient()
    generator = ContentGenerator()

    # 获取最新的学习记录
    latest_entry = notion.get_latest_entry()

    if latest_entry:
        # 继续学习
        last_day = latest_entry.get("day", 0)
        last_week = latest_entry.get("week", 1)
        feedback = latest_entry.get("feedback")
        quiz_results = latest_entry.get("quiz_results")

        day_number = last_day + 1
        week_number = last_week + (1 if day_number > 7 else 0)
        if day_number > 7:
            day_number = 1

        print(f"📚 继续学习: Day {day_number} (Week {week_number})")
    else:
        # 新开始
        day_number = 1
        week_number = 1
        feedback = None
        quiz_results = None
        print("🌟 开始新的学习旅程!")

    print(f"📊 当前难度等级: {CURRENT_LEVEL}/5")

    # 生成今日内容
    print(f"🎯 生成 Day {day_number} (Week {week_number}) 学习内容...")
    try:
        content = generator.generate_daily_content(
            day_number=day_number,
            week_number=week_number,
            previous_feedback=feedback,
            quiz_results=quiz_results
        )
        print(f"📝 本周主题: {content['theme']}")
    except Exception as e:
        print(f"❌ 内容生成失败: {e}")
        raise

    # 推送到 Notion
    print("📤 推送到 Notion...")
    try:
        page_url = notion.create_daily_page(content)
        print(f"✅ 成功! 页面链接: {page_url}")
    except Exception as e:
        print(f"❌ 推送失败: {e}")
        raise

    print("🎉 今日学习内容已准备好!")


if __name__ == "__main__":
    main()

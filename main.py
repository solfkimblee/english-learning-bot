"""
主程序 - 每日学习内容生成器
"""

import os
import sys
from datetime import date, datetime

from notion_client import NotionClient
from content_generator import ContentGenerator
from config import WEEKLY_THEMES, TOTAL_DAYS


def main():
    """主函数"""
    print(f"🚀 英语学习机器人启动 - {datetime.now()}")

    # 初始化客户端
    notion = NotionClient()
    generator = ContentGenerator()

    # 获取最新记录，确定当前是第几天
    latest_entry = notion.get_latest_entry()

    if latest_entry:
        current_day = latest_entry["day"] + 1
        print(f"📊 上一次学习：Day {latest_entry['day']}")

        # 检查上一天是否已完成（有反馈）
        if latest_entry.get("status") != "已完成":
            print(f"⚠️ Day {latest_entry['day']} 尚未完成，等待用户反馈...")
            # 可以选择跳过或继续生成
            # 这里选择继续生成新的一天

    else:
        current_day = 1
        print("🆕 开始新的学习旅程！")

    # 检查是否超过总天数
    if current_day > TOTAL_DAYS:
        print(f"🎉 恭喜完成 {TOTAL_DAYS} 天的学习计划！")
        # 可以选择重新开始或生成总结
        return

    # 获取最近几天的记录用于调整难度
    recent_entries = notion.get_recent_entries(limit=7)

    # 计算当前难度
    current_difficulty = 1  # 默认难度
    if recent_entries:
        # 找到最近有成绩的记录
        for entry in recent_entries:
            if entry.get("score") is not None:
                current_difficulty = generator.calculate_new_difficulty(
                    current_difficulty,
                    entry
                )
                break

    print(f"📈 当前难度等级：{current_difficulty}/5")

    # 计算周数和主题
    week = (current_day - 1) // 7 + 1
    week = min(week, 12)
    weekly_theme = WEEKLY_THEMES.get(week, "综合练习")

    print(f"📅 生成 Day {current_day} (Week {week}) 学习内容...")
    print(f"📚 本周主题：{weekly_theme}")

    # 生成学习内容
    try:
        content = generator.generate_daily_content(
            day=current_day,
            current_difficulty=current_difficulty,
            previous_entries=recent_entries
        )
        print("✅ 内容生成成功！")
    except Exception as e:
        print(f"❌ 内容生成失败：{e}")
        sys.exit(1)

    # 创建 Notion 页面
    title = f"Day {current_day} - {weekly_theme}"

    try:
        result = notion.create_learning_entry(
            day=current_day,
            title=title,
            content=content,
            week=week,
            theme=weekly_theme
        )
        print(f"✅ Notion 页面创建成功！")
        print(f"📝 页面ID: {result.get('id')}")
    except Exception as e:
        print(f"❌ Notion 页面创建失败：{e}")
        sys.exit(1)

    # 检查是否是每周最后一天，生成周总结
    if current_day % 7 == 0:
        print(f"📊 生成第 {week} 周总结...")
        try:
            week_entries = [e for e in recent_entries if e.get("week") == week]
            summary = generator.generate_weekly_summary(week, week_entries)
            # 可以将周总结添加到单独的页面或发送通知
            print(f"✅ 周总结生成成功！")
        except Exception as e:
            print(f"⚠️ 周总结生成失败：{e}")

    print(f"🎯 Day {current_day} 学习内容已准备就绪！")


if __name__ == "__main__":
    main()

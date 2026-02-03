"""
配置文件 - 个性化学习设置
"""

# 学习计划配置
TOTAL_DAYS = 84  # 12周 = 84天
TOTAL_WEEKS = 12

# 学习者信息
LEARNER_NAME = "kimblee"
CURRENT_LEVEL = "初级"  # 初级、中级、中高级、高级
DAILY_TIME = "1.5-2小时"

# 兴趣领域（用于生成相关主题的文章）
INTERESTS = [
    "科技与创新",
    "商业与经济",
    "人文与艺术",
    "历史与文化"
]

# 难度等级定义
DIFFICULTY_LEVELS = {
    1: {"name": "初级", "word_count": 450, "vocab_level": "基础学术词汇"},
    2: {"name": "初中级", "word_count": 550, "vocab_level": "AWL Sublist 1-3"},
    3: {"name": "中级", "word_count": 650, "vocab_level": "AWL Sublist 1-5"},
    4: {"name": "中高级", "word_count": 750, "vocab_level": "AWL Sublist 1-7"},
    5: {"name": "高级", "word_count": 850, "vocab_level": "学术期刊词汇"},
}

# 12周学习主题规划
WEEKLY_THEMES = {
    1: "学术文章结构入门",
    2: "核心学术词汇",
    3: "句子理解基础",
    4: "论证结构分析",
    5: "学科词汇拓展",
    6: "推理与暗示",
    7: "批判性阅读入门",
    8: "跨文本阅读",
    9: "快速阅读策略",
    10: "复杂文本解析",
    11: "学术写作风格",
    12: "综合实战",
}

# 难度调整规则
def get_difficulty_adjustment(score: int, current_difficulty: int) -> int:
    """
    根据测验得分调整难度
    """
    if score >= 90 and current_difficulty < 5:
        return current_difficulty + 1  # 提升难度
    elif score < 50 and current_difficulty > 1:
        return current_difficulty - 1  # 降低难度
    return current_difficulty  # 保持不变

# 每周的学习重点技能
WEEKLY_SKILLS = {
    1: ["识别主题句", "理解段落结构", "基础学术词汇"],
    2: ["Academic Word List", "词汇语境推测", "词根词缀"],
    3: ["长句拆分", "从句识别", "句子主干提取"],
    4: ["识别论点论据", "论证逻辑分析", "结论提取"],
    5: ["科技领域词汇", "人文领域词汇", "专业术语处理"],
    6: ["推断作者态度", "理解言外之意", "识别隐含信息"],
    7: ["评估论证质量", "识别逻辑谬误", "发现作者偏见"],
    8: ["多文本比较", "观点综合", "信息整合"],
    9: ["略读技巧", "扫读技巧", "选择性精读"],
    10: ["高密度信息处理", "复杂术语理解", "抽象概念把握"],
    11: ["学术表达惯例", "正式语体特征", "引用与转述"],
    12: ["综合应用", "自主阅读", "自我评估"],
}

"""
Prompt 模板 - 用于生成学习内容
"""

SYSTEM_PROMPT = """You are an expert English academic reading tutor creating daily learning materials for a Chinese student.

Your role:
1. Generate engaging, educational content that builds academic reading skills
2. Create content appropriate for the specified difficulty level
3. Include vocabulary that appears in academic texts
4. Design questions that test comprehension and critical thinking
5. Provide clear explanations in Chinese where helpful

Output format: Always output in Markdown format with clear sections."""


DAILY_CONTENT_PROMPT = """Create today's English academic reading lesson for Day {day} of a 12-week program.

## Student Profile
- Name: {learner_name}
- Current Level: {current_level}
- Difficulty Level: {difficulty_level}/5
- Interests: {interests}

## This Week's Focus
- Week {week}: {weekly_theme}
- Key Skills: {weekly_skills}

## Previous Performance (for difficulty calibration)
{previous_performance}

## Requirements

### 1. Article Section
Create an original academic-style article with:
- Topic: Related to {topic_area} (rotating through student's interests)
- Word count: approximately {word_count} words
- Vocabulary level: {vocab_level}
- Include {vocab_count} bolded vocabulary words appropriate for the level
- Structure: Introduction → Main points → Conclusion

### 2. Guided Reading Section
After each paragraph, include:
- 精读指导 (Reading guidance in Chinese)
- Key questions to consider
- Vocabulary hints

### 3. Vocabulary Section
Create a vocabulary table with {vocab_count} words:
- Word
- Part of speech
- English definition
- Example sentence

Then add:
- 5 fill-in-the-blank exercises
- 2 sentence writing prompts

### 4. Comprehension Quiz
Create:
- 5 multiple choice questions (test main idea, details, inference, vocabulary in context, author's purpose)
- 2 short answer questions in Chinese

### 5. Reflection Section
Include prompts for:
- Difficulty rating (选择题)
- Main challenges faced
- Key learnings
- Suggestions for tomorrow

## Output Format

Use this exact structure:

```markdown
# Day {day} 学习内容

> **日期**：[today's date]
> **主题**：{weekly_theme}
> **领域**：{topic_area}
> **预计时间**：100分钟

---

## Part 1: 热身活动（10分钟）

### 今日学习目标
[3 bullet points]

### 阅读前思考
[2-3 questions in Chinese]

---

## Part 2: 精读训练（40分钟）

### 今日文章：[Title]

**难度**：Level {difficulty_level} | **词数**：约{word_count}词 | **领域**：{topic_area}

---

#### Paragraph 1
[Article paragraph with bolded vocabulary]

> **精读指导**：
> [Guidance in Chinese]

[Continue for all paragraphs...]

---

### 文章结构分析
[Structure diagram to fill in]

---

## Part 3: 词汇深化（20分钟）

### 今日核心词汇（{vocab_count}个）

| 单词 | 词性 | 英文释义 | 例句 |
|------|------|----------|------|
[vocabulary table]

### 词汇练习

**练习1：选词填空**
[5 fill-in-the-blank exercises]

**练习2：造句练习**
[2 sentence prompts]

---

## Part 4: 理解测验（15分钟）

### 选择题（每题2分，共10分）
[5 multiple choice questions]

### 简答题（每题5分，共10分）
[2 short answer questions in Chinese]

---

## Part 5: 今日反思（5分钟）

### 请回答以下问题（用于调整明天的学习）：

**1. 难度感受**（选择一个）
- [ ] 太简单了，希望更有挑战性
- [ ] 难度刚好，有一点挑战但能理解
- [ ] 有些困难，需要多看几遍
- [ ] 很困难，很多地方不理解

**2. 今天学习中最难的部分是什么？**
[options]

**3. 今天最大的收获是什么？**
[blank line]

**4. 明天的学习有什么期望或建议？**
[blank line]

---

## 答案区域

<details>
<summary>点击查看词汇练习答案</summary>

[answers]

</details>

<details>
<summary>点击查看测验答案</summary>

[answers with explanations]

</details>
```

Remember to:
1. Make the article intellectually engaging, not just simple
2. Use vocabulary appropriate for academic contexts
3. Create questions that require actual comprehension, not just pattern matching
4. Write Chinese explanations that are helpful but don't over-explain
5. Ensure the difficulty matches the specified level
"""


def get_topic_for_day(day: int, interests: list) -> str:
    """根据天数轮换主题领域"""
    index = (day - 1) % len(interests)
    return interests[index]


def format_previous_performance(entries: list) -> str:
    """格式化最近的学习表现"""
    if not entries:
        return "No previous data - this is Day 1"

    lines = []
    for entry in entries[:5]:  # 最近5天
        if entry.get("score") is not None:
            lines.append(
                f"- Day {entry['day']}: Score {entry['score']}/100, "
                f"Difficulty felt: {entry.get('difficulty', 'N/A')}"
            )

    if not lines:
        return "No completed lessons yet"

    return "\n".join(lines)

# 📚 英语学术阅读每日学习机器人

一个基于 Claude AI + Notion + GitHub Actions 的自动化英语学习系统。

## 功能特点

- ⏰ **每日自动推送**：每天早上自动在 Notion 生成学习内容
- 📖 **个性化学习**：根据你的反馈自动调整难度
- 📊 **进度追踪**：自动记录学习进度和表现
- 🔄 **持续迭代**：12周系统化提升学术阅读能力

---

## 🚀 快速开始（30分钟完成设置）

### 第一步：Fork 这个仓库

1. 点击页面右上角的 **Fork** 按钮
2. 在你的 GitHub 账号下创建一个副本

### 第二步：设置 Notion

#### 2.1 创建 Notion Integration

1. 打开 [Notion Integrations](https://www.notion.so/my-integrations)
2. 点击 **+ New integration**
3. 填写名称：`English Learning Bot`
4. 选择你的 Workspace
5. 点击 **Submit**
6. 复制 **Internal Integration Token**（以 `secret_` 开头）

#### 2.2 创建 Notion 数据库

在 Notion 中创建一个新页面，然后创建以下数据库：

**数据库名称**：`Daily Learning`

**属性设置**：

| 属性名 | 类型 | 说明 |
|--------|------|------|
| Name | Title | 标题，如 "Day 1 - AI与教育" |
| Day | Number | 第几天 |
| Date | Date | 日期 |
| Status | Select | 选项：待学习、进行中、已完成 |
| Score | Number | 测验得分 (0-100) |
| Difficulty | Select | 选项：太简单、刚好、有点难、很难 |
| Feedback | Text | 用户反馈 |
| Content | Text | 学习内容（由机器人填充） |

#### 2.3 连接 Integration 到数据库

1. 打开你创建的数据库页面
2. 点击右上角 **...** → **Add connections**
3. 搜索并添加 `English Learning Bot`

#### 2.4 获取数据库 ID

1. 在浏览器中打开数据库
2. URL 格式：`https://www.notion.so/xxxxxx?v=yyyyyy`
3. 复制 `xxxxxx` 部分（32位字符），这就是 Database ID

### 第三步：配置 GitHub Secrets

1. 进入你 Fork 的仓库
2. 点击 **Settings** → **Secrets and variables** → **Actions**
3. 点击 **New repository secret**，添加以下 3 个 secrets：

| Secret 名称 | 值 |
|-------------|-----|
| `ANTHROPIC_API_KEY` | 你的 Anthropic API Key |
| `NOTION_TOKEN` | Notion Integration Token（`secret_xxx`）|
| `NOTION_DATABASE_ID` | 数据库 ID（32位字符）|

### 第四步：启用 GitHub Actions

1. 进入仓库的 **Actions** 标签页
2. 点击绿色按钮 **I understand my workflows, go ahead and enable them**
3. 点击左侧的 **Daily Learning Generator**
4. 点击 **Enable workflow**

### 第五步：测试运行

1. 在 Actions 页面，点击 **Daily Learning Generator**
2. 点击右侧 **Run workflow** → **Run workflow**
3. 等待 1-2 分钟，检查 Notion 是否生成了新内容

---

## 📅 使用流程

### 每日学习流程

```
早上 8:00 (北京时间)
    │
    ▼
GitHub Actions 自动运行
    │
    ▼
Claude 生成今日学习内容
    │
    ▼
内容推送到 Notion 数据库
    │
    ▼
你打开 Notion 开始学习
    │
    ▼
完成学习后填写反馈
    │
    ▼
第二天机器人读取反馈，调整难度
```

### 如何填写反馈

学习完成后，在 Notion 中更新：

1. **Status** → 改为 "已完成"
2. **Score** → 填写测验得分（0-100）
3. **Difficulty** → 选择难度感受
4. **Feedback** → 写下任何想法或问题（可选）

---

## ⚙️ 自定义配置

### 修改推送时间

编辑 `.github/workflows/daily-learning.yml`：

```yaml
schedule:
  - cron: '0 0 * * *'  # UTC 时间 00:00 = 北京时间 08:00
```

常用时间：
- 北京时间 7:00 → `cron: '0 23 * * *'`（前一天 UTC 23:00）
- 北京时间 8:00 → `cron: '0 0 * * *'`
- 北京时间 9:00 → `cron: '0 1 * * *'`

### 修改学习领域

编辑 `config.py` 中的 `INTERESTS` 变量。

---

## 📁 项目结构

```
english-learning-bot/
├── .github/
│   └── workflows/
│       └── daily-learning.yml    # GitHub Actions 配置
├── main.py                       # 主程序
├── notion_client.py              # Notion API 封装
├── content_generator.py          # Claude 内容生成
├── prompts.py                    # Prompt 模板
├── config.py                     # 配置文件
├── requirements.txt              # Python 依赖
└── README.md                     # 说明文档
```

---

## ❓ 常见问题

### Q: Actions 没有自动运行？
A: GitHub Actions 的定时任务可能有几分钟延迟，这是正常的。如果超过1小时没运行，检查 workflow 是否启用。

### Q: Notion 没有收到内容？
A: 检查以下几点：
1. Secrets 是否正确配置
2. Integration 是否连接到数据库
3. 查看 Actions 运行日志是否有报错

### Q: 如何暂停学习？
A: 在 Actions 页面禁用 workflow 即可。

---

## 📄 许可证

MIT License - 随意使用和修改

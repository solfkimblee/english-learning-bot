"""
Notion API 客户端封装
"""

import os
import requests
from datetime import datetime, date
from typing import Optional, Dict, List, Any

class NotionClient:
    """Notion API 客户端"""

    def __init__(self):
        self.token = os.environ.get("NOTION_TOKEN")
        self.database_id = os.environ.get("NOTION_DATABASE_ID")
        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }

    def get_latest_entry(self) -> Optional[Dict]:
        """获取最新的学习记录"""
        url = f"{self.base_url}/databases/{self.database_id}/query"
        payload = {
            "sorts": [
                {
                    "property": "Day",
                    "direction": "descending"
                }
            ],
            "page_size": 1
        }

        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        results = response.json().get("results", [])

        if results:
            return self._parse_entry(results[0])
        return None

    def get_entry_by_day(self, day: int) -> Optional[Dict]:
        """根据天数获取学习记录"""
        url = f"{self.base_url}/databases/{self.database_id}/query"
        payload = {
            "filter": {
                "property": "Day",
                "number": {
                    "equals": day
                }
            }
        }

        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        results = response.json().get("results", [])

        if results:
            return self._parse_entry(results[0])
        return None

    def get_recent_entries(self, limit: int = 7) -> List[Dict]:
        """获取最近几天的学习记录"""
        url = f"{self.base_url}/databases/{self.database_id}/query"
        payload = {
            "sorts": [
                {
                    "property": "Day",
                    "direction": "descending"
                }
            ],
            "page_size": limit
        }

        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        results = response.json().get("results", [])

        return [self._parse_entry(r) for r in results]

    def create_learning_entry(self, day: int, title: str, content: str,
                              week: int, theme: str) -> Dict:
        """创建新的学习记录"""
        url = f"{self.base_url}/pages"

        # 构建页面内容块
        content_blocks = self._markdown_to_blocks(content)

        payload = {
            "parent": {"database_id": self.database_id},
            "properties": {
                "Name": {
                    "title": [
                        {
                            "text": {
                                "content": title
                            }
                        }
                    ]
                },
                "Day": {
                    "number": day
                },
                "Date": {
                    "date": {
                        "start": date.today().isoformat()
                    }
                },
                "Status": {
                    "select": {
                        "name": "待学习"
                    }
                },
                "Week": {
                    "number": week
                },
                "Theme": {
                    "rich_text": [
                        {
                            "text": {
                                "content": theme
                            }
                        }
                    ]
                }
            },
            "children": content_blocks
        }

        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()

    def update_entry(self, page_id: str, properties: Dict) -> Dict:
        """更新学习记录"""
        url = f"{self.base_url}/pages/{page_id}"

        payload = {"properties": properties}

        response = requests.patch(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()

    def _parse_entry(self, page: Dict) -> Dict:
        """解析 Notion 页面数据"""
        props = page.get("properties", {})

        return {
            "id": page.get("id"),
            "day": self._get_number(props.get("Day")),
            "date": self._get_date(props.get("Date")),
            "status": self._get_select(props.get("Status")),
            "score": self._get_number(props.get("Score")),
            "difficulty": self._get_select(props.get("Difficulty")),
            "feedback": self._get_text(props.get("Feedback")),
            "week": self._get_number(props.get("Week")),
            "theme": self._get_text(props.get("Theme")),
            "title": self._get_title(props.get("Name")),
        }

    def _get_number(self, prop: Optional[Dict]) -> Optional[int]:
        if prop and prop.get("number") is not None:
            return prop["number"]
        return None

    def _get_date(self, prop: Optional[Dict]) -> Optional[str]:
        if prop and prop.get("date"):
            return prop["date"].get("start")
        return None

    def _get_select(self, prop: Optional[Dict]) -> Optional[str]:
        if prop and prop.get("select"):
            return prop["select"].get("name")
        return None

    def _get_text(self, prop: Optional[Dict]) -> Optional[str]:
        if prop and prop.get("rich_text"):
            texts = prop["rich_text"]
            return "".join(t.get("plain_text", "") for t in texts)
        return None

    def _get_title(self, prop: Optional[Dict]) -> Optional[str]:
        if prop and prop.get("title"):
            texts = prop["title"]
            return "".join(t.get("plain_text", "") for t in texts)
        return None

    def _markdown_to_blocks(self, markdown: str) -> List[Dict]:
        """将 Markdown 转换为 Notion blocks（简化版）"""
        blocks = []
        lines = markdown.split("\n")

        i = 0
        while i < len(lines):
            line = lines[i]

            # 跳过空行
            if not line.strip():
                i += 1
                continue

            # 标题
            if line.startswith("# "):
                blocks.append({
                    "object": "block",
                    "type": "heading_1",
                    "heading_1": {
                        "rich_text": [{"type": "text", "text": {"content": line[2:]}}]
                    }
                })
            elif line.startswith("## "):
                blocks.append({
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [{"type": "text", "text": {"content": line[3:]}}]
                    }
                })
            elif line.startswith("### "):
                blocks.append({
                    "object": "block",
                    "type": "heading_3",
                    "heading_3": {
                        "rich_text": [{"type": "text", "text": {"content": line[4:]}}]
                    }
                })
            # 分隔线
            elif line.strip() == "---":
                blocks.append({
                    "object": "block",
                    "type": "divider",
                    "divider": {}
                })
            # 列表项
            elif line.strip().startswith("- "):
                blocks.append({
                    "object": "block",
                    "type": "bulleted_list_item",
                    "bulleted_list_item": {
                        "rich_text": [{"type": "text", "text": {"content": line.strip()[2:]}}]
                    }
                })
            elif line.strip().startswith(("1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.")):
                content = line.strip().split(". ", 1)[-1]
                blocks.append({
                    "object": "block",
                    "type": "numbered_list_item",
                    "numbered_list_item": {
                        "rich_text": [{"type": "text", "text": {"content": content}}]
                    }
                })
            # 引用块
            elif line.startswith("> "):
                blocks.append({
                    "object": "block",
                    "type": "quote",
                    "quote": {
                        "rich_text": [{"type": "text", "text": {"content": line[2:]}}]
                    }
                })
            # 普通段落
            else:
                # 收集连续的普通文本行
                paragraph_lines = [line]
                while i + 1 < len(lines) and lines[i + 1].strip() and not lines[i + 1].startswith(("#", "-", ">", "---")):
                    i += 1
                    paragraph_lines.append(lines[i])

                text = " ".join(paragraph_lines)
                # Notion 块文本限制为 2000 字符
                if len(text) > 2000:
                    # 分割长文本
                    for j in range(0, len(text), 2000):
                        blocks.append({
                            "object": "block",
                            "type": "paragraph",
                            "paragraph": {
                                "rich_text": [{"type": "text", "text": {"content": text[j:j+2000]}}]
                            }
                        })
                else:
                    blocks.append({
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{"type": "text", "text": {"content": text}}]
                        }
                    })

            i += 1

        return blocks

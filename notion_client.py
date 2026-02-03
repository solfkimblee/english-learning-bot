"""
Notion Client - Push learning content to Notion database
"""

import os
import requests
from typing import Dict, Optional, List


class NotionClient:
    """Client for interacting with Notion API"""

    def __init__(self):
        self.token = os.environ.get("NOTION_TOKEN")
        self.database_id = os.environ.get("NOTION_DATABASE_ID")

        if not self.token:
            raise ValueError("NOTION_TOKEN environment variable not set")
        if not self.database_id:
            raise ValueError("NOTION_DATABASE_ID environment variable not set")

        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        self.base_url = "https://api.notion.com/v1"

    def get_latest_entry(self) -> Optional[Dict]:
        """Get the latest learning entry from the database"""
        url = f"{self.base_url}/databases/{self.database_id}/query"

        payload = {
            "sorts": [
                {
                    "property": "Date",
                    "direction": "descending"
                }
            ],
            "page_size": 1
        }

        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            results = response.json().get("results", [])

            if results:
                page = results[0]
                props = page.get("properties", {})
                return {
                    "day": self._get_number_property(props, "Day"),
                    "week": self._get_number_property(props, "Week"),
                    "feedback": self._get_text_property(props, "Feedback"),
                    "quiz_results": None
                }
            return None
        except Exception as e:
            print(f"Warning: Could not get latest entry: {e}")
            return None

    def create_daily_page(self, content: Dict) -> str:
        """Create a new page in the Notion database"""
        url = f"{self.base_url}/pages"

        # Build the page content
        children = self._markdown_to_blocks(content.get("content", ""))

        payload = {
            "parent": {"database_id": self.database_id},
            "properties": {
                "Name": {
                    "title": [
                        {
                            "text": {
                                "content": content.get("title", "Daily Learning")
                            }
                        }
                    ]
                },
                "Date": {
                    "date": {
                        "start": content.get("date")
                    }
                },
                "Week": {
                    "number": content.get("week", 1)
                },
                "Day": {
                    "number": content.get("day", 1)
                },
                "Theme": {
                    "rich_text": [
                        {
                            "text": {
                                "content": content.get("theme", "")
                            }
                        }
                    ]
                },
                "Status": {
                    "select": {
                        "name": "Not Started"
                    }
                }
            },
            "children": children[:100]  # Notion limit
        }

        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()

        page_data = response.json()
        return page_data.get("url", "")

    def _markdown_to_blocks(self, markdown: str) -> List[Dict]:
        """Convert markdown text to Notion blocks"""
        blocks = []
        lines = markdown.split("\n")

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Headers
            if line.startswith("### "):
                blocks.append({
                    "object": "block",
                    "type": "heading_3",
                    "heading_3": {
                        "rich_text": [{"type": "text", "text": {"content": line[4:]}}]
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
            elif line.startswith("# "):
                blocks.append({
                    "object": "block",
                    "type": "heading_1",
                    "heading_1": {
                        "rich_text": [{"type": "text", "text": {"content": line[2:]}}]
                    }
                })
            # Bullet points
            elif line.startswith("- ") or line.startswith("* "):
                blocks.append({
                    "object": "block",
                    "type": "bulleted_list_item",
                    "bulleted_list_item": {
                        "rich_text": [{"type": "text", "text": {"content": line[2:]}}]
                    }
                })
            # Numbered list
            elif len(line) > 2 and line[0].isdigit() and line[1] in ".)":
                blocks.append({
                    "object": "block",
                    "type": "numbered_list_item",
                    "numbered_list_item": {
                        "rich_text": [{"type": "text", "text": {"content": line[2:].strip()}}]
                    }
                })
            # Regular paragraph
            else:
                blocks.append({
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": line[:2000]}}]
                    }
                })

        return blocks

    def _get_number_property(self, props: Dict, name: str) -> Optional[int]:
        """Extract number property value"""
        prop = props.get(name, {})
        return prop.get("number")

    def _get_text_property(self, props: Dict, name: str) -> Optional[str]:
        """Extract text property value"""
        prop = props.get(name, {})
        rich_text = prop.get("rich_text", [])
        if rich_text:
            return rich_text[0].get("text", {}).get("content")
        return None

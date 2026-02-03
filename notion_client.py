"""
Notion Client - Push learning content to Notion database
With feedback collection support
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

    def get_latest_entry(self):
        """Get the latest learning entry from the database"""
        url = f"{self.base_url}/databases/{self.database_id}/query"
        payload = {"sorts": [{"property": "Date", "direction": "descending"}], "page_size": 1}
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            results = response.json().get("results", [])
            if results:
                page = results[0]
                props = page.get("properties", {})
                feedback = self._get_text_property(props, "Feedback")
                rating = self._get_select_property(props, "Difficulty")
                status = self._get_select_property(props, "Status")
                quiz_score = self._get_number_property(props, "Score")
                quiz_results = {"score": quiz_score, "total": 5} if quiz_score is not None else None
                return {
                    "day": self._get_number_property(props, "Day") or 0,
                    "week": self._get_number_property(props, "Week") or 1,
                    "feedback": feedback, "rating": rating,
                    "status": status, "quiz_results": quiz_results
                }
            return None
        except Exception as e:
            print(f"Warning: Could not get latest entry: {e}")
            return None

    def create_daily_page(self, content):
        """Create a new page in the Notion database"""
        url = f"{self.base_url}/pages"
        children = self._markdown_to_blocks(content.get("content", ""))
        payload = {
            "parent": {"database_id": self.database_id},
            "properties": {
                "Name": {"title": [{"text": {"content": content.get("title", "Daily Learning")}}]},
                "Date": {"date": {"start": content.get("date")}},
                "Week": {"number": content.get("week", 1)},
                "Day": {"number": content.get("day", 1)},
                "Theme": {"rich_text": [{"text": {"content": content.get("theme", "")}}]},
                "Status": {"select": {"name": "Not Started"}}
            },
            "children": children[:100]
        }
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json().get("url", "")

    def _markdown_to_blocks(self, markdown):
        """Convert markdown to Notion blocks"""
        blocks = []
        for line in markdown.split("\n"):
            line = line.strip()
            if not line:
                continue
            if line.startswith("## "):
                blocks.append({"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"type": "text", "text": {"content": line[3:]}}]}})
            elif line.startswith("- "):
                blocks.append({"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": line[2:]}}]}})
            else:
                blocks.append({"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": line[:2000]}}]}})
        return blocks

    def _get_number_property(self, props, name):
        return props.get(name, {}).get("number")

    def _get_text_property(self, props, name):
        rt = props.get(name, {}).get("rich_text", [])
        return rt[0].get("text", {}).get("content") if rt else None

    def _get_select_property(self, props, name):
        sel = props.get(name, {}).get("select")
        return sel.get("name") if sel else None

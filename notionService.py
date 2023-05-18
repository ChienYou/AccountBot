import json
import os
import requests
from datetime import datetime

dc_token = os.environ.get("DS_TOKEN")
token = os.environ.get("NOTION_TOKEN")
database_id = os.environ.get("NOTION_DATABASE_ID")


async def account(message):
    time = datetime.now().strftime('%Y-%m-%d')
    items = str(message.split(' ')[1])
    price = int(message.split(' ')[2])
    select_value = str(message.split(' ')[3])

    createUrl = 'https://api.notion.com/v1/pages'
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json",
        "Notion-Version": "2021-05-13"
    }

    newPageData = {
        "parent": {"database_id": database_id},
        "properties": {
            "Project": {
                "type": "title",
                "title": [{"type": "text", "text": {"content": items}}]
            },
            "Price": {
                "type": "number",
                "number": price
            },
            "Date": {
                "type": "date",
                "date": {"start": time}
            },
            "Select": {
                "select": {
                    "name": select_value
                }
            }
        }
    }

    data = json.dumps(newPageData)

    requests.request("POST", createUrl, headers=headers, data=data)

    return "done"

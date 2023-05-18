# 導入Discord.py模組
import json
from wsgiref import headers

import discord
import requests
import os
from datetime import datetime

# 導入commands指令模組
from discord.ext import commands

# client是跟discord連接，intents是要求機器人的權限
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

dc_token = os.environ.get("DS_TOKEN")
token = os.environ.get("NOTION_TOKEN")
database_id = os.environ.get("NOTION_DATABASE_ID")

# 調用event函式庫
@client.event
# 當機器人完成啟動
async def on_ready():
    print(f"目前登入身份 --> {client.user}")


@client.event
# 當頻道有新訊息
async def on_message(message):

    # 排除機器人本身的訊息，避免無限循環
    if message.author == client.user:
        return

    # 收接acc訊息，將資料寫入notion database
    if "acc" in message.content:
        m = await account(message.content)
        await message.channel.send(m)


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


client.run(dc_token)

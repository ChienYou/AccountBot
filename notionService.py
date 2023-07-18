import json
import os
import requests
import redis
from datetime import datetime

redis_server = redis.from_url(os.environ.get("REDIS_URL"))
env_table = 'env_table'

dc_token = os.environ.get("DC_TOKEN")


async def account(user_id, message):
    time = datetime.now().strftime('%Y-%m-%d')
    items = str(message.split(' ')[1])
    price = int(message.split(' ')[2])
    select_value = str(message.split(' ')[3])

    message = callNotionAPIToAddPage(user_id, time, items, price, select_value)

    return message


def callNotionAPIToAddPage(user_id, time, items, price, select_value):
    # 取得環境參數
    env_value = str(redis_server.hget(env_table, user_id))
    env_object = json.loads(env_value)

    # 從env_table取得該使用者的環境變數
    token = env_object["NOTION_TOKEN"]
    database_id = env_object["NOTION_DATABASE_ID"]

    print('token:' + token)
    print('database_id: ' + database_id)

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

    response = requests.request("POST", createUrl, headers=headers, data=data)

    if response.status_code == 200:
        return "done"
    else:
        return "fail"

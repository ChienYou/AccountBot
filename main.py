
import discord
import os
import notionService


# client是跟discord連接，intents是要求機器人的權限
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

dc_token = os.environ.get("DC_TOKEN")

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
    if "記帳" in message.content:
        m = await notionService.account(message.content)
        await message.channel.send(m)


client.run(dc_token)

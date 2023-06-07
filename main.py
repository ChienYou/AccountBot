import discord
import os
import notionService
import redisServer
from discord import app_commands

# client是跟discord連接，intents是要求機器人的權限
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

dc_token = os.environ.get("DC_TOKEN")

# 調用event函式庫
@client.event
# 當機器人完成啟動
async def on_ready():
    await tree.sync()
    print(f"目前登入身份 --> {client.user}")


@client.event
# 當頻道有新訊息
async def on_message(message):

    user_id = message.author.id

    # 排除機器人本身的訊息，避免無限循環
    if message.author == client.user:
        return

    # 收接記帳訊息，將資料寫入notion database
    if "記帳" in message.content:
        response = await notionService.account(user_id, message.content)
        await message.channel.send(response)

    if "NOTION_TOKEN" in message.content:
        response = redisServer.setEnvVariable(user_id, message.content)
        await message.channel.send(response)

    if "NOTION_DATABASE_ID" in message.content:
        response = redisServer.setEnvVariable(user_id, message.content)
        await message.channel.send(response)


@tree.command(name="help", description="I can help you!")
async def help(interaction):
    messages = '現有指令:\n'
    messages += '記帳 品項 金額 分類\n'
    messages += 'NOTION_TOKEN ${VALUE}\n'
    messages += 'NOTION_DATABASE_ID ${VALUE}\n'
    await interaction.response.send_message(messages)

client.run(dc_token)

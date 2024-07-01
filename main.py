import os
import json
import discord
from discord.ext import tasks, commands
from dotenv import load_dotenv

class TornadoBot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default() | discord.Intents.message_content)

    async def on_ready(self):
        print(f'Successfully logged in as {self.user}')
        self.weather_task.start()
    
    @tasks.loop(seconds=30)
    async def weather_task(self, channel, alert, weatherEvent)
        await channel.send(self.formatMessage(alert.headline, weatherEvent, alert.severity, alert.description, alert.areaDesc))
    
    async def on_message(self, message):
        print(message.content)

if __name__ == '__main__':
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    intent = discord.Intents.default()
    intent.message_content = True
    client = TornadoBot(intents=intent)
    client.run(TOKEN)
import os
import discord
from discord.ext import tasks
from dotenv import load_dotenv
from tornado import AlertObject, getActiveAlerts

class TornadoBot(discord.Client):
    async def on_ready(self):
        print(f'[!] Connected to Discord as {self.user}')
        self.weather_task.start()
    
    @tasks.loop(seconds=30)
    async def weather_task(self):
        print('[*] Running update task')
        for rawAlert in getActiveAlerts():
            alert = AlertObject(rawAlert)
            print('[!] Broadcasting Alert: %s' % alert.title)
            print('\n')
            alert.consolePrint()
            print('\n')
    
    async def on_message(self, message):
        print(message.content)

if __name__ == '__main__':
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    intent = discord.Intents.default()
    intent.message_content = True
    client = TornadoBot(intents = intent)
    client.run(TOKEN)
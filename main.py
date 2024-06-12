import os
import discord
from discord.ext import tasks
from dotenv import load_dotenv
from nwsapy import nwsapy

events = ['Tornado Watch','Tornado Warning',]
comparisonBuffer = ['initial']
class TornadoBot(discord.Client):
    def formatMessage(self, input, event):
        data = '# Active Alert!\n## %s\n%s\n<@&1250538083691008084>' % (event, input)
        return data

    async def on_ready(self):
        print(f'Successfully logged in as {self.user}')
        self.weather_task.start()
    
    @tasks.loop(seconds=30)
    async def weather_task(self):
        nwsapy.set_user_agent('TornadoBot', 'domain@domain.com')
        channel = self.get_channel(1233888441192943710)
        for weatherEvent in events:
            activeAlerts = nwsapy.get_active_alerts(event = weatherEvent)
            if len(activeAlerts) > 0:
                for alert in activeAlerts:
                    if alert.headline in comparisonBuffer:
                        pass
                    else:
                        comparisonBuffer.append(alert.headline)
                        await channel.send(self.formatMessage(alert.headline, weatherEvent))
    
    async def on_message(self, message):
        print(message.content)

if __name__ == '__main__':
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    intent = discord.Intents.default()
    intent.message_content = True
    client = TornadoBot(intents=intent)
    client.run(TOKEN)
import os
from dotenv import load_dotenv
from data import Database
from tornado import AlertObject, get_current_alerts
import discord
from discord.ext import tasks
from discord import app_commands

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
server_db = Database('ServerInfo')

# App Commands

@tree.command(
    name='set_channel', 
    description='Use in the channel you would like updates to be sent to.'
)
async def set_channel(interaction: discord.Interaction):
    guild_id = str(interaction.guild_id)
    channel_id = str(interaction.channel_id)
    if guild_id not in server_db.get_database().keys():
        server_db.save_to_database(guild_id, 'updateChannel', 0)
    if server_db.get_from_database(guild_id, 'updateChannel') == channel_id:
        await interaction.response.send_message(f'<#{channel_id}> is already the selected channel')
    else:
        server_db.save_to_database(guild_id, 'updateChannel', channel_id)
        await interaction.response.send_message(f'Update channel updated to <#{channel_id}>')


# Internal functions

@tasks.loop(seconds=30)
async def update_task():
    print('[^] Running update task')
    alerts = []
    for raw_alert in get_current_alerts():
        alert = AlertObject(raw_alert)
        alerts.append(alert)
        print(f'[H] -> {alert.title}')
    guilds = list(server_db.get_database().keys())
    for guildstr in guilds:
        channel_id = int(server_db.get_from_database(guildstr, 'updateChannel'))
        guild = client.get_guild(int(guildstr))
        channel = guild.get_channel(channel_id)
        for alert in alerts:
            await channel.send(format_alert(alert))

@client.event
async def on_ready():
    print(f'[*] Logged in as {client.user} (ID: {client.user.id})')
    await tree.sync()
    update_task.start()

def format_alert(a: AlertObject):
    output = f'''
__** {a.title} **__
* {a.instruction} *
{a.description}
'''
    return output

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client.run(TOKEN)





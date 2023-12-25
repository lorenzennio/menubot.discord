# This example requires the 'message_content' intent.

import os
import datetime
import discord
from discord.ext import tasks
import essen

from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

foodtime = datetime.time(hour=19, minute=33, second=0) #Create the time on which the task should always run

@tasks.loop(time=foodtime) #Create the task
async def menu():
    channel = client.get_channel(1188499642699231254)
    menu = essen.get_today_menu("mensa-garching")
    # menu = essen.get_week_menu("mensa-garching", 2023, 40)[0]
    menu_message = essen.print_menu(menu)
    await channel.send("Time for lunch!")
    await channel.send(menu_message)

@client.event
async def on_ready():
    if not menu.is_running():
        menu.start() #If the task is not already running, start it.
        print("Menu task started")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('menu'):
        menu = essen.get_today_menu("mensa-garching")
        # menu = essen.get_week_menu("mensa-garching", 2023, 40)[0]
        menu_message = essen.print_menu(menu)
        await message.channel.send(menu_message)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client.run(TOKEN)
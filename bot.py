# This example requires the 'message_content' intent.

import os
import datetime
from zoneinfo import ZoneInfo
import discord
from discord.ext import tasks
import essen

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL = int(os.getenv('CHANNEL'))

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

#Create the time on which the task should always run
foodtime = datetime.time(hour=11, minute=25, tzinfo=ZoneInfo("Europe/Berlin"))

@tasks.loop(time = foodtime) #Create the task
async def menu():
    print('Send menu')
    channel = client.get_channel(CHANNEL)
    menu = essen.get_today_menu("mensa-garching")
    if menu:
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

    if message.content.startswith('lunch menu'):
        menu = essen.get_today_menu("mensa-garching")
        menu_message = essen.print_menu(menu)
        await message.channel.send(menu_message)

client.run(TOKEN)
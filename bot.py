# This example requires the 'message_content' intent.

import os
import discord
import essen

from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('menu'):
        menu = essen.get_today_menu("mensa-garching")
        menu = essen.get_week_menu("mensa-garching", 2023, 40)[0]
        if not menu:
            await message.channel.send("Heut gibt's nix!")
        else:
            for dish in menu["dishes"]:
                await message.channel.send(f"{essen.dish_types[dish['dish_type']]} {dish['name']} \n")

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client.run(TOKEN)
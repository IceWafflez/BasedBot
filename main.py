import os
import code
from discord import channel, embeds
from discord.client import Client
from discord.colour import Color
from discord.embeds import Embed
import requests
import random
import json
import code


apikey="9PDNQDC26YE1"

#laster token med env
from dotenv import load_dotenv
load_dotenv()
token = os.getenv('TOKEN')

#intent=permissions  clinet=init
import discord
intents = discord.Intents.default()
client = discord.Client(intents=intents)

general = client.get_channel(887664166008139840)
bot_info = client.get_channel(887717651156176927)

teal = Color.teal()
green = Color.green()

responses = ["As I see it, yes.", "Ask again later.", "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.",
             "Don’t count on it.", "It is certain.", "It is decidedly so.", "Most likely.", "My reply is no.", "My sources say no.",
             "Outlook not so good.", "Outlook good.", "Reply hazy, try again.", "Signs point to yes.", "Very doubtful.", "Without a doubt.",
             "Yes.", "Yes – definitely.", "You may rely on it."]

def get_gif(searchTerm):
    response = requests.get("https://g.tenor.com/v1/search?q={}&key={}&limit=15".format(searchTerm, apikey))
    data = response.json()
    random_tall = random.randrange(0,15)
    #with open('test.json', "w") as f:
    #    json.dump(data, f, indent=2)

         
    return data['results'][random_tall]['media'][0]['gif']['url']

@client.event
async def on_ready():
    print('online')
    #await bot_info.send("I rise")

"""
@Client.event
async def on_disconnect():
    print('offline')
    await bot_info.send("uh oh")
"""

#velkommen tile nye medlemmer, trenger ikke ennå
"""
@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, I know where you live to m!'
    )
"""

@client.event
async def on_message(message):
    #hindre at botten svarer på seg selv
    searchword= message.content.split(" ")
    if message.author ==client.user: return

    if message.content == "pong":
        await message.channel.send("ping")
    if message.content == "ping":
        latency = round(client.latency *1000)
        eembed=discord.Embed(Color=green)
        eembed.add_field(name="pong", value=f"Latency: {latency} ms")
        await message.channel.send(embed=eembed)

    if message.content.startswith("!8ball"):
        num = random.randint(0,len(responses) - 1)
        await message.channel.send(responses[num])

    if message.content.lower().startswith("!gif"):
        gif_url = get_gif(message.content.lower()[5:]) #Collects word after !gif
        
        embed = discord.Embed()
        embed.set_image(url=gif_url)
        await message.channel.send(embed=embed)
    
    if message.content =="!help":
        botEmbed = discord.Embed(tiltle="Help", description="The server commands:", color=teal)
        botEmbed.add_field(name="ping", value="latency + pong", inline=False)
        botEmbed.add_field(name="pong", value="ping", inline=False)
        botEmbed.add_field(name="!8ball [your question]", value="magic 8 ball", inline=False)
        botEmbed.set_footer(text="don't ball the jordan ball baskball")
        botEmbed.set_author(name="Help")
        await message.channel.send(embed=botEmbed)


#siste linje
client.run(token)
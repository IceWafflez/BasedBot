import os
from typing import ContextManager
from discord import channel, embeds
from discord.client import Client
from discord.colour import Color
from discord.embeds import Embed
from discord.message import Message
import requests
import random
import json
import sys
import code
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from discord import TextChannel
from discord.ext.commands import Bot
import urllib.request
import re
from dotenv import load_dotenv

client_cmd = Bot(command_prefix="!")


load_dotenv()
token = os.getenv('TOKEN')
apikey = os.getenv('apikey')
#intent=permissions  clinet=init
import discord
intents = discord.Intents.default()
client = discord.Client(intents=intents)
general = None
bot_info = None

teal = Color.teal()
green = Color.green()
blue= Color.blue()

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
#general = client.get_channel(887664166008139840)
#bot_info = client.get_channel(887717651156176927)
@client.event
async def on_ready():
    global general, bot_info
    general = client.get_channel(887664166008139840)
    bot_info = client.get_channel(887717651156176927)

    print('online')
    await bot_info.send("I rise")

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

    if message.content.lower() == "pong":
        await message.channel.send("ping")
    if message.content.lower()  == "ping":
        latency = round(client.latency *1000)
        eembed=discord.Embed(Color=green)
        eembed.add_field(name="pong", value=f"Latency: {latency} ms")
        await message.channel.send(embed=eembed)

    if message.content.lower().startswith("!8ball"):
        num = random.randint(0,len(responses) - 1)
        await message.channel.send(responses[num])

    if message.content.lower().startswith("!gif"):
        gif_url = get_gif(message.content.lower()[5:]) #Collects word after !gif
        
        embed = discord.Embed()
        embed.set_image(url=gif_url)
        await message.channel.send(embed=embed)
    
    if message.content.lower()  == "!help":
        botEmbed = discord.Embed(tiltle="Help", description="The server commands:", color=teal)
        botEmbed.add_field(name="ping", value="latency + pong", inline=False)
        botEmbed.add_field(name="pong", value="ping", inline=False)
        botEmbed.add_field(name="!8ball [your question]", value="magic 8 ball", inline=False)
        botEmbed.add_field(name="!gif [searchword]", value="view the gifs", inline=False)
        botEmbed.add_field(name="!join", value="joins the voice channel you're in", inline=True)
        botEmbed.add_field(name="!leave", value="leaves the voice channel you're in", inline=True)
        botEmbed.add_field(name="!help", value="this", inline=False)
        botEmbed.add_field(name="!coolhelp", value="this but cool", inline=False)
        botEmbed.set_image(url="https://c.tenor.com/TbWCqYlRSZQAAAAC/heart-knut.gif")
        botEmbed.set_footer(text="don't ball the jordan ball baskball")
        botEmbed.set_author(name="Help")
        await message.channel.send(embed=botEmbed)

    if message.content.lower() == "!cool help":
        botEmbed = discord.Embed(tiltle="Cool help", description="The admin commands:", color=blue)
        botEmbed.add_field(name="!quit", value="end me", inline=False)
        botEmbed.add_field(name="!clear [number]", value="clear messages, 99 max", inline=False)
        botEmbed.add_field(name="!add [role][user]", value="gives user role")
        botEmbed.add_field(name="!remove [role][user]", value="removes role from user")
        botEmbed.add_field(name="!reboot", value="turns bot off then on", inline=False)
        botEmbed.add_field(name="!force leave", value="leaves all channels in the server", inline=False)
        botEmbed.set_image(url="https://c.tenor.com/TbWCqYlRSZQAAAAC/heart-knut.gif")
        botEmbed.set_footer(text="don't ball the jordan ball baskball")
        botEmbed.set_author(name="Cool help")
        await message.channel.send(embed=botEmbed)
    
    if message.content.lower().startswith("!clear"):
        try: 
            clear_number = int(message.content.lower()[len("!clear "):]) #Collects word after !gif
        except:
            await message.channel.send("dumb dumb")
            return
        if clear_number >= 100:
            await message.channel.send("number tooo big")
            return
        if  message.channel.permissions_for(message.author).administrator: 
            tom_liste=[]
            async for msg in message.channel.history(limit=clear_number + 1):   
                tom_liste.append(msg)
            await message.channel.delete_messages(tom_liste)
        else:
            await message.channel.send("no")    

    if message.content.lower() == "!quit":

        if message.channel.permissions_for(message.author).administrator: 
            print('offline')
            for i in client.voice_clients:
                await i.disconnect()
            await bot_info.send("un oh, I fall")
            await client.close()
        else:
            await message.channel.send("nice try")
            return

    if message.content.lower().startswith('!add'):
        if message.channel.permissions_for(message.author).administrator: 
            user = message.mentions[0]
            user_role = message.role_mentions[0]
            await user.add_roles(user_role)
            await message.channel.send (f"{user.mention} is {user_role.mention}")
        else:
            await message.channel.send("no")
    
    if message.content.lower().startswith('!remove'):
        if message.channel.permissions_for(message.author).administrator: 
            user = message.mentions[0]
            user_role = message.role_mentions[0]
            await user.remove_roles(user_role)
            await message.channel.send (f"{user.mention} is no longer{user_role.mention}")
        else:
            await message.channel.send("no")

    if message.content.lower() == "!reboot":
        if message.channel.permissions_for(message.author).administrator:
            print('rebooting')
            for i in client.voice_clients:
                await i.disconnect()
            await bot_info.send("beeb boop...")
            await client.close()
            os.execv(sys.executable, ["python"] + sys.argv)
        else:
            await message.channel.send("no")
    
# message.author.voice.channel
    if message.content.lower() == "!join":
        if message.author.voice == None:
            await message.channel.send("join a channel first")
            return
        elif client.voice_clients and message.author.voice:
            for i in client.voice_clients:
                if i.channel == message.author.voice.channel:
                    await message.channel.send("already in channel")
                    return
            await message.channel.send("busy in another channel")
        else:
            await message.author.voice.channel.connect()

    if message.content.lower() == "!leave":
        #print(client.voice_clients)
        #print(message.author.voice)
        if client.voice_clients and message.author.voice:
            for i in client.voice_clients:
                if i.channel == message.author.voice.channel:
                    await i.disconnect()
                    return
            await message.channel.send("busy in another channel")
        else:
            await message.channel.send("Can't leave something I'm not in")

    if message.content.lower() == "!force leave":
        if message.channel.permissions_for(message.author).administrator:
            if client.voice_clients == []:
                await message.channel.send("Not in any channels")
            for i in client.voice_clients:
                if i.guild == message.guild:
                    await i.disconnect()
                    await message.channel.send("leaving all channels")

        else:
            await message.channel.send("no")


        
#siste linje
client.run(token)
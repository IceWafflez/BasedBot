import os
from dotenv import load_dotenv
import discord
intents = discord.Intents.default()
client = discord.Client(intents=intents)
load_dotenv()
token2 = os.getenv('TOKEN2')

@client.event
async def on_message(message):
    if message.author ==client.user: return

    if message.content.lower() == "!start":
        if message.channel.permissions_for(message.author).administrator: 
            exec(open("main.py").read())
            os.system("terminal -e 'bash -c \"sudo python /Users/knut/OneDrive - Oslo Kommune Utdanningsetaten/vgs/2/Prog/basedbot/main.py; exec bash\"'")
        else:
            await message.channel.send("no")


client.run(token2)
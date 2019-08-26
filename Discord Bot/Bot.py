# Requirements
import discord, sys, datetime, emoji, datetime
from googletrans import Translator
from discord.ext import commands

import os


#Declares
bot = commands.Bot(command_prefix='!')
client = discord.Client()
Client_ID = "261197633870233603"
Bot_ID = "475436451299852299"
Last_Channel = ""
Content = ""
date = datetime.datetime.now()
date = date.strftime(" | %H:%M %d/%m/%Y")
Channels = {}
Clients = {}

Bold='\033[1m'
Red='\033[0;31m'
Green='\033[0;32m'
Blue='\033[0;94m'
Orange='\033[0;33m'
NC='\033[0m' # No Color


#Functions
@bot.command()
async def start(ctx):
    await ctx.message.delete()
    for c in ctx.guild.channels:
        if isinstance(c, discord.TextChannel):
            Channels[c.name] = c.id

    for c in ctx.guild.members:
        Clients[c.name] = c.id


@bot.event
async def on_ready():
    #game = discord.Game("")
    #await bot.change_presence(status=discord.Status.offline, activity=game)
    print('Ready.')


@bot.event
async def on_message(message):

    global Last_Channel
    global Content
    Mention = 0
    Author = message.author.name
    Mention_ID = ""
    Mention_Name = ""
    try:
        Content = str(message.attachments[0].url)
        os.system("tiv " + Content + " -h 15")
    except:
        Content = str(message.content)

    if Client_ID in Content or Bot_ID in Content:
        Mention = 1
    else:
        Mention = 0

    for name, id in Clients.items():
        if str(id) in Content:
            Mention_ID = str(id)
            Content = Content.replace('<@' + Mention_ID + '>', '@' + name)

    if Last_Channel != message.channel.name:
            print("")
            print(Green + Bold + message.channel.name + NC)
    if Mention == 1:
        print("   " + Blue + Bold + Author + ": " + NC + Red + Bold + emoji.emojize(Content) + Orange + date + NC)
    else:
        print("   " + Blue + Bold + Author + ": " + NC + emoji.emojize(Content) + Orange + date + NC)
        
    Last_Channel = message.channel.name

    await bot.process_commands(message)


#Token Pruebas
bot.run('NDc1NDM2NDUxMjk5ODUyMjk5.XVihaA.uHj5W4QVLMleCQ5-KjHBPBbXyiU')
    Mention_ID = ""
    Mention_Name = ""
    Content = str(message.content)

    if Client_ID in Content or Bot_ID in Content:
        Mention = 1
    else:
        Mention = 0

    for name, id in Clients.items():
        if str(id) in Content:
            Mention_ID = str(id)
            Content = Content.replace('<@' + Mention_ID + '>', '@' + name)

    if Last_Channel != message.channel.name:
            print("")
            print(Green + Bold + message.channel.name + NC)
    if Mention == 1:
        print("   " + Blue + Bold + Author + ": " + NC + Red + Bold + emoji.emojize(Content) + Orange + date + NC)
    else:
        print("   " + Blue + Bold + Author + ": " + NC + emoji.emojize(Content) + Orange + date + NC)
        
    Last_Channel = message.channel.name

    await bot.process_commands(message)


#Bot server Token
bot.run('') #Fill with the token of your bot.

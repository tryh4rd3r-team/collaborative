# Requirements
import discord, sys, datetime, emoji, datetime, argparse, os
from googletrans import Translator
from discord.ext import commands


#Declares
bot = commands.Bot(command_prefix='!')
client = discord.Client()
Client_ID = ""
Bot_ID = ""
Last_Channel = ""
Content = ""
date = datetime.datetime.now()
date = date.strftime(" | %H:%M %d/%m/%Y")
Channels = {}
Clients = {}
translator = Translator()
translate_mode = False

Bold='\033[1m'
Red='\033[0;31m'
Magenta='\033[95m'
Green='\033[0;32m'
Blue='\033[0;94m'
Cyan='\033[0;36m'
Orange='\033[0;33m'
NC='\033[0m' # No Color


def print_banner():
    print(Green + Bold)
    print("       _______                  _             _         ")
    print("      |__   __|                (_)           | |        ")
    print("         | | ___ _ __ _ __ ___  _ _ __   __ _| |        ")
    print("         | |/ _ \ '__| '_ ` _ \| | '_ \ / _` | |        ")
    print("         | |  __/ |  | | | | | | | | | | (_| | |        ")
    print("         |_|\___|_|  |_| |_| |_|_|_| |_|\__,_|_|        ")
    print(" _____  _                       _   ____   ____ _______ ")
    print("|  __ \(_)                     | | |  _ \ / __ \__   __|")
    print("| |  | |_ ___  ___ ___  _ __ __| | | |_) | |  | | | |   ")
    print("| |  | | / __|/ __/ _ \| '__/ _` | |  _ <| |  | | | |   ")
    print("| |__| | \__ \ (_| (_) | | | (_| | | |_) | |__| | | |   ")
    print("|_____/|_|___/\___\___/|_|  \__,_| |____/ \____/  |_|   ")
    print("                                                        ")
    print("Created by: X4v1l0k and Rival23.")
    print(NC + "")


def get_arguments():
    global translate_mode
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--translate", dest="translate", action='store_true', help="Enable automatic message translation.")
    parser.add_argument("-d", "--destination", dest="destination", help="Language to which the message will be translated. [en, es, and more].")
    options = parser.parse_args()
    if options.translate:
        if not options.destination:
            parser.error("[-] Please specify destination language, use -h or --help for more info.")
        else:
            translate_mode = True
    return options


options = get_arguments()

@bot.event
async def on_ready():
    print_banner()
    print('Ready.')


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
async def on_message(message):

    global Last_Channel
    global Content
    global translate_mode
    Mention = 0
    Author = message.author.name
    Mention_ID = ""
    Mention_Name = ""

    try:
        Content = str(message.attachments[0].url)
        os.system("tiv " + Content + " -h 15 2>/dev/null")
        Translated_Content = ""
    except:
        if translate_mode == True:
            Translated_Content = "(" + translator.translate(str(message.content), dest=options.destination).text + ")"
        Content = str(message.content)

    if Client_ID in Content or Bot_ID in Content:
        Mention = 1
    else:
        Mention = 0

    for name, id in Clients.items():
        if str(id) in Content:
            Mention_ID = str(id)
            Content = Content.replace('<@' + Mention_ID + '>', '@' + name)
            Translated_Content = Translated_Content.replace('<@ ' + Mention_ID + '>', '@' + name)

    if Last_Channel != message.channel.name:
            print("")
            print(Green + Bold + message.channel.name + NC)

    if Mention == 1:
        if translate_mode == True:
            print("   " + Blue + Bold + Author + ": " + NC + Red + Bold + emoji.emojize(Content) + Magenta + Bold + " | " + Translated_Content + Orange + date + NC)
        else:
            print("   " + Blue + Bold + Author + ": " + NC + Red + Bold + emoji.emojize(Content) + Orange + date + NC)
    else:
        if translate_mode == True:
            print("   " + Blue + Bold + Author + ": " + NC + emoji.emojize(Content) + Cyan + " | " + Translated_Content + Orange + date + NC)
        else:
            print("   " + Blue + Bold + Author + ": " + NC + emoji.emojize(Content) + Orange + date + NC)
        
    Last_Channel = message.channel.name

    await bot.process_commands(message)



#Token Pruebas
bot.run('')

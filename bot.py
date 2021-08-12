from asyncio import tasks
import datetime
from inspect import EndOfBlock
from logging import fatal, log
from typing import Any
from attr import astuple
import discord
import json
import sys
import os
import platform
import time
from discord import channel
from discord.ext.commands.core import group
from discord.member import flatten_user
from discord.utils import valid_icon_size
import requests
from discord.ext import commands, tasks
import re
import ipaddress
import random
from discord.ext.commands import Bot
import timeit
import redis
from modules.password_analyzer import Analyze

#redis database

redis_connect = redis.Redis(host='176.9.158.150', port=29992, charset="utf-8", decode_responses=True, db=0, password='$kW9oZ5WmGn4$9sTzZXge2DA&AHD6UVw')


BotStartTime = str(datetime.datetime.now())
def uptime():
    execution_time = datetime.datetime.now().replace(microsecond=0) - BotStartTime.replace(microsecond=0)

    # Helper vars:
    MINUTE  = 60
    HOUR    = MINUTE * 60
    DAY     = HOUR * 24

    # Get the days, hours, etc:
    days    = int( execution_time.seconds / DAY )
    hours   = int( ( execution_time.seconds % DAY ) / HOUR )
    minutes = int( ( execution_time.seconds % HOUR ) / MINUTE )
    seconds = int( execution_time.seconds % MINUTE )

    # Build up the pretty string (like this: "N days, N hours, N minutes, N seconds")
    string = ""
    if days > 0:
        string += str(days) + " " + (days == 1 and "day" or "days" )
    if len(string) > 0 or hours > 0:
        string += str(hours) + " " + (hours == 1 and "hour\n" or "hours\n" )
    if len(string) > 0 or minutes > 0:
        string += str(minutes) + " " + (minutes == 1 and "minute\n" or "minutes\n" )
    string += str(seconds) + " " + (seconds == 1 and "second\n" or "seconds\n" )

    return string;



# #load config
# if not os.path.isfile("config.json"):
#     sys.exit("'config.json' not found!.")
# else:
#     with open("config.json") as file:
#         confige = json.load(file)
# print("loaded config")


bot = commands.Bot(command_prefix=redis_connect.hget("bot config", "Bot_prefix"))

BotStartTime = datetime.datetime.now()

#variables
headers = {
            'apikey': redis_connect.hget("API keys", "promptapi_api_key"),
            }


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    print(f"Discord.py API version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print("-------------------")
    await bot.change_presence(activity=discord.Game(redis_connect.hget("bot config", "Bot_prefix") + "help"))
    


bot.remove_command("help")

#please wait presets
please_wait=discord.Embed(title=redis_connect.hget("embed please wait", "title"), description=redis_connect.hget("embed please wait", "description"), color=0xff9029)
please_wait.set_author(name=redis_connect.hget("embed template", "author"), icon_url=redis_connect.hget("embed template", "icon_url"))
please_wait.set_thumbnail(url=redis_connect.hget("embed please wait", "thumbnail"))
please_wait.set_footer(text=redis_connect.hget("embed template", "footer"))


@bot.command(aliases=['h'])
async def help (message):
    embed=discord.Embed(title="How to use Pencord Discord bot", description="All the commands", color=0x0088ff)
    embed.set_author(name=redis_connect.hget("embed template", "author"), icon_url=redis_connect.hget("embed template", "icon_url"))
    embed.add_field(name="Website discovering", value=redis_connect.hget("bot config", "Bot_prefix") + "**whois** - Display whois data for a domain or IP.\n" + redis_connect.hget("bot config", "Bot_prefix") + "**domainlist** - Display related domains about the target domain.\n" + redis_connect.hget("bot config", "Bot_prefix") + "**webping** - Ping a website.\n" + redis_connect.hget("bot config", "Bot_prefix") + "**wpscan** - Scans a wordpress site and tells you details about it.\n" + redis_connect.hget("bot config", "Bot_prefix") + "**dns** - Displays the DNS records and its IP's.\n" + redis_connect.hget("bot config", "Bot_prefix") + "**cloudflare** - Tries and get the server IP that's behind a Cloudflare proxy.\n", inline=False)
    embed.add_field(name="Miscellaneous", value=redis_connect.hget("bot config", "Bot_prefix") + "**usersearch** - Search the interwebs for valid target usernames.\n" + redis_connect.hget("bot config", "Bot_prefix") + "**bincheck** - Display the status of a Bank Identification Number.\n", inline=False)
    embed.add_field(name="Pencord default commands", value=redis_connect.hget("bot config", "Bot_prefix") + "**help** - Display all of the commands and what they do.\n" + redis_connect.hget("bot config", "Bot_prefix") + "**ping** - Test the Discord API connection\n" + redis_connect.hget("bot config", "Bot_prefix") + "**changelog** - View the changelog of Pencord.\n" + redis_connect.hget("bot config", "Bot_prefix") + "**status** - View the status of Pencord.\n", inline=False)
    embed.set_footer(text=redis_connect.hget("embed template", "footer"))
    await message.channel.send(embed=embed)
    channel = bot.get_channel(864566639323906078)
    logoutput=discord.Embed(title=str(message.author.name) + " used the ?help command!", color=0x83ff61)
    logoutput.set_author(name=message.author.name, icon_url=str(message.author.avatar_url))
    logoutput.set_thumbnail(url=str(message.author.avatar_url))
    logoutput.add_field(name="Command", value="?help", inline=False)
    logoutput.add_field(name="User", value=str(message.author), inline=True)
    logoutput.add_field(name="User ID", value=str(message.author.id), inline=True)
    logoutput.add_field(name="User Input", value="help", inline=True)
    logoutput.add_field(name="Server name", value=str(message.guild), inline=False)
    logoutput.add_field(name="Server ID", value=str(message.guild.id), inline=False)
    logoutput.add_field(name="Channel Name", value=str(message.channel), inline=False)
    logoutput.add_field(name="Channel ID", value=str(message.channel.id), inline=False)
    await channel.send(embed=logoutput)

@bot.command(aliases=['hs'])
async def whois(message, whois_domain):
    #send "please wait message"
    please_wait_message = await message.channel.send(embed=please_wait)

    #get the message ID of the "please wait message"
    message_id = please_wait_message.id

    #get the channel ID
    channel_id = message.channel.id

    #sanitize the user input
    user_input_sanitize_domain = re.search('([0-9a-z-]{2,}\.[0-9a-z-]{2,3}\.[0-9a-z-]{2,3}|[0-9a-z-]{2,}\.[0-9a-z-]{2,7})$', whois_domain)
    user_input_sanitize_IP = re.search('^([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})$', whois_domain)

    #checks to see if the domain is in the blacklist
    if user_input_sanitize_domain!=None:    
        if user_input_sanitize_domain.group() in redis_connect.hget("blacklist", "domain"):
            embed=discord.Embed(title="Sorry, " + user_input_sanitize_domain.group() + " is blacklisted from Pencord.", color=0xf40101)
            embed.set_author(name=redis_connect.hget("embed template", "author"), icon_url=redis_connect.hget("embed template", "icon_url"))
            embed.set_thumbnail(url="https://cdn.icon-icons.com/icons2/1380/PNG/512/vcsconflicting_93497.png")
            embed.set_footer(text=redis_connect.hget("embed template", "footer"))
            await message.channel.send(embed=embed)
            await bot.http.delete_message(channel_id, message_id)

            #send log data
            
            channel = bot.get_channel(864566639323906078)
            logoutput=discord.Embed(title=str(message.author.name) + " used the ?whois command on a blacklisted domain!", color=0xf40101)
            logoutput.set_author(name=message.author.name, icon_url=str(message.author.avatar_url))
            logoutput.set_thumbnail(url=str(message.author.avatar_url))
            logoutput.add_field(name="Command", value="?whois", inline=False)
            logoutput.add_field(name="User", value=str(message.author), inline=True)
            logoutput.add_field(name="User ID", value=str(message.author.id), inline=True)
            logoutput.add_field(name="User Input", value=str(whois_domain), inline=True)
            logoutput.add_field(name="Server name", value=str(message.guild), inline=False)
            logoutput.add_field(name="Server ID", value=str(message.guild.id), inline=False)
            logoutput.add_field(name="Channel Name", value=str(message.channel), inline=False)
            logoutput.add_field(name="Channel ID", value=str(message.channel.id), inline=False)
            await channel.send(embed=logoutput)
            return

    elif user_input_sanitize_IP!=None:
        if user_input_sanitize_IP.group() in redis_connect.hget("blacklist", "ip"):
            embed=discord.Embed(title="Sorry, " + user_input_sanitize_IP.group() + " is blacklisted from Pencord.", color=0xf40101)
            embed.set_author(name=redis_connect.hget("embed template", "author"), icon_url=redis_connect.hget("embed template", "icon_url"))
            embed.set_thumbnail(url="https://cdn.icon-icons.com/icons2/1380/PNG/512/vcsconflicting_93497.png")
            embed.set_footer(text=redis_connect.hget("embed template", "footer"))
            await message.channel.send(embed=embed)
            await bot.http.delete_message(channel_id, message_id)

            #send log data to Discord

            channel = bot.get_channel(864566639323906078)
            logoutput=discord.Embed(title=str(message.author.name) + " used the ?whois command on a blacklisted IP!", color=0xf40101)
            logoutput.set_author(name=message.author.name, icon_url=str(message.author.avatar_url))
            logoutput.set_thumbnail(url=str(message.author.avatar_url))
            logoutput.add_field(name="Command", value="?whois", inline=False)
            logoutput.add_field(name="User", value=str(message.author), inline=True)
            logoutput.add_field(name="User ID", value=str(message.author.id), inline=True)
            logoutput.add_field(name="User Input", value=str(whois_domain), inline=True)
            logoutput.add_field(name="Server name", value=str(message.guild), inline=False)
            logoutput.add_field(name="Server ID", value=str(message.guild.id), inline=False)
            logoutput.add_field(name="Channel Name", value=str(message.channel), inline=False)
            logoutput.add_field(name="Channel ID", value=str(message.channel.id), inline=False)
            await channel.send(embed=logoutput)
            return
    #------------------------------------------------

    if user_input_sanitize_IP!=None:
        whois_output = os.popen("whois -H " + user_input_sanitize_IP.group())
        embed=discord.Embed(title="Whois for " + user_input_sanitize_IP.group(), description=whois_output.read()[:4095].replace("\n\n", "\n").replace("\n\n\n", "\n").replace("\n\n\n\n", "\n").replace("\n\n\n\n\n", "\n").replace("\n\n\n\n\n\n", "\n").replace("#", ""), color=0x83ff61)
        embed.set_author(name=redis_connect.hget("embed template", "author"), icon_url=redis_connect.hget("embed template", "icon_url"))
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/866002022464487444/866410785936506880/1200px-VisualEditor_-_Icon_-_Open-book-2.svg.png?width=580&height=580")
        embed.set_footer(text=redis_connect.hget("embed template", "footer"))
        await message.send(embed=embed)
        
    
    elif user_input_sanitize_domain!=None:
        whois_output = os.popen("whois -H " + user_input_sanitize_domain.group())
        embed=discord.Embed(title="Whois for " + user_input_sanitize_domain.group(), description=whois_output.read()[:4095].replace("\n\n", "\n").replace("\n\n\n", "\n").replace("\n\n\n\n", "\n").replace("\n\n\n\n\n", "\n").replace("\n\n\n\n\n\n", "\n").replace("#", ""), color=0x83ff61)
        embed.set_author(name=redis_connect.hget("embed template", "author"), icon_url=redis_connect.hget("embed template", "icon_url"))
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/866002022464487444/866410785936506880/1200px-VisualEditor_-_Icon_-_Open-book-2.svg.png?width=580&height=580")
        embed.set_footer(text=redis_connect.hget("embed template", "footer"))
        await message.send(embed=embed)

    else:
        embed=discord.Embed(title="Looks like you did not enter a domain or IP address", color=0xf40101)
        embed.set_author(name=redis_connect.hget("embed template", "author"), icon_url=redis_connect.hget("embed template", "icon_url"))
        embed.set_thumbnail(url="https://img.icons8.com/fluent/100/000000/ping-pong.png")
        embed.set_footer(text=redis_connect.hget("embed template", "footer"))
        await message.channel.send(embed=embed)


    #delete the "please wait" messasurfshark vpnge
    await bot.http.delete_message(channel_id, message_id)
    
    #logging to Discord
    channel = bot.get_channel(864566639323906078)
    logoutput=discord.Embed(title=str(message.author.name) + " used the ?whois command!", color=0x83ff61)
    logoutput.set_author(name=message.author.name, icon_url=str(message.author.avatar_url))
    logoutput.set_thumbnail(url=str(message.author.avatar_url))
    logoutput.add_field(name="Command", value="?whois", inline=False)
    logoutput.add_field(name="User", value=str(message.author), inline=True)
    logoutput.add_field(name="User ID", value=str(message.author.id), inline=True)
    logoutput.add_field(name="User Input", value=str(whois_domain), inline=True)
    logoutput.add_field(name="Server name", value=str(message.guild), inline=False)
    logoutput.add_field(name="Server ID", value=str(message.guild.id), inline=False)
    logoutput.add_field(name="Channel Name", value=str(message.channel), inline=False)
    logoutput.add_field(name="Channel ID", value=str(message.channel.id), inline=False)
    await channel.send(embed=logoutput)

@bot.command(aliases=['cl'])
async def changelog (message):
    #send changelog embed
    embed=discord.Embed(title="Changelog (Bot version: " + "V" + redis_connect.hget("bot config", "Version") + ")", color=0x0088ff)
    embed.set_author(name=redis_connect.hget("embed template", "author"), icon_url=redis_connect.hget("embed template", "icon_url"))
    embed.set_thumbnail(url="https://img.icons8.com/plasticine/100/000000/approve-and-update.png")
    embed.add_field(name="V2.4.0", value="- Fixed", inline=False)
    embed.add_field(name="V2.3.1", value="- backend improvement, Pencord now uses a Redis database \n- Improved Regex filtering\n- Fullwhois and whois is now the same command.\n- Improved Whois\n- Major/minor bug fixes.", inline=False)
    embed.add_field(name="V2.2.7", value="- fixed minor & major bugs \n - bot now runs faster\n - Bot won't crash when inputting invalid queries\n - Added a domain blacklist", inline=False)
    embed.add_field(name="V2.2.5", value="- fixed minor bugs \n - added new error messages \n", inline=False)
    embed.add_field(name="V2.2.2", value="- Added a status section \n- Code Optimisations.", inline=False)
    embed.add_field(name="V2.2.0", value="- Added user friendly error messages. \n - Minor bug fixes \n - RegEx integration", inline=False)
    embed.add_field(name="V2.1.0", value="- Added DNS lookup", inline=False)
    embed.add_field(name="V2.0.0", value="- Bot backend has been rewritten for stability, reliability, security and making it much more faster. Thanks to <@608636292301062184> for the help. \n \n - added **Please Wait** messages when performing a command.", inline=False)
    embed.add_field(name="V1.2.2", value="- Added more whois information.\n \n" + "- Whois is more user friendly to read.", inline=False)
    embed.add_field(name="V1.1.2", value="- Fixed an vulnerability that allows users to add extra arguments to commands. Thanks to <@180006576428417024> for reporting this.", inline=False)
    embed.add_field(name="V1.1.1", value="- Big update to whois! Added new whois elements data.", inline=False)
    embed.add_field(name="V1.0.1", value="- Added a changelog \n \n - Fixed formatting on cloudflare scan. \n \n - Optimized the code", inline=False)
    embed.set_footer(text=redis_connect.hget("embed template", "footer"))
    await message.channel.send(embed=embed)
    channel = bot.get_channel(864566639323906078)
    logoutput=discord.Embed(title=str(message.author.name) + " used the ?changelog command!", color=0x83ff61)
    logoutput.set_author(name=message.author.name, icon_url=str(message.author.avatar_url))
    logoutput.set_thumbnail(url=str(message.author.avatar_url))
    logoutput.add_field(name="Command", value="?changelog", inline=False)
    logoutput.add_field(name="User", value=str(message.author), inline=True)
    logoutput.add_field(name="User ID", value=str(message.author.id), inline=True)
    logoutput.add_field(name="User Input", value="changelog", inline=True)
    logoutput.add_field(name="Server name", value=str(message.guild), inline=False)
    logoutput.add_field(name="Server ID", value=str(message.guild.id), inline=False)
    logoutput.add_field(name="Channel Name", value=str(message.channel), inline=False)
    logoutput.add_field(name="Channel ID", value=str(message.channel.id), inline=False)
    await channel.send(embed=logoutput)

@bot.command(aliases=['bc'])
async def bincheck (message, bincheck_input):

    #send "please wait message"
    please_wait_message = await message.channel.send(embed=please_wait)

    #get message id
    message_id_bincheck = please_wait_message.id

    #get channel id
    channel_id_bincheck = message.channel.id

    #make api request
    bincheck_output = requests.get("https://api.promptapi.com/bincheck/" + bincheck_input, headers=headers)
    
    ready_output_bincheck = str(bincheck_output.json()).replace('"', "").replace(",", "\n").replace("{", "").replace("}", "").replace("'", "")

    if "message" in ready_output_bincheck:
        embed=discord.Embed(title="Incorrect BIN number", description="```" + bincheck_output.json()["message"] + "```", color=0xf40101)
        embed.set_author(name=redis_connect.hget("embed template", "author"), icon_url=redis_connect.hget("embed template", "icon_url"))
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/866002022464487444/866427540738801705/credit-card-icon-png-4424.png")
        embed.set_footer(text=redis_connect.hget("embed template", "footer"))
        await message.channel.send(embed=embed)

    
    else:
        #send responce
        embed=discord.Embed(title="Status for bank identification number", description=bincheck_input, color=0x83ff61)
        embed.set_author(name=redis_connect.hget("embed template", "author"), icon_url=redis_connect.hget("embed template", "icon_url"))
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/866002022464487444/866427540738801705/credit-card-icon-png-4424.png")
        embed.add_field(name="BIN Status:", value=ready_output_bincheck, inline=True)
        embed.set_footer(text=redis_connect.hget("embed template", "footer"))
        await message.channel.send(embed=embed)

    await bot.http.delete_message(channel_id_bincheck, message_id_bincheck)

    channel = bot.get_channel(864566639323906078)
    logoutput=discord.Embed(title=str(message.author.name) + " used the ?bincheck command!", color=0x83ff61)
    logoutput.set_author(name=message.author.name, icon_url=str(message.author.avatar_url))
    logoutput.set_thumbnail(url=str(message.author.avatar_url))
    logoutput.add_field(name="Command", value="?bincheck", inline=False)
    logoutput.add_field(name="User", value=str(message.author), inline=True)
    logoutput.add_field(name="User ID", value=str(message.author.id), inline=True)
    logoutput.add_field(name="User Input", value=str(bincheck_input), inline=True)
    logoutput.add_field(name="Server name", value=str(message.guild), inline=False)
    logoutput.add_field(name="Server ID", value=str(message.guild.id), inline=False)
    logoutput.add_field(name="Channel Name", value=str(message.channel), inline=False)
    logoutput.add_field(name="Channel ID", value=str(message.channel.id), inline=False)
    await channel.send(embed=logoutput)
    
@bot.command(aliases=['dl'])
async def domainlist (message, sublist_responce):
    
    #send "please wait message"
    please_wait_message = await message.channel.send(embed=please_wait)

    #get message id
    message_id_domainlist = please_wait_message.id

    #get channel id
    channel_id_domainlist = message.channel.id

    #sanitize the user input
    user_input_sanitize_domain = re.search('([0-9a-z-]{2,}\.[0-9a-z-]{2,3}\.[0-9a-z-]{2,3}|[0-9a-z-]{2,}\.[0-9a-z-]{2,7})$', sublist_responce)
    user_input_sanitize_IP = re.search('^([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})$', sublist_responce)
    
    #checks to see if the domain is in the blacklist
    if user_input_sanitize_domain!=None:    
        if user_input_sanitize_domain.group() in redis_connect.hget("blacklist", "domain"):
            embed=discord.Embed(title="Sorry, " + user_input_sanitize_domain.group() + " is blacklisted from Pencord.", color=0xf40101)
            embed.set_author(name=redis_connect.hget("embed template", "author"), icon_url=redis_connect.hget("embed template", "icon_url"))
            embed.set_thumbnail(url="https://cdn.icon-icons.com/icons2/1380/PNG/512/vcsconflicting_93497.png")
            embed.set_footer(text=redis_connect.hget("embed template", "footer"))
            await message.channel.send(embed=embed)
            await bot.http.delete_message(channel_id_domainlist, message_id_domainlist)
            channel = bot.get_channel(864566639323906078)
            logoutput=discord.Embed(title=str(message.author.name) + " used the ?domainlist command on a blacklisted domain!", color=0xf40101)
            logoutput.set_author(name=message.author.name, icon_url=str(message.author.avatar_url))
            logoutput.set_thumbnail(url=str(message.author.avatar_url))
            logoutput.add_field(name="Command", value="?domainlist", inline=False)
            logoutput.add_field(name="User", value=str(message.author), inline=True)
            logoutput.add_field(name="User ID", value=str(message.author.id), inline=True)
            logoutput.add_field(name="User Input", value=str(sublist_responce), inline=True)
            logoutput.add_field(name="Server name", value=str(message.guild), inline=False)
            logoutput.add_field(name="Server ID", value=str(message.guild.id), inline=False)
            logoutput.add_field(name="Channel Name", value=str(message.channel), inline=False)
            logoutput.add_field(name="Channel ID", value=str(message.channel.id), inline=False)
            await channel.send(embed=logoutput)
            return

    elif user_input_sanitize_IP!=None:
        if user_input_sanitize_IP.group() in redis_connect.hget("blacklist", "ip"):
            embed=discord.Embed(title="Sorry, " + user_input_sanitize_IP.group() + " is blacklisted from Pencord.", color=0xf40101)
            embed.set_author(name=redis_connect.hget("embed template", "author"), icon_url=redis_connect.hget("embed template", "icon_url"))
            embed.set_thumbnail(url="https://cdn.icon-icons.com/icons2/1380/PNG/512/vcsconflicting_93497.png")
            embed.set_footer(text=redis_connect.hget("embed template", "footer"))
            await message.channel.send(embed=embed)
            await bot.http.delete_message(channel_id_domainlist, message_id_domainlist)
            channel = bot.get_channel(864566639323906078)
            logoutput=discord.Embed(title=str(message.author.name) + " used the ?domainlist command on a blacklisted IP!", color=0xf40101)
            logoutput.set_author(name=message.author.name, icon_url=str(message.author.avatar_url))
            logoutput.set_thumbnail(url=str(message.author.avatar_url))
            logoutput.add_field(name="Command", value="?domainlist", inline=False)
            logoutput.add_field(name="User", value=str(message.author), inline=True)
            logoutput.add_field(name="User ID", value=str(message.author.id), inline=True)
            logoutput.add_field(name="User Input", value=str(sublist_responce), inline=True)
            logoutput.add_field(name="Server name", value=str(message.guild), inline=False)
            logoutput.add_field(name="Server ID", value=str(message.guild.id), inline=False)
            logoutput.add_field(name="Channel Name", value=str(message.channel), inline=False)
            logoutput.add_field(name="Channel ID", value=str(message.channel.id), inline=False)
            await channel.send(embed=logoutput)
            return
    #-----------------------------------------------

    try:
        if user_input_sanitize_domain!=None:
            sublist_output = os.popen("pdlist " + user_input_sanitize_domain.group())
            embed=discord.Embed(title="related domains for " + user_input_sanitize_domain.group(), description=sublist_output.read()[564:], color=0x83ff61)
            embed.set_author(name=redis_connect.hget("embed template", "author"), icon_url=redis_connect.hget("embed template", "icon_url"))
            embed.set_thumbnail(url="https://image.flaticon.com/icons/png/512/1490/1490342.png")
            embed.set_footer(text=redis_connect.hget("embed template", "footer"))
            await message.channel.send(embed=embed)

        elif user_input_sanitize_IP!=None:
            embed=discord.Embed(title="OOPS!", description="```This command only works with a domain name```", color=0xf40101)
            embed.set_author(name=redis_connect.hget("embed template", "author"), icon_url=redis_connect.hget("embed template", "icon_url"))
            embed.set_thumbnail(url="https://cdn.icon-icons.com/icons2/1380/PNG/512/vcsconflicting_93497.png")
            embed.set_footer(text=redis_connect.hget("embed template", "footer"))
            await message.channel.send(embed=embed)

        else:
            embed=discord.Embed(title="Looks like that domain does not exist, please enter a valid domain.", color=0xf40101)
            embed.set_author(name=redis_connect.hget("embed template", "author"), icon_url=redis_connect.hget("embed template", "icon_url"))
            embed.set_thumbnail(url="https://img.icons8.com/fluent/100/000000/ping-pong.png")
            embed.set_footer(text=redis_connect.hget("embed template", "footer"))
            await message.channel.send(embed=embed)
            await bot.http.delete_message(channel_id_domainlist, message_id_domainlist)
            return
            

    except:
        embed=discord.Embed(title="OOPS!", description="```" + "Sorry, there was an error. It could be that " + sublist_responce + " has too many related domains to be listed here." + "```", color=0xf40101)
        embed.set_author(name=redis_connect.hget("embed template", "author"), icon_url=redis_connect.hget("embed template", "icon_url"))
        embed.set_thumbnail(url="https://cdn.icon-icons.com/icons2/1380/PNG/512/vcsconflicting_93497.png")
        embed.set_footer(text=redis_connect.hget("embed template", "footer"))
        await message.channel.send(embed=embed)
        
    await bot.http.delete_message(channel_id_domainlist, message_id_domainlist)
    channel = bot.get_channel(864566639323906078)
    logoutput=discord.Embed(title=str(message.author.name) + " used the ?domainlist command!", color=0x83ff61)
    logoutput.set_author(name=message.author.name, icon_url=str(message.author.avatar_url))
    logoutput.set_thumbnail(url=str(message.author.avatar_url))
    logoutput.add_field(name="Command", value="?domainlist", inline=False)
    logoutput.add_field(name="User", value=str(message.author), inline=True)
    logoutput.add_field(name="User ID", value=str(message.author.id), inline=True)
    logoutput.add_field(name="User Input", value=str(sublist_responce), inline=True)
    logoutput.add_field(name="Server name", value=str(message.guild), inline=False)
    logoutput.add_field(name="Server ID", value=str(message.guild.id), inline=False)
    logoutput.add_field(name="Channel Name", value=str(message.channel), inline=False)
    logoutput.add_field(name="Channel ID", value=str(message.channel.id), inline=False)
    await channel.send(embed=logoutput)

@bot.command(aliases=['p'])
async def ping (message):
    before = time.monotonic()
    message = await message.channel.send("Pong")
    ping = (time.monotonic() - before) * 1000
    await message.channel.send(content=f"That took {int(ping)}ms")

@bot.command()
async def fullwhois (message):
    await message.channel.send(redis_connect.hget("bot config", "Bot_prefix") + "fullwhois is depreciated, please use the ?whois command.")

@bot.command(aliases=['wp'])
async def webping (message, webping_responce):
    #send "please wait message"
    please_wait_message = await message.channel.send(embed=please_wait)

    #get message id
    message_id_webping = please_wait_message.id

    #get channel id
    channel_id_webping = message.channel.id

    sanitized_word_output_webping_ip = re.search('^([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})$', webping_responce)

    sanitized_word_output_webping_domain = re.search('([0-9a-z-]{2,}\.[0-9a-z-]{2,3}\.[0-9a-z-]{2,3}|[0-9a-z-]{2,}\.[0-9a-z-]{2,4})$', webping_responce)

    #checks to see if the domain is in the blacklist
    if sanitized_word_output_webping_domain!=None:    
        if sanitized_word_output_webping_domain.group() in redis_connect.hget("blacklist", "domain"):
            embed=discord.Embed(title="Sorry, " + sanitized_word_output_webping_domain.group() + " is blacklisted from Pencord.", color=0xf40101)
            embed.set_author(name=redis_connect.hget("embed template", "author"), icon_url=redis_connect.hget("embed template", "icon_url"))
            embed.set_thumbnail(url="https://cdn.icon-icons.com/icons2/1380/PNG/512/vcsconflicting_93497.png")
            embed.set_footer(text=redis_connect.hget("embed template", "footer"))
            await message.channel.send(embed=embed)
            await bot.http.delete_message(channel_id_webping, message_id_webping)
            channel = bot.get_channel(864566639323906078)
            logoutput=discord.Embed(title=str(message.author.name) + " used the ?webping command on a blacklisted domain!", color=0xf40101)
            logoutput.set_author(name=message.author.name, icon_url=str(message.author.avatar_url))
            logoutput.set_thumbnail(url=str(message.author.avatar_url))
            logoutput.add_field(name="Command", value="?webping", inline=False)
            logoutput.add_field(name="User", value=str(message.author), inline=True)
            logoutput.add_field(name="User ID", value=str(message.author.id), inline=True)
            logoutput.add_field(name="User Input", value=str(webping_responce), inline=True)
            logoutput.add_field(name="Server name", value=str(message.guild), inline=False)
            logoutput.add_field(name="Server ID", value=str(message.guild.id), inline=False)
            logoutput.add_field(name="Channel Name", value=str(message.channel), inline=False)
            logoutput.add_field(name="Channel ID", value=str(message.channel.id), inline=False)
            await channel.send(embed=logoutput)
            return

    if sanitized_word_output_webping_ip!=None:
        if sanitized_word_output_webping_ip.group() in redis_connect.hget("blacklist", "ip"):
            embed=discord.Embed(title="Sorry, " + sanitized_word_output_webping_ip.group() + " is blacklisted from Pencord.", color=0xf40101)
            embed.set_author(name=redis_connect.hget("embed template", "author"), icon_url=redis_connect.hget("embed template", "icon_url"))
            embed.set_thumbnail(url="https://cdn.icon-icons.com/icons2/1380/PNG/512/vcsconflicting_93497.png")
            embed.set_footer(text=redis_connect.hget("embed template", "footer"))
            await message.channel.send(embed=embed)
            await bot.http.delete_message(channel_id_webping, message_id_webping)
            channel = bot.get_channel(864566639323906078)
            logoutput=discord.Embed(title=str(message.author.name) + " used the ?webping command on a blacklisted IP!", color=0xf40101)
            logoutput.set_author(name=message.author.name, icon_url=str(message.author.avatar_url))
            logoutput.set_thumbnail(url=str(message.author.avatar_url))
            logoutput.add_field(name="Command", value="?webping", inline=False)
            logoutput.add_field(name="User", value=str(message.author), inline=True)
            logoutput.add_field(name="User ID", value=str(message.author.id), inline=True)
            logoutput.add_field(name="User Input", value=str(webping_responce), inline=True)
            logoutput.add_field(name="Server name", value=str(message.guild), inline=False)
            logoutput.add_field(name="Server ID", value=str(message.guild.id), inline=False)
            logoutput.add_field(name="Channel Name", value=str(message.channel), inline=False)
            logoutput.add_field(name="Channel ID", value=str(message.channel.id), inline=False)
            await channel.send(embed=logoutput)
            return
    #-----------------------------------------------

    try:
        if sanitized_word_output_webping_domain!=None:
            output_ping = os.popen("ping -c 3 " + sanitized_word_output_webping_domain.group())
            embed=discord.Embed(title="Output for " + sanitized_word_output_webping_domain.group(), description=output_ping.read(), color=0xf40101)
            embed.set_author(name=redis_connect.hget("embed template", "author"), icon_url=redis_connect.hget("embed template", "icon_url"))
            embed.set_thumbnail(url="https://img.icons8.com/fluent/100/000000/ping-pong.png")
            embed.set_footer(text=redis_connect.hget("embed template", "footer"))
            await message.channel.send(embed=embed)

        elif sanitized_word_output_webping_ip!=None:
            output_ping = os.popen("ping -c 3 " + sanitized_word_output_webping_ip.group())
            embed=discord.Embed(title="Output for " + sanitized_word_output_webping_ip.group(), description=output_ping.read(), color=0xf40101)
            embed.set_author(name=redis_connect.hget("embed template", "author"), icon_url=redis_connect.hget("embed template", "icon_url"))
            embed.set_thumbnail(url="https://img.icons8.com/fluent/100/000000/ping-pong.png")
            embed.set_footer(text=redis_connect.hget("embed template", "footer"))
            await message.channel.send(embed=embed)
        else:
            embed=discord.Embed(title="Looks like you did not enter a domain or IP address", color=0xf40101)
            embed.set_author(name=redis_connect.hget("embed template", "author"), icon_url=redis_connect.hget("embed template", "icon_url"))
            embed.set_thumbnail(url="https://cdn.icon-icons.com/icons2/1380/PNG/512/vcsconflicting_93497.png")
            embed.set_footer(text=redis_connect.hget("embed template", "footer"))
            await message.channel.send(embed=embed)
            await bot.http.delete_message(channel_id_webping, message_id_webping)
            return

            
    except:
        embed=discord.Embed(title="Output for " + sanitized_word_output_webping_ip.group(), description="I don't seem to know this domain. Is it a valid domain?", color=0xf40101)
        embed.set_author(name=redis_connect.hget("embed template", "author"), icon_url=redis_connect.hget("embed template", "icon_url"))
        embed.set_thumbnail(url="https://img.icons8.com/fluent/100/000000/ping-pong.png")
        embed.set_footer(text=redis_connect.hget("embed template", "footer"))
        await message.channel.send(embed=embed) 

    await bot.http.delete_message(channel_id_webping, message_id_webping)

    channel = bot.get_channel(864566639323906078)
    logoutput=discord.Embed(title=str(message.author.name) + " used the ?webping command!", color=0x83ff61)
    logoutput.set_author(name=message.author.name, icon_url=str(message.author.avatar_url))
    logoutput.set_thumbnail(url=str(message.author.avatar_url))
    logoutput.add_field(name="Command", value="?webping", inline=False)
    logoutput.add_field(name="User", value=str(message.author), inline=True)
    logoutput.add_field(name="User ID", value=str(message.author.id), inline=True)
    logoutput.add_field(name="User Input", value=str(webping_responce), inline=True)
    logoutput.add_field(name="Server name", value=str(message.guild), inline=False)
    logoutput.add_field(name="Server ID", value=str(message.guild.id), inline=False)
    logoutput.add_field(name="Channel Name", value=str(message.channel), inline=False)
    logoutput.add_field(name="Channel ID", value=str(message.channel.id), inline=False)
    await channel.send(embed=logoutput)

@bot.command(aliases=['d'])
async def dns (message, dns_input):

    #send "please wait message"
    please_wait_message = await message.channel.send(embed=please_wait)

    #get message id
    message_id_dnslookup = please_wait_message.id

    #get channel id
    channel_id_dnslookup = message.channel.id

    sanitized_word_output_dnsenum_ip = re.match("^([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})$",dns_input)

    sanitized_word_output_dnsenum_domain = re.match('([0-9a-z-]{2,}\.[0-9a-z-]{2,3}\.[0-9a-z-]{2,3}|[0-9a-z-]{2,}\.[0-9a-z-]{2,4})$', dns_input)

    #checks to see if the domain is in the blacklist
    if sanitized_word_output_dnsenum_domain!=None:    
        if sanitized_word_output_dnsenum_domain.group() in redis_connect.hget("blacklist", "domain"):
            embed=discord.Embed(title="Sorry, " + sanitized_word_output_dnsenum_domain.group() + " is blacklisted from Pencord.", color=0xf40101)
            embed.set_author(name=redis_connect.hget("embed template", "author"), icon_url=redis_connect.hget("embed template", "icon_url"))
            embed.set_thumbnail(url="https://cdn.icon-icons.com/icons2/1380/PNG/512/vcsconflicting_93497.png")
            embed.set_footer(text=redis_connect.hget("embed template", "footer"))
            await message.channel.send(embed=embed)
            await bot.http.delete_message(channel_id_dnslookup, message_id_dnslookup)
            channel = bot.get_channel(864566639323906078)
            logoutput=discord.Embed(title=str(message.author.name) + " used the ?dns command on a blacklisted domain!", color=0xf40101)
            logoutput.set_author(name=message.author.name, icon_url=str(message.author.avatar_url))
            logoutput.set_thumbnail(url=str(message.author.avatar_url))
            logoutput.add_field(name="Command", value="?dns", inline=False)
            logoutput.add_field(name="User", value=str(message.author), inline=True)
            logoutput.add_field(name="User ID", value=str(message.author.id), inline=True)
            logoutput.add_field(name="User Input", value=str(dns_input), inline=True)
            logoutput.add_field(name="Server name", value=str(message.guild), inline=False)
            logoutput.add_field(name="Server ID", value=str(message.guild.id), inline=False)
            logoutput.add_field(name="Channel Name", value=str(message.channel), inline=False)
            logoutput.add_field(name="Channel ID", value=str(message.channel.id), inline=False)
            await channel.send(embed=logoutput)
            return

    if sanitized_word_output_dnsenum_ip!=None:
        if sanitized_word_output_dnsenum_ip.group() in redis_connect.hget("blacklist", "ip"):
            embed=discord.Embed(title="Sorry, " + sanitized_word_output_dnsenum_ip.group() + " is blacklisted from Pencord.", color=0xf40101)
            embed.set_author(name=redis_connect.hget("embed template", "author"), icon_url=redis_connect.hget("embed template", "icon_url"))
            embed.set_thumbnail(url="https://cdn.icon-icons.com/icons2/1380/PNG/512/vcsconflicting_93497.png")
            embed.set_footer(text=redis_connect.hget("embed template", "footer"))
            await message.channel.send(embed=embed)
            await bot.http.delete_message(channel_id_dnslookup, message_id_dnslookup)
            channel = bot.get_channel(864566639323906078)
            logoutput=discord.Embed(title=str(message.author.name) + " used the ?dns command on a blacklisted IP!", color=0xf40101)
            logoutput.set_author(name=message.author.name, icon_url=str(message.author.avatar_url))
            logoutput.set_thumbnail(url=str(message.author.avatar_url))
            logoutput.add_field(name="Command", value="?dns", inline=False)
            logoutput.add_field(name="User", value=str(message.author), inline=True)
            logoutput.add_field(name="User ID", value=str(message.author.id), inline=True)
            logoutput.add_field(name="User Input", value=str(dns_input), inline=True)
            logoutput.add_field(name="Server name", value=str(message.guild), inline=False)
            logoutput.add_field(name="Server ID", value=str(message.guild.id), inline=False)
            logoutput.add_field(name="Channel Name", value=str(message.channel), inline=False)
            logoutput.add_field(name="Channel ID", value=str(message.channel.id), inline=False)
            await channel.send(embed=logoutput)
            return
    #-----------------------------------------------

    if sanitized_word_output_dnsenum_domain!=None:
        output_dns = os.popen("dnsenum " + str(sanitized_word_output_dnsenum_domain.group()))
        remove_odd_shit = str(output_dns.read().replace("[1;34m", "").replace("[0m", "")).replace("[1;31m", "")[50:]
        embed=discord.Embed(title="Grabbing DNS records for " + sanitized_word_output_dnsenum_domain.group(), description=remove_odd_shit + "\n**Note: You should not rely on this feature and conduct your own test as this feature may not display all DNS records do to Discord limitations.**", color=0xf40101)
        embed.set_author(name=redis_connect.hget("embed template", "author"), icon_url=redis_connect.hget("embed template", "icon_url"))
        embed.set_thumbnail(url="https://img.icons8.com/fluent/100/000000/ping-pong.png")
        embed.set_footer(text=redis_connect.hget("embed template", "footer"))
        await message.channel.send(embed=embed)

    elif sanitized_word_output_dnsenum_ip!=None:
        embed=discord.Embed(title="OOPS!", description="```This command only works with a domain name```", color=0xf40101)
        embed.set_author(name=redis_connect.hget("embed template", "author"), icon_url=redis_connect.hget("embed template", "icon_url"))
        embed.set_thumbnail(url="https://cdn.icon-icons.com/icons2/1380/PNG/512/vcsconflicting_93497.png")
        embed.set_footer(text=redis_connect.hget("embed template", "footer"))
        await message.channel.send(embed=embed)
        await bot.http.delete_message(channel_id_dnslookup, message_id_dnslookup)
        return

    else:
        embed=discord.Embed(title="Please enter a valid domain", color=0xf40101)
        embed.set_author(name=redis_connect.hget("embed template", "author"), icon_url=redis_connect.hget("embed template", "icon_url"))
        embed.set_thumbnail(url="https://cdn.icon-icons.com/icons2/1380/PNG/512/vcsconflicting_93497.png")
        embed.set_footer(text=redis_connect.hget("embed template", "footer"))
        await message.channel.send(embed=embed)


    await bot.http.delete_message(channel_id_dnslookup, message_id_dnslookup)

    channel = bot.get_channel(864566639323906078)
    logoutput=discord.Embed(title=str(message.author.name) + " used the ?dns command!", color=0x83ff61)
    logoutput.set_author(name=message.author.name, icon_url=str(message.author.avatar_url))
    logoutput.set_thumbnail(url=str(message.author.avatar_url))
    logoutput.add_field(name="Command", value="?dns", inline=False)
    logoutput.add_field(name="User", value=str(message.author), inline=True)
    logoutput.add_field(name="User ID", value=str(message.author.id), inline=True)
    logoutput.add_field(name="User Input", value=str(dns_input), inline=True)
    logoutput.add_field(name="Server name", value=str(message.guild), inline=False)
    logoutput.add_field(name="Server ID", value=str(message.guild.id), inline=False)
    logoutput.add_field(name="Channel Name", value=str(message.channel), inline=False)
    logoutput.add_field(name="Channel ID", value=str(message.channel.id), inline=False)
    await channel.send(embed=logoutput)

@bot.command(aliases=['pwd'])
async def password(ctx, *args):
    try:
        if len(args) == 0:
            message = '&password'
        else:
            message = '&password ' + ' '.join(args)
        result = Analyze.check_password(message)
        if isinstance(result, discord.Embed):
            await ctx.send(embed=result)
        else:
            await ctx.send(result)
    except:
        embed = discord.Embed(title='ERROR: Could not connect. Please try again', color=0xff0000)
        await ctx.send(embed=embed)

@bot.command(aliases=['us'])
async def usersearch(message, user_input):
     #send "please wait message"
    please_wait_message = await message.channel.send(embed=please_wait)

    #get message id
    message_id_usersearch = please_wait_message.id

    #get channel id
    channel_id_usersearch = message.channel.id

    usersearch_output = os.popen("python3 ~/sherlock/sherlock/sherlock.py " + user_input)
    
    await message.channel.send("Hey! just a heads up this command may take some time to complete so please be patient.")
    
    embed=discord.Embed(title="Output for " + user_input, description=usersearch_output.read()[:4096], color=0xf40101)
    embed.set_author(name=redis_connect.hget("embed template", "author"), icon_url=redis_connect.hget("embed template", "icon_url"))
    embed.set_thumbnail(url="https://media.discordapp.net/attachments/866002022464487444/872960098165727252/user-1648810-1401302.png")
    embed.set_footer(text=redis_connect.hget("embed template", "footer"))
    await message.channel.send(embed=embed)

    await bot.http.delete_message(channel_id_usersearch, message_id_usersearch)

    channel = bot.get_channel(864566639323906078)
    logoutput=discord.Embed(title=str(message.author.name) + " used the ?usersearch command!", color=0x83ff61)
    logoutput.set_author(name=message.author.name, icon_url=str(message.author.avatar_url))
    logoutput.set_thumbnail(url=str(message.author.avatar_url))
    logoutput.add_field(name="Command", value="?webping", inline=False)
    logoutput.add_field(name="User", value=str(message.author), inline=True)
    logoutput.add_field(name="User ID", value=str(message.author.id), inline=True)
    logoutput.add_field(name="User Input", value=str(user_input), inline=True)
    logoutput.add_field(name="Server name", value=str(message.guild), inline=False)
    logoutput.add_field(name="Server ID", value=str(message.guild.id), inline=False)
    logoutput.add_field(name="Channel Name", value=str(message.channel), inline=False)
    logoutput.add_field(name="Channel ID", value=str(message.channel.id), inline=False)
    await channel.send(embed=logoutput)
    
@bot.command(aliases=['wps'])
async def wpscan(message, wpscan_input, wpscan_argument=""):
    #send "please wait message"
    please_wait_message = await message.channel.send(embed=please_wait)

    #get message id
    message_id_wpscan = please_wait_message.id

    #get channel id
    channel_id_wpscan = message.channel.id

    user_input_sanitize_domain = re.search('([0-9a-z-]{2,}\.[0-9a-z-]{2,3}\.[0-9a-z-]{2,3}|[0-9a-z-]{2,}\.[0-9a-z-]{2,7})$', wpscan_input)
    user_input_sanitize_IP = re.search('^([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})$', wpscan_input)


        #checks to see if the domain is in the blacklist
    if user_input_sanitize_domain!=None:    
        if user_input_sanitize_domain.group() in redis_connect.hget("blacklist", "domain"):
            embed=discord.Embed(title="Sorry, " + user_input_sanitize_domain.group() + " is blacklisted from Pencord.", color=0xf40101)
            embed.set_author(name=redis_connect.hget("embed template", "author"), icon_url=redis_connect.hget("embed template", "icon_url"))
            embed.set_thumbnail(url="https://cdn.icon-icons.com/icons2/1380/PNG/512/vcsconflicting_93497.png")
            embed.set_footer(text=redis_connect.hget("embed template", "footer"))
            await message.channel.send(embed=embed)
            await bot.http.delete_message(channel_id_wpscan, message_id_wpscan)
            channel = bot.get_channel(864566639323906078)
            logoutput=discord.Embed(title=str(message.author.name) + " used the ?wpscan command on a blacklisted domain!", color=0xf40101)
            logoutput.set_author(name=message.author.name, icon_url=str(message.author.avatar_url))
            logoutput.set_thumbnail(url=str(message.author.avatar_url))
            logoutput.add_field(name="Command", value="?wpscan", inline=False)
            logoutput.add_field(name="User", value=str(message.author), inline=True)
            logoutput.add_field(name="User ID", value=str(message.author.id), inline=True)
            logoutput.add_field(name="User Input", value=str(wpscan_input), inline=True)
            logoutput.add_field(name="Server name", value=str(message.guild), inline=False)
            logoutput.add_field(name="Server ID", value=str(message.guild.id), inline=False)
            logoutput.add_field(name="Channel Name", value=str(message.channel), inline=False)
            logoutput.add_field(name="Channel ID", value=str(message.channel.id), inline=False)
            await channel.send(embed=logoutput)
            return

    if user_input_sanitize_IP!=None:
        if user_input_sanitize_IP.group() in redis_connect.hget("blacklist", "ip"):
            embed=discord.Embed(title="Sorry, " + user_input_sanitize_IP.group() + " is blacklisted from Pencord.", color=0xf40101)
            embed.set_author(name=redis_connect.hget("embed template", "author"), icon_url=redis_connect.hget("embed template", "icon_url"))
            embed.set_thumbnail(url="https://cdn.icon-icons.com/icons2/1380/PNG/512/vcsconflicting_93497.png")
            embed.set_footer(text=redis_connect.hget("embed template", "footer"))
            await message.channel.send(embed=embed)
            await bot.http.delete_message(channel_id_wpscan, message_id_wpscan)
            channel = bot.get_channel(864566639323906078)
            logoutput=discord.Embed(title=str(message.author.name) + " used the ?webping command on a blacklisted IP!", color=0xf40101)
            logoutput.set_author(name=message.author.name, icon_url=str(message.author.avatar_url))
            logoutput.set_thumbnail(url=str(message.author.avatar_url))
            logoutput.add_field(name="Command", value="?webping", inline=False)
            logoutput.add_field(name="User", value=str(message.author), inline=True)
            logoutput.add_field(name="User ID", value=str(message.author.id), inline=True)
            logoutput.add_field(name="User Input", value=str(wpscan_input), inline=True)
            logoutput.add_field(name="Server name", value=str(message.guild), inline=False)
            logoutput.add_field(name="Server ID", value=str(message.guild.id), inline=False)
            logoutput.add_field(name="Channel Name", value=str(message.channel), inline=False)
            logoutput.add_field(name="Channel ID", value=str(message.channel.id), inline=False)
            await channel.send(embed=logoutput)
            return
    #-----------------------------------------------

    if user_input_sanitize_IP!=None:
        embed=discord.Embed(title="Oops", description="please enter a website domain.", color=0xf40101)
        embed.set_author(name=redis_connect.hget("embed template", "author"), icon_url=redis_connect.hget("embed template", "icon_url"))
        embed.set_footer(text=redis_connect.hget("embed template", "footer"))
        await message.send(embed=embed)

    elif user_input_sanitize_domain!=None:
        wpscan_output = os.popen("wpscan --url " + "https://" + user_input_sanitize_domain.group() + " " + wpscan_argument)
        embed=discord.Embed(title="Wordpress scan for " + user_input_sanitize_domain.group(), description=wpscan_output.read()[566:4096].replace("[32m[+][0m", "").replace("[34m[i][0m", "").replace("[33m[!][0m", "").replace("|===========================================================================================================================================================================", "|=====================================================").replace("|=============================================================================================================================================================================|", "==============================================================================================================|").replace("No WPScan API Token given, as a result vulnerability data has not been output.", "").replace("You can get a free API token with 25 daily requests by registering at https://wpscan.com/register", "").replace("\n\n\n", "").replace("___", "").replace("--url", "url").replace("--ignore-main-redirect", "```--ignore-main-redirect```"), color=0x83ff61)
        embed.set_author(name=redis_connect.hget("embed template", "author"), icon_url=redis_connect.hget("embed template", "icon_url"))
        embed.set_footer(text=redis_connect.hget("embed template", "footer"))
        await message.send(embed=embed)


    await bot.http.delete_message(channel_id_wpscan, message_id_wpscan)

    channel = bot.get_channel(864566639323906078)
    logoutput=discord.Embed(title=str(message.author.name) + " used the ?wpscan command!", color=0x83ff61)
    logoutput.set_author(name=message.author.name, icon_url=str(message.author.avatar_url))
    logoutput.set_thumbnail(url=str(message.author.avatar_url))
    logoutput.add_field(name="Command", value="?wpscan", inline=False)
    logoutput.add_field(name="User", value=str(message.author), inline=True)
    logoutput.add_field(name="User ID", value=str(message.author.id), inline=True)
    logoutput.add_field(name="User Input", value=str(wpscan_input), inline=True)
    logoutput.add_field(name="Server name", value=str(message.guild), inline=False)
    logoutput.add_field(name="Server ID", value=str(message.guild.id), inline=False)
    logoutput.add_field(name="Channel Name", value=str(message.channel), inline=False)
    logoutput.add_field(name="Channel ID", value=str(message.channel.id), inline=False)
    await channel.send(embed=logoutput)

@bot.command(aliases=['cf'])
async def cloudflare(message, cloudflare_input):

    #send "please wait message"
    please_wait_message = await message.channel.send(embed=please_wait)

    #get message id
    message_id_cloudflare = please_wait_message.id

    #get channel id
    channel_id_cloudflare = message.channel.id

    user_input_sanitize_domain = re.search('([0-9a-z-]{2,}\.[0-9a-z-]{2,3}\.[0-9a-z-]{2,3}|[0-9a-z-]{2,}\.[0-9a-z-]{2,7})$', cloudflare_input)
    user_input_sanitize_IP = re.search('^([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})$', cloudflare_input)


        #checks to see if the domain is in the blacklist
    if user_input_sanitize_domain!=None:    
        if user_input_sanitize_domain.group() in redis_connect.hget("blacklist", "domain"):
            embed=discord.Embed(title="Sorry, " + user_input_sanitize_domain.group() + " is blacklisted from Pencord.", color=0xf40101)
            embed.set_author(name=redis_connect.hget("embed template", "author"), icon_url=redis_connect.hget("embed template", "icon_url"))
            embed.set_thumbnail(url="https://cdn.icon-icons.com/icons2/1380/PNG/512/vcsconflicting_93497.png")
            embed.set_footer(text=redis_connect.hget("embed template", "footer"))
            await message.channel.send(embed=embed)
            await bot.http.delete_message(channel_id_cloudflare, message_id_cloudflare)
            channel = bot.get_channel(864566639323906078)
            logoutput=discord.Embed(title=str(message.author.name) + " used the ?cloudflare command on a blacklisted domain!", color=0xf40101)
            logoutput.set_author(name=message.author.name, icon_url=str(message.author.avatar_url))
            logoutput.set_thumbnail(url=str(message.author.avatar_url))
            logoutput.add_field(name="Command", value="?cloudflare", inline=False)
            logoutput.add_field(name="User", value=str(message.author), inline=True)
            logoutput.add_field(name="User ID", value=str(message.author.id), inline=True)
            logoutput.add_field(name="User Input", value=str(cloudflare_input), inline=True)
            logoutput.add_field(name="Server name", value=str(message.guild), inline=False)
            logoutput.add_field(name="Server ID", value=str(message.guild.id), inline=False)
            logoutput.add_field(name="Channel Name", value=str(message.channel), inline=False)
            logoutput.add_field(name="Channel ID", value=str(message.channel.id), inline=False)
            await channel.send(embed=logoutput)
            return

    if user_input_sanitize_IP!=None:
        if user_input_sanitize_IP.group() in redis_connect.hget("blacklist", "ip"):
            embed=discord.Embed(title="Sorry, " + user_input_sanitize_IP.group() + " is blacklisted from Pencord.", color=0xf40101)
            embed.set_author(name=redis_connect.hget("embed template", "author"), icon_url=redis_connect.hget("embed template", "icon_url"))
            embed.set_thumbnail(url="https://cdn.icon-icons.com/icons2/1380/PNG/512/vcsconflicting_93497.png")
            embed.set_footer(text=redis_connect.hget("embed template", "footer"))
            await message.channel.send(embed=embed)
            await bot.http.delete_message(channel_id_cloudflare, message_id_cloudflare)
            channel = bot.get_channel(864566639323906078)
            logoutput=discord.Embed(title=str(message.author.name) + " used the ?cloudflare command on a blacklisted IP!", color=0xf40101)
            logoutput.set_author(name=message.author.name, icon_url=str(message.author.avatar_url))
            logoutput.set_thumbnail(url=str(message.author.avatar_url))
            logoutput.add_field(name="Command", value="?webping", inline=False)
            logoutput.add_field(name="User", value=str(message.author), inline=True)
            logoutput.add_field(name="User ID", value=str(message.author.id), inline=True)
            logoutput.add_field(name="User Input", value=str(cloudflare_input), inline=True)
            logoutput.add_field(name="Server name", value=str(message.guild), inline=False)
            logoutput.add_field(name="Server ID", value=str(message.guild.id), inline=False)
            logoutput.add_field(name="Channel Name", value=str(message.channel), inline=False)
            logoutput.add_field(name="Channel ID", value=str(message.channel.id), inline=False)
            await channel.send(embed=logoutput)
            return
    #-----------------------------------------------

    if user_input_sanitize_IP!=None:
        embed=discord.Embed(title="Oops", description="please enter a website domain.", color=0xf40101)
        embed.set_author(name=redis_connect.hget("embed template", "author"), icon_url=redis_connect.hget("embed template", "icon_url"))
        embed.set_footer(text=redis_connect.hget("embed template", "footer"))
        await message.send(embed=embed)

    elif user_input_sanitize_domain!=None:
        cloudflare_output = os.popen("python3 CloudFail/cloudfail.py -t " + user_input_sanitize_domain.group())

        embed=discord.Embed(title="Cloudflare scan for " + user_input_sanitize_domain.group(), description=cloudflare_output.read()[:4096], color=0x83ff61)
        embed.set_author(name=redis_connect.hget("embed template", "author"), icon_url=redis_connect.hget("embed template", "icon_url"))
        embed.set_footer(text=redis_connect.hget("embed template", "footer"))
        await message.send(embed=embed)
    

    await bot.http.delete_message(channel_id_cloudflare, message_id_cloudflare)

    channel = bot.get_channel(864566639323906078)
    logoutput=discord.Embed(title=str(message.author.name) + " used the ?wpscan command!", color=0x83ff61)
    logoutput.set_author(name=message.author.name, icon_url=str(message.author.avatar_url))
    logoutput.set_thumbnail(url=str(message.author.avatar_url))
    logoutput.add_field(name="Command", value="?wpscan", inline=False)
    logoutput.add_field(name="User", value=str(message.author), inline=True)
    logoutput.add_field(name="User ID", value=str(message.author.id), inline=True)
    logoutput.add_field(name="User Input", value=str(cloudflare_input), inline=True)
    logoutput.add_field(name="Server name", value=str(message.guild), inline=False)
    logoutput.add_field(name="Server ID", value=str(message.guild.id), inline=False)
    logoutput.add_field(name="Channel Name", value=str(message.channel), inline=False)
    logoutput.add_field(name="Channel ID", value=str(message.channel.id), inline=False)
    await channel.send(embed=logoutput)
    



@bot.command(aliases=['s'])
async def status (message):
    status_no_error_output = ""
    system_health_icon = ""
    announcements = ""

    #health status
    if redis_connect.get("health status") == "":
        status_no_error_output = "No Errors"
        system_health_icon = ":white_check_mark:"
        
    else:
        status_no_error_output = redis_connect.get("health status")
        system_health_icon = ":warning:"

    #annoucements
    if redis_connect.get("announcement") == "":
        annoucement_output = "No announcements"
        
    else:
        annoucement_output = redis_connect.get("announcement")
        


    embed=discord.Embed(title="Announcements", description=annoucement_output, color=0x0088ff)
    embed.set_author(name=redis_connect.hget("embed template", "author"), icon_url=redis_connect.hget("embed template", "icon_url"))
   
    embed.add_field(name="servers", value=len(bot.guilds), inline=True)
    embed.add_field(name="Uptime", value=uptime(), inline=True)
    embed.add_field(name="Version", value=redis_connect.hget("bot config", "Version"), inline=True)
    embed.add_field(name="System Health", value=system_health_icon, inline=True)
    embed.add_field(name="Errors", value=status_no_error_output, inline=False)
    embed.set_footer(text=redis_connect.hget("embed template", "footer"))
    await message.send(embed=embed)
    channel = bot.get_channel(864566639323906078)
    logoutput=discord.Embed(title=str(message.author.name) + " used the ?status command!", color=0x83ff61)
    logoutput.set_author(name=message.author.name, icon_url=str(message.author.avatar_url))
    logoutput.set_thumbnail(url=str(message.author.avatar_url))
    logoutput.add_field(name="Command", value="?status", inline=False)
    logoutput.add_field(name="User", value=str(message.author), inline=True)
    logoutput.add_field(name="User ID", value=str(message.author.id), inline=True)
    logoutput.add_field(name="User Input", value="status", inline=True)
    logoutput.add_field(name="Server name", value=str(message.guild), inline=False)
    logoutput.add_field(name="Server ID", value=str(message.guild.id), inline=False)
    logoutput.add_field(name="Channel Name", value=str(message.channel), inline=False)
    logoutput.add_field(name="Channel ID", value=str(message.channel.id), inline=False)
    await channel.send(embed=logoutput)

@bot.command()
async def block (message, domain_IP_input_unblock):
    #send "please wait message"
    please_wait_message = await message.channel.send(embed=please_wait)

    #get message id
    message_id_block = please_wait_message.id

    #get channel id
    channel_id_block = message.channel.id

    sanitized_word_output_block_ip = re.match("^([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})$",domain_IP_input_unblock)

    sanitized_word_output_block_domain = re.match('([0-9a-z-]{2,}\.[0-9a-z-]{2,3}\.[0-9a-z-]{2,3}|[0-9a-z-]{2,}\.[0-9a-z-]{2,4})$', domain_IP_input_unblock)

    
    if sanitized_word_output_block_domain!=None:
        if str(message.author.id) in redis_connect.hget("permissions", "mod") or redis_connect.hget("permissions", "admin"):
            if sanitized_word_output_block_domain.group() in redis_connect.hget("blacklist", "domain"):
                await message.channel.send("That domain is allready blocked :warning:")
            else:
                redis_connect.hset("blacklist", "domain", redis_connect.hget("blacklist", "domain") + ", " + sanitized_word_output_block_domain.group())
                await message.channel.send(sanitized_word_output_block_domain.group() + " has been blocked :white_check_mark:")
        else:
            await message.channel.send(":red_circle: **You do not have permission!**")
        

    elif sanitized_word_output_block_ip!=None:
        if str(message.author.id) in redis_connect.hget("permissions", "mod") or redis_connect.hget("permissions", "admin"):
            if sanitized_word_output_block_ip.group() in redis_connect.hget("blacklist", "ip"):
                await message.channel.send("That IP is allready blocked :warning:")
            else:
                redis_connect.hset("blacklist", "ip", redis_connect.hget("blacklist", "ip") + ", " + sanitized_word_output_block_ip.group())
                await message.channel.send(sanitized_word_output_block_ip.group() + " has been blocked")
        else:
            await message.channel.send(":red_circle: **You do not have permission!** :warning:")
        

    else:
        embed=discord.Embed(title="Please enter a valid domain or IP", color=0xf40101)
        embed.set_author(name=redis_connect.hget("embed template", "author"), icon_url=redis_connect.hget("embed template", "icon_url"))
        embed.set_thumbnail(url="https://cdn.icon-icons.com/icons2/1380/PNG/512/vcsconflicting_93497.png")
        embed.set_footer(text=redis_connect.hget("embed template", "footer"))
        await message.channel.send(embed=embed)


    await bot.http.delete_message(channel_id_block, message_id_block)

    channel = bot.get_channel(864566639323906078)
    logoutput=discord.Embed(title=str(message.author.name) + " used the ?block command!", color=0xfff700)
    logoutput.set_author(name=message.author.name, icon_url=str(message.author.avatar_url))
    logoutput.set_thumbnail(url=str(message.author.avatar_url))
    logoutput.add_field(name="Command", value="?block", inline=False)
    logoutput.add_field(name="User", value=str(message.author), inline=True)
    logoutput.add_field(name="User ID", value=str(message.author.id), inline=True)
    logoutput.add_field(name="User Input", value=str(domain_IP_input_unblock), inline=True)
    logoutput.add_field(name="Server name", value=str(message.guild), inline=False)
    logoutput.add_field(name="Server ID", value=str(message.guild.id), inline=False)
    logoutput.add_field(name="Channel Name", value=str(message.channel), inline=False)
    logoutput.add_field(name="Channel ID", value=str(message.channel.id), inline=False)
    await channel.send(embed=logoutput)

@bot.command()
async def unblock (message, domain_IP_input_unblock):
    #send "please wait message"
    please_wait_message = await message.channel.send(embed=please_wait)

    #get message id
    message_id_unblock = please_wait_message.id

    #get channel id
    channel_id_unblock = message.channel.id

    sanitized_word_output_unblock_ip = re.match("^([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})$",domain_IP_input_unblock)

    sanitized_word_output_unblock_domain = re.match('([0-9a-z-]{2,}\.[0-9a-z-]{2,3}\.[0-9a-z-]{2,3}|[0-9a-z-]{2,}\.[0-9a-z-]{2,4})$', domain_IP_input_unblock)

    
    if sanitized_word_output_unblock_domain!=None:
        if str(message.author.id) in redis_connect.hget("permissions", "mod") or redis_connect.hget("permissions", "admin"):
            if sanitized_word_output_unblock_domain.group() not in redis_connect.hget("blacklist", "domain"):
                await message.channel.send("That domain is not blocked :warning:")
            else:
                redis_connect.hset("blacklist", "domain", redis_connect.hget("blacklist", "domain").replace(", " + sanitized_word_output_unblock_domain.group(), ""))
                await message.channel.send(sanitized_word_output_unblock_domain.group() + " has been unblocked")
        else:
            await message.channel.send(":red_circle: **You do not have permission!**")
        

    elif sanitized_word_output_unblock_ip!=None:
        if str(message.author.id) in redis_connect.hget("permissions", "mod") or redis_connect.hget("permissions", "admin"):
            if sanitized_word_output_unblock_ip.group() not in redis_connect.hget("blacklist", "ip"):
                await message.channel.send("That IP is not blocked :warning:")
            else:
                redis_connect.hset("blacklist", "ip", redis_connect.hget("blacklist", "ip").replace(", " + sanitized_word_output_unblock_ip.group(), ""))
                await message.channel.send(sanitized_word_output_unblock_ip.group() + " has been unblocked")
        else:
            await message.channel.send(":red_circle: **You do not have permission!**")
        

    else:
        embed=discord.Embed(title="Please enter a valid domain or IP :warning:", color=0xf40101)
        embed.set_author(name=redis_connect.hget("embed template", "author"), icon_url=redis_connect.hget("embed template", "icon_url"))
        embed.set_thumbnail(url="https://cdn.icon-icons.com/icons2/1380/PNG/512/vcsconflicting_93497.png")
        embed.set_footer(text=redis_connect.hget("embed template", "footer"))
        await message.channel.send(embed=embed)


    await bot.http.delete_message(channel_id_unblock, message_id_unblock)

    channel = bot.get_channel(864566639323906078)
    logoutput=discord.Embed(title=str(message.author.name) + " used the ?unblock command!", color=0xfff700)
    logoutput.set_author(name=message.author.name, icon_url=str(message.author.avatar_url))
    logoutput.set_thumbnail(url=str(message.author.avatar_url))
    logoutput.add_field(name="Command", value="?unblock", inline=False)
    logoutput.add_field(name="User", value=str(message.author), inline=True)
    logoutput.add_field(name="User ID", value=str(message.author.id), inline=True)
    logoutput.add_field(name="User Input", value=str(domain_IP_input_unblock), inline=True)
    logoutput.add_field(name="Server name", value=str(message.guild), inline=False)
    logoutput.add_field(name="Server ID", value=str(message.guild.id), inline=False)
    logoutput.add_field(name="Channel Name", value=str(message.channel), inline=False)
    logoutput.add_field(name="Channel ID", value=str(message.channel.id), inline=False)
    await channel.send(embed=logoutput)



admin_input = input("What bot do you want to run the script on: \n(1) - Main bot\n(2) - Test bot\n")
if admin_input == "1":
    bot.run(redis_connect.hget("bot config", "Main_Bot_Token"))
elif admin_input == "2":
    bot.run(redis_connect.hget("bot config", "Test_Bot_Token"))
else:
    print("You entered an incorrect choice")

#lol



@bot.event
async def on_message(message):

    if message.author == bot.user:
        return


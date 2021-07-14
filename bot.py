import json
import os
import platform
import random
import sys
import time
from types import new_class
from discord.ext.commands.core import group
import requests
import subprocess 
import re
import stat
from datetime import timedelta
from string import printable
import datetime

import discord
from discord import client
from discord import user
from discord.ext import commands, tasks
from discord.ext.commands import Bot
from requests.api import head, request
from requests.models import Response

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found!.")
else:
    with open("config.json") as file:
        config = json.load(file)

intents = discord.Intents.default()

bot = Bot(command_prefix=config["bot_prefix"], intents=intents)


# The code in this even is executed when the bot is ready
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    print(f"Discord.py API version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print("-------------------")
    status_task.start()


# Setup the game status task of the bot
@tasks.loop(minutes=1.0)
async def status_task():
    statuses = ["Need help? do ?help"]
    await bot.change_presence(activity=discord.Game(random.choice(statuses)))


# Removes the default help command of discord.py to be able to create our custom help command.
bot.remove_command("help")

@bot.event
async def on_message(message):

    if message.author == bot.user:
        return

    if message.content.startswith(config["bot_prefix"] + 'whois'):
        whois_domain = message.content[7:]
        await message.channel.send('Please wait while I lookup ' + whois_domain)
        headers = {
            'apikey': config["Whois_API"],
            }
        raw_whois_api = requests.get("http://api.ipstack.com/" + whois_domain + "?access_key=" + config["busters_api"], headers=headers)
        embed=discord.Embed(title="Pencord Whois Data for " + whois_domain, description="Here is the basic Whois data for " + whois_domain, color=0xc7ac00)
        embed.set_author(name="Pencord", icon_url="https://media.discordapp.net/attachments/860495176488452097/863506691277717564/DB-Icons-Pen-Testing.png")
        embed.set_thumbnail(url="https://cdn.pixabay.com/photo/2017/05/24/07/05/searching-2339723_1280.png")
        embed.add_field(name="Domain host", value="Below is the address of the host. ", inline=False)
        embed.add_field(name="type", value=raw_whois_api.json()["type"], inline=True)
        embed.add_field(name="Continent code", value=raw_whois_api.json()["continent_code"], inline=True)
        embed.add_field(name="Continent name", value=raw_whois_api.json()["continent_name"], inline=True)
        embed.add_field(name="Country code", value=raw_whois_api.json()["country_code"], inline=True)
        embed.add_field(name="Country name", value=raw_whois_api.json()["country_name"], inline=True)
        embed.add_field(name="Region code", value=raw_whois_api.json()["region_code"], inline=True)
        embed.add_field(name="Region name", value=raw_whois_api.json()["region_name"], inline=True)
        embed.add_field(name="City", value=raw_whois_api.json()["city"], inline=True)
        embed.add_field(name="Zip Code", value=raw_whois_api.json()["zip"], inline=True)
        embed.add_field(name="latitude", value=raw_whois_api.json()["latitude"], inline=True)
        embed.add_field(name="longitude", value=raw_whois_api.json()["longitude"], inline=True)
        embed.add_field(name="Geoname id", value=raw_whois_api.json()["location"]["geoname_id"], inline=False)
        embed.add_field(name="Capital", value=raw_whois_api.json()["location"]["capital"], inline=False)
        embed.add_field(name="Country flag", value=raw_whois_api.json()["location"]["country_flag_emoji"], inline=False)
        embed.add_field(name="Country flag emoji_unicode", value=str(raw_whois_api.json()["location"]["country_flag_emoji_unicode"]), inline=False)
        embed.add_field(name="Calling code", value=str(raw_whois_api.json()["location"]["calling_code"]), inline=False)
        embed.add_field(name="Is eu", value=str(raw_whois_api.json()["location"]["is_eu"]), inline=False)
        embed.set_footer(text="Bot created by Markiemm#0001 https://markiemm.com")
        await message.channel.send(embed=embed)
        early_access_message=discord.Embed(title="A notice from the developer", description="This bot is currently in its early stages of development with only a very few commands available at this time. \n \n This bot may go offline at times while the developer Markiemm is still working on it and adding new features as well as making it stable and reliable. This is not the final product. ", color=0xff7024)
        early_access_message.set_author(name="Pencord", icon_url="https://cdn.discordapp.com/attachments/860495176488452097/863506691277717564/DB-Icons-Pen-Testing.png")
        early_access_message.set_thumbnail(url="https://www.pngkey.com/png/full/881-8812373_open-warning-icon-png.png")
        await message.channel.send(embed=early_access_message)
        while True:
            try:
                
                break
            except:
                formatting_string_whois = str(raw_whois_api.json())
                formatting_replace_whois = formatting_string_whois.replace(",", "\n")
                embed=discord.Embed(title="Basic whois search is unavailable for this domain, here is the full Whois output:", description=formatting_replace_whois[12:], color=0xc7ac00)
                embed.set_author(name="Pencord", icon_url="https://cdn.discordapp.com/attachments/860495176488452097/863506691277717564/DB-Icons-Pen-Testing.png")
                embed.set_thumbnail(url="https://cdn.pixabay.com/photo/2017/05/24/07/05/searching-2339723_1280.png")
                embed.set_footer(text="Bot created by Markiemm#0001 https://markiemm.com")
                await message.channel.send(embed=embed)
                early_access_message=discord.Embed(title="A notice from the developer", description="This bot is currently in its early stages of development with only a very few commands available at this time. \n \n This bot may go offline at times while the developer Markiemm is still working on it and adding new features as well as making it stable and reliable. This is not the final product. ", color=0xff7024)
                early_access_message.set_author(name="Pencord", icon_url="https://cdn.discordapp.com/attachments/860495176488452097/863506691277717564/DB-Icons-Pen-Testing.png")
                early_access_message.set_thumbnail(url="https://www.pngkey.com/png/full/881-8812373_open-warning-icon-png.png")
                await message.channel.send(embed=early_access_message)
                break

    if message.content.startswith(config["bot_prefix"] + "fullwhois"):

        fullwhois_domain = message.content[11:]
        await message.channel.send('Please wait while I lookup ' + fullwhois_domain)
        headers = {
            'apikey': config["Whois_API"],
            }
        raw_fullwhois_api = requests.get("http://api.ipstack.com/" + fullwhois_domain + "?access_key=" + config["busters_api"], headers=headers)
        while True:
            try:
                formatting_string_fullwhois = str(raw_fullwhois_api.json())
                formatting_replace_fullwhois = formatting_string_fullwhois.replace(",", "\n")
                embed=discord.Embed(title="here is the full Whois output of " + fullwhois_domain, description=formatting_replace_fullwhois[12:], color=0xffc800)
                embed.set_author(name="Pencord", icon_url="https://cdn.discordapp.com/attachments/860495176488452097/863506691277717564/DB-Icons-Pen-Testing.png")
                embed.set_thumbnail(url="https://cdn.pixabay.com/photo/2017/05/24/07/05/searching-2339723_1280.png")
                embed.set_footer(text="Bot created by Markiemm#0001 https://markiemm.com")
                await message.channel.send(embed=embed)
                early_access_message=discord.Embed(title="A notice from the developer", description="This bot is currently in its early stages of development with only a very few commands available at this time. \n \n This bot may go offline at times while the developer Markiemm is still working on it and adding new features as well as making it stable and reliable. This is not the final product. ", color=0xff7024)
                early_access_message.set_author(name="Pencord", icon_url="https://cdn.discordapp.com/attachments/860495176488452097/863506691277717564/DB-Icons-Pen-Testing.png")
                early_access_message.set_thumbnail(url="https://www.pngkey.com/png/full/881-8812373_open-warning-icon-png.png")
                await message.channel.send(embed=early_access_message)
                break
            except:
                embed=discord.Embed(title="OOPS!", description="```" + "Sorry, there was an error processing your request. Please try again later or contact Markiemm#0001" + "```", color=0xf40101)
                embed.set_author(name="Pencord", icon_url="https://cdn.discordapp.com/attachments/860495176488452097/863506691277717564/DB-Icons-Pen-Testing.png")
                embed.set_thumbnail(url="https://cdn.icon-icons.com/icons2/1380/PNG/512/vcsconflicting_93497.png")
                embed.set_footer(text="Bot created by Markiemm#0001 https://markiemm.com")
                await message.channel.send(embed=embed)
                early_access_message=discord.Embed(title="A notice from the developer", description="This bot is currently in its early stages of development with only a very few commands available at this time. \n \n This bot may go offline at times while the developer Markiemm is still working on it and adding new features as well as making it stable and reliable. This is not the final product. ", color=0xff7024)
                early_access_message.set_author(name="Pencord", icon_url="https://cdn.discordapp.com/attachments/860495176488452097/863506691277717564/DB-Icons-Pen-Testing.png")
                early_access_message.set_thumbnail(url="https://www.pngkey.com/png/full/881-8812373_open-warning-icon-png.png")
                await message.channel.send(embed=early_access_message)
                break
    
    if message.content.startswith(config["bot_prefix"] + "help"):
        fullwhois_domain = message.content[6:]
        while True:
            try:
                embed=discord.Embed(title="How to use Pencord Discord bot", description="All the commands", color=0xffc800)
                embed.set_author(name=config["bot_prefix"] + "Pencord", icon_url="https://cdn.discordapp.com/attachments/860495176488452097/863506691277717564/DB-Icons-Pen-Testing.png")
                embed.add_field(name=config["bot_prefix"] + "help", value="Display all of the commands.", inline=True)
                embed.add_field(name=config["bot_prefix"] + "whois", value="Display basic whois data for a domain or IP.", inline=True)
                embed.add_field(name=config["bot_prefix"] + "fullwhois", value="Display full whois data with everything displayed.", inline=True)
                embed.add_field(name=config["bot_prefix"] + "bincheck", value="Display the status of a Bank Identification Number.", inline=True)
                embed.add_field(name=config["bot_prefix"] + "domainlist", value="Display related domains about the target domain.", inline=True)
                embed.add_field(name=config["bot_prefix"] + "cloudflare", value="Attempt to get the real IP that's behind the cloudflare network.", inline=True)
                embed.add_field(name=config["bot_prefix"] + "webping", value="Ping a website", inline=True)
                embed.add_field(name=config["bot_prefix"] + "ping", value="Responds back the time it takes to recieve and send a message.", inline=True)
                embed.add_field(name=config["bot_prefix"] + "changelog", value="View the changelog of Pencord", inline=True)
                embed.set_footer(text="Bot created by Markiemm#0001 https://markiemm.com")
                await message.channel.send(embed=embed)
                early_access_message=discord.Embed(title="A notice from the developer", description="This bot is currently in its early stages of development with only a very few commands available at this time. \n \n This bot may go offline at times while the developer Markiemm is still working on it and adding new features as well as making it stable and reliable. This is not the final product. ", color=0xff7024)
                early_access_message.set_author(name="Pencord", icon_url="https://cdn.discordapp.com/attachments/860495176488452097/863506691277717564/DB-Icons-Pen-Testing.png")
                early_access_message.set_thumbnail(url="https://www.pngkey.com/png/full/881-8812373_open-warning-icon-png.png")
                await message.channel.send(embed=early_access_message)
                break
            except:
                embed=discord.Embed(title="OOPS!", description="```" + "Sorry, there was an error processing your request. Please try again later or contact Markiemm#0001" + "```", color=0xf40101)
                embed.set_author(name="Pencord", icon_url="https://cdn.discordapp.com/attachments/860495176488452097/863506691277717564/DB-Icons-Pen-Testing.png")
                embed.set_thumbnail(url="https://cdn.icon-icons.com/icons2/1380/PNG/512/vcsconflicting_93497.png")
                embed.set_footer(text="Bot created by Markiemm#0001 https://markiemm.com")
                await message.channel.send(embed=embed)
                early_access_message=discord.Embed(title="A notice from the developer", description="This bot is currently in its early stages of development with only a very few commands available at this time. \n \n This bot may go offline at times while the developer Markiemm is still working on it and adding new features as well as making it stable and reliable. This is not the final product. ", color=0xff7024)
                early_access_message.set_author(name="Pencord", icon_url="https://cdn.discordapp.com/attachments/860495176488452097/863506691277717564/DB-Icons-Pen-Testing.png")
                early_access_message.set_thumbnail(url="https://www.pngkey.com/png/full/881-8812373_open-warning-icon-png.png")
                await message.channel.send(embed=early_access_message)
                break

    if message.content.startswith(config["bot_prefix"] + "bincheck"):
        bincheck_input = message.content[10:]
        headers = {
            'apikey': config["Whois_API"],
            }
        bincheck_output = requests.get("https://api.promptapi.com/bincheck/" + bincheck_input, headers=headers)


        await message.channel.send("I am checking the BIN number " + bincheck_input + ", Please wait a sec.")
        check_error_bin = "message" in str(bincheck_output.json())
        if check_error_bin == True:
            embed=discord.Embed(title="Incorrect BIN number", description="```" + bincheck_output.json()["message"] + "```", color=0xf40101)
            embed.set_author(name="Pencord", icon_url="https://cdn.discordapp.com/attachments/860495176488452097/863506691277717564/DB-Icons-Pen-Testing.png")
            embed.set_thumbnail(url="https://cdn.icon-icons.com/icons2/1380/PNG/512/vcsconflicting_93497.png")
            embed.set_footer(text="Bot created by Markiemm#0001 https://markiemm.com")
            await message.channel.send(embed=embed)
            early_access_message=discord.Embed(title="A notice from the developer", description="This bot is currently in its early stages of development with only a very few commands available at this time. \n \n This bot may go offline at times while the developer Markiemm is still working on it and adding new features as well as making it stable and reliable. This is not the final product. ", color=0xff7024)
            early_access_message.set_author(name="Pencord", icon_url="https://cdn.discordapp.com/attachments/860495176488452097/863506691277717564/DB-Icons-Pen-Testing.png")
            early_access_message.set_thumbnail(url="https://www.pngkey.com/png/full/881-8812373_open-warning-icon-png.png")
            await message.channel.send(embed=early_access_message)
        else:
            while True:
                try:
                    char_edit_bin_ready = str(bincheck_output.json())
                    bin_edit_1 = char_edit_bin_ready.replace('"', "")
                    bin_edit_2 = bin_edit_1.replace(",", "\n")
                    bin_edit_3 = bin_edit_2.replace("{", "")
                    bin_edit_4 = bin_edit_3.replace("}", "")
                    bin_edit_5 = bin_edit_4.replace("'", "")
                    embed=discord.Embed(title="Status for bank identification number", description=bincheck_input, color=0xf40101)
                    embed.set_thumbnail(url="https://icons-for-free.com/iconfiles/png/512/card+credit+card+debit+card+master+card+icon-1320184902079563557.png")
                    embed.add_field(name="BIN Status:", value=bin_edit_5, inline=True)
                    embed.set_footer(text="Bot created by Markiemm#0001 https://markiemm.com")
                    await message.channel.send(embed=embed)
                    early_access_message=discord.Embed(title="A notice from the developer", description="This bot is currently in its early stages of development with only a very few commands available at this time. \n \n This bot may go offline at times while the developer Markiemm is still working on it and adding new features as well as making it stable and reliable. This is not the final product. ", color=0xff7024)
                    early_access_message.set_author(name="Pencord", icon_url="https://cdn.discordapp.com/attachments/860495176488452097/863506691277717564/DB-Icons-Pen-Testing.png")
                    early_access_message.set_thumbnail(url="https://www.pngkey.com/png/full/881-8812373_open-warning-icon-png.png")
                    await message.channel.send(embed=early_access_message)
                    break
                except:
                    embed=discord.Embed(title="OOPS!", description="```" + "Sorry, there was an error processing your request. Please try again later or contact Markiemm#0001" + "```", color=0xf40101)
                    embed.set_author(name="Pencord", icon_url="https://cdn.discordapp.com/attachments/860495176488452097/863506691277717564/DB-Icons-Pen-Testing.png")
                    embed.set_thumbnail(url="https://cdn.icon-icons.com/icons2/1380/PNG/512/vcsconflicting_93497.png")
                    embed.set_footer(text="Bot created by Markiemm#0001 https://markiemm.com")
                    await message.channel.send(embed=embed)
                    early_access_message=discord.Embed(title="A notice from the developer", description="This bot is currently in its early stages of development with only a very few commands available at this time. \n \n This bot may go offline at times while the developer Markiemm is still working on it and adding new features as well as making it stable and reliable. This is not the final product. ", color=0xff7024)
                    early_access_message.set_author(name="Pencord", icon_url="https://cdn.discordapp.com/attachments/860495176488452097/863506691277717564/DB-Icons-Pen-Testing.png")
                    early_access_message.set_thumbnail(url="https://www.pngkey.com/png/full/881-8812373_open-warning-icon-png.png")
                    await message.channel.send(embed=early_access_message)
                    break

    if message.content.startswith(config["bot_prefix"] + "ping"):
        before = time.monotonic()
        message = await message.channel.send("Pong")
        ping = (time.monotonic() - before) * 1000
        await message.channel.send(content=f"That took {int(ping)}ms")
        early_access_message=discord.Embed(title="A notice from the developer", description="This bot is currently in its early stages of development with only a very few commands available at this time. \n \n This bot may go offline at times while the developer Markiemm is still working on it and adding new features as well as making it stable and reliable. This is not the final product. ", color=0xff7024)
        early_access_message.set_author(name="Pencord", icon_url="https://cdn.discordapp.com/attachments/860495176488452097/863506691277717564/DB-Icons-Pen-Testing.png")
        early_access_message.set_thumbnail(url="https://www.pngkey.com/png/full/881-8812373_open-warning-icon-png.png")
        await message.channel.send(embed=early_access_message)

    if message.content.startswith(config["bot_prefix"] + "webping"):
        responce = str(message.content[9:]).split(' ', 1)[0]
        sanitized_word_output = re.match("([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}",responce).group(0)
        output_ping = os.popen("ping -c 3 " + str(sanitized_word_output))
        if output_ping.read() == "":
            embed=discord.Embed(title="pinging " + str(sanitized_word_output), description="I don't seem to know this domain. Is it a valid domain and don't include the http or https protocol.", color=0xf40101)
            embed.set_thumbnail(url="https://img.icons8.com/fluent/100/000000/ping-pong.png")
            embed.set_footer(text="Bot created by Markiemm#0001 https://markiemm.com")
            await message.channel.send(embed=embed)
            early_access_message=discord.Embed(title="A notice from the developer", description="This bot is currently in its early stages of development with only a very few commands available at this time. \n \n This bot may go offline at times while the developer Markiemm is still working on it and adding new features as well as making it stable and reliable. This is not the final product. ", color=0xff7024)
            early_access_message.set_author(name="Pencord", icon_url="https://cdn.discordapp.com/attachments/860495176488452097/863506691277717564/DB-Icons-Pen-Testing.png")
            early_access_message.set_thumbnail(url="https://www.pngkey.com/png/full/881-8812373_open-warning-icon-png.png")
            await message.channel.send(embed=early_access_message)
        else:
            output_ping = os.popen("ping -c 3 " + str(sanitized_word_output))
            await message.channel.send("Pinging " + str(sanitized_word_output) + "...")
            embed=discord.Embed(title="pinging " + str(sanitized_word_output), description=output_ping.read(), color=0xf40101)
            embed.set_thumbnail(url="https://img.icons8.com/fluent/100/000000/ping-pong.png")
            embed.set_footer(text="Bot created by Markiemm#0001 https://markiemm.com")
            await message.channel.send(embed=embed)
            early_access_message=discord.Embed(title="A notice from the developer", description="This bot is currently in its early stages of development with only a very few commands available at this time. \n \n This bot may go offline at times while the developer Markiemm is still working on it and adding new features as well as making it stable and reliable. This is not the final product. ", color=0xff7024)
            early_access_message.set_author(name="Pencord", icon_url="https://cdn.discordapp.com/attachments/860495176488452097/863506691277717564/DB-Icons-Pen-Testing.png")
            early_access_message.set_thumbnail(url="https://www.pngkey.com/png/full/881-8812373_open-warning-icon-png.png")
            await message.channel.send(embed=early_access_message)
    
    if message.content.startswith(config["bot_prefix"] + "domainlist"):
        sublist_responce = message.content[12:]
        await message.channel.send("Please wait, i'm getting domains that's related to " + sublist_responce)
        sublist_output = os.popen("pdlist " + sublist_responce)
        while True:
            try:
                embed=discord.Embed(title="subdomains for " + sublist_responce, description=str(sublist_output.read()[610:]), color=0xffc800)
                embed.set_thumbnail(url="https://image.flaticon.com/icons/png/512/1490/1490342.png")
                embed.set_footer(text="Bot created by Markiemm#0001 https://markiemm.com")
                await message.channel.send(embed=embed)
                early_access_message=discord.Embed(title="A notice from the developer", description="This bot is currently in its early stages of development with only a very few commands available at this time. \n \n This bot may go offline at times while the developer Markiemm is still working on it and adding new features as well as making it stable and reliable. This is not the final product. ", color=0xff7024)
                early_access_message.set_author(name="Pencord", icon_url="https://cdn.discordapp.com/attachments/860495176488452097/863506691277717564/DB-Icons-Pen-Testing.png")
                early_access_message.set_thumbnail(url="https://www.pngkey.com/png/full/881-8812373_open-warning-icon-png.png")
                await message.channel.send(embed=early_access_message)
                break
            except:
                embed=discord.Embed(title="OOPS!", description="```" + "Sorry, there was an error. It could be that the domain " + sublist_responce + " has too many subdomains to be listed here." + "```", color=0xf40101)
                embed.set_author(name="Pencord", icon_url="https://cdn.discordapp.com/attachments/860495176488452097/863506691277717564/DB-Icons-Pen-Testing.png")
                embed.set_thumbnail(url="https://cdn.icon-icons.com/icons2/1380/PNG/512/vcsconflicting_93497.png")
                embed.set_footer(text="Bot created by Markiemm#0001 https://markiemm.com")
                await message.channel.send(embed=embed)
                early_access_message=discord.Embed(title="A notice from the developer", description="This bot is currently in its early stages of development with only a very few commands available at this time. \n \n This bot may go offline at times while the developer Markiemm is still working on it and adding new features as well as making it stable and reliable. This is not the final product. ", color=0xff7024)
                early_access_message.set_author(name="Pencord", icon_url="https://cdn.discordapp.com/attachments/860495176488452097/863506691277717564/DB-Icons-Pen-Testing.png")
                early_access_message.set_thumbnail(url="https://www.pngkey.com/png/full/881-8812373_open-warning-icon-png.png")
                await message.channel.send(embed=early_access_message)
                break
    
    if message.content.startswith(config["bot_prefix"] + "cloudflare"):
        cloudflare_responce = str(message.content[12:]).split(' ', 1)[0]
        await message.channel.send("Please wait, i'm getting real IP address of " + cloudflare_responce)
        cloudflare_output = os.popen("python3 cloudfail.py -t " + cloudflare_responce)
        while True:
            try:
                embed=discord.Embed(title="Real IP for " + cloudflare_responce, description=cloudflare_output.read()[317:], color=0xffc800)
                embed.set_thumbnail(url="https://img.icons8.com/color/100/000000/cloudflare.png")
                embed.set_footer(text="Bot created by Markiemm#0001 https://markiemm.com")
                await message.channel.send(embed=embed)
                early_access_message=discord.Embed(title="A notice from the developer", description="This bot is currently in its early stages of development with only a very few commands available at this time. \n \n This bot may go offline at times while the developer Markiemm is still working on it and adding new features as well as making it stable and reliable. This is not the final product. ", color=0xff7024)
                early_access_message.set_author(name="Pencord", icon_url="https://cdn.discordapp.com/attachments/860495176488452097/863506691277717564/DB-Icons-Pen-Testing.png")
                early_access_message.set_thumbnail(url="https://www.pngkey.com/png/full/881-8812373_open-warning-icon-png.png")
                await message.channel.send(embed=early_access_message)
                break
            except:
                embed=discord.Embed(title="OOPS!", description="```" + "Something went wrong, try with a different domain or try again later." + "```", color=0xf40101)
                embed.set_author(name="Pencord", icon_url="https://cdn.discordapp.com/attachments/860495176488452097/863506691277717564/DB-Icons-Pen-Testing.png")
                embed.set_thumbnail(url="https://img.icons8.com/color/100/000000/cloudflare.png")
                embed.set_footer(text="Bot created by Markiemm#0001 https://markiemm.com")
                await message.channel.send(embed=embed)
                early_access_message=discord.Embed(title="A notice from the developer", description="This bot is currently in its early stages of development with only a very few commands available at this time. \n \n This bot may go offline at times while the developer Markiemm is still working on it and adding new features as well as making it stable and reliable. This is not the final product. ", color=0xff7024)
                early_access_message.set_author(name="Pencord", icon_url="https://cdn.discordapp.com/attachments/860495176488452097/863506691277717564/DB-Icons-Pen-Testing.png")
                early_access_message.set_thumbnail(url="https://www.pngkey.com/png/full/881-8812373_open-warning-icon-png.png")
                await message.channel.send(embed=early_access_message)
                break
        
    if message.content.startswith(config["bot_prefix"] + "changelog"):
        embed=discord.Embed(title="Changelog", color=0xff7b00)
        embed.set_author(name="Pencord", icon_url="https://cdn.discordapp.com/attachments/860495176488452097/863506691277717564/DB-Icons-Pen-Testing.png")
        embed.set_thumbnail(url="https://img.icons8.com/plasticine/100/000000/approve-and-update.png")
        embed.add_field(name="V1.1.2", value="- Fixed an vulnerability that allows users to add extra arguments to commands. Thanks to <@180006576428417024> for reporting this.", inline=False)
        embed.add_field(name="V1.1.1", value="- Big update to whois! Added new whois elements data.", inline=False)
        embed.add_field(name="V1.0.1", value="- Added a changelog \n - Fixed formatting on cloudflare scan. \n - Optimized the code", inline=False)
        embed.set_footer(text="Bot created by Markiemm#0001 https://markiemm.com")
        await message.channel.send(embed=embed)

    
# Run the bot with the token
bot.run(config["Main_Bot_token"])

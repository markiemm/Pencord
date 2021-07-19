from attr import astuple
import discord
import json
import sys
import os
import platform
import time
from discord import channel
import requests
from discord.ext import commands
import re

#load config
if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found!.")
else:
    with open("config.json") as file:
        config = json.load(file)
print("loaded config")


bot = commands.Bot(command_prefix=config["Bot_config"]["Bot_prefix"])



#variables
headers = {
            'apikey': config["Api_keys"]["promptapi_api_key"],
            }


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    print(f"Discord.py API version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print("-------------------")
    

bot.remove_command("help")

#please wait presets
please_wait=discord.Embed(title=config["Embeds"]["Please_wait"]["title"], description=config["Embeds"]["Please_wait"]["description"], color=0xff9029)
please_wait.set_author(name=config["Embeds"]["template"]["author"], icon_url=config["Embeds"]["template"]["icon_url"])
please_wait.set_thumbnail(url=config["Embeds"]["Please_wait"]["thumbnail"])
please_wait.set_footer(text=config["Embeds"]["template"]["footer"])


@bot.command()
async def help (message):
    embed=discord.Embed(title="How to use Pencord Discord bot", description="All the commands", color=0x0088ff)
    embed.set_author(name=config["Embeds"]["template"]["author"], icon_url=config["Embeds"]["template"]["icon_url"])
    embed.add_field(name=config["Bot_config"]["Bot_prefix"] + "help", value="Display all of the commands.", inline=True)
    embed.add_field(name=config["Bot_config"]["Bot_prefix"] + "whois", value="Display basic whois data for a domain or IP.", inline=True)
    embed.add_field(name=config["Bot_config"]["Bot_prefix"] + "fullwhois", value="Display full whois data with everything displayed.", inline=True)
    embed.add_field(name=config["Bot_config"]["Bot_prefix"] + "bincheck", value="Display the status of a Bank Identification Number.", inline=True)
    embed.add_field(name=config["Bot_config"]["Bot_prefix"] + "domainlist", value="Display related domains about the target domain.", inline=True)
    embed.add_field(name=config["Bot_config"]["Bot_prefix"] + "cloudflare", value="Attempt to get the real IP that's behind the cloudflare network.", inline=True)
    embed.add_field(name=config["Bot_config"]["Bot_prefix"] + "webping", value="Ping a website", inline=True)
    embed.add_field(name=config["Bot_config"]["Bot_prefix"] + "ping", value="Responds back the time it takes to recieve and send a message.", inline=True)
    embed.add_field(name=config["Bot_config"]["Bot_prefix"] + "dns", value="Displays the DNS records and its IP's **Note: You should not rely on this feature and conduct your own test as this feature may not display all DNS records**", inline=True)
    embed.add_field(name=config["Bot_config"]["Bot_prefix"] + "changelog", value="View the changelog of Pencord", inline=False)
    embed.set_footer(text=config["Embeds"]["template"]["footer"])
    await message.channel.send(embed=embed)

@bot.command()
async def whois(message, whois_domain):
    #send "please wait message"
    please_wait_message = await message.channel.send(embed=please_wait)

    #get the message ID of the "please wait message"
    msg_id_whois = please_wait_message.id

    #get the channel ID
    channel_id_whois = message.channel.id

    #make a request to promptapi
    api_whois_promptapi_out = requests.get("https://api.promptapi.com/whois/query?domain=" + whois_domain, headers=headers)
    api_whois_ipstack_out = requests.get("http://api.ipstack.com/" + whois_domain + "?access_key=" + config["Api_keys"]["busters_api"], headers=headers)

    embed=discord.Embed(title="Pencord Whois Data for " + whois_domain, description="Here is the basic Whois data for " + whois_domain, color=0x83ff61)
    embed.set_author(name=config["Embeds"]["template"]["author"], icon_url=config["Embeds"]["template"]["icon_url"])
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/866002022464487444/866410785936506880/1200px-VisualEditor_-_Icon_-_Open-book-2.svg.png")
    embed.set_footer(text=config["Embeds"]["template"]["footer"])

    embed.add_field(name="----------------------Location----------------------", value="-----------------------------------------------------", inline=False)
    embed.add_field(name="Country name", value=api_whois_ipstack_out.json()["country_name"], inline=True)
    embed.add_field(name="Continent name", value=api_whois_ipstack_out.json()["continent_name"], inline=True)
    embed.add_field(name="Region name", value=api_whois_ipstack_out.json()["region_name"], inline=True)
    embed.add_field(name="City", value=api_whois_ipstack_out.json()["city"], inline=True)
    embed.add_field(name="Zip Code", value=api_whois_ipstack_out.json()["zip"], inline=True)
    embed.add_field(name="Capital", value=api_whois_ipstack_out.json()["location"]["capital"], inline=True)

    embed.add_field(name="latitude", value=api_whois_ipstack_out.json()["latitude"], inline=True)
    embed.add_field(name="longitude", value=api_whois_ipstack_out.json()["longitude"], inline=True)

    embed.add_field(name="----------------------Codes----------------------", value="-------------------------------------------------", inline=False)
    embed.add_field(name="Country code", value=api_whois_ipstack_out.json()["country_code"], inline=True)
    embed.add_field(name="Continent code", value=api_whois_ipstack_out.json()["continent_code"], inline=True)
    embed.add_field(name="Region code", value=api_whois_ipstack_out.json()["region_code"], inline=True)
    embed.add_field(name="Geoname id", value=api_whois_ipstack_out.json()["location"]["geoname_id"], inline=True)
    embed.add_field(name="Calling code", value=str(api_whois_ipstack_out.json()["location"]["calling_code"]), inline=True)

    embed.add_field(name="----------------------Status----------------------", value="--------------------------------------------------", inline=False)
    embed.add_field(name="type", value=api_whois_ipstack_out.json()["type"], inline=True)
    embed.add_field(name="Is eu", value=str(api_whois_ipstack_out.json()["location"]["is_eu"]), inline=True)

    embed.add_field(name="----------------------Provider----------------------", value="--------------------------------------------------", inline=False)
    embed.add_field(name="Domain Provider", value=str(api_whois_promptapi_out.json()["result"]["registrar"]), inline=True)
    embed.add_field(name="Updated Date", value=str(api_whois_promptapi_out.json()["result"]["updated_date"]), inline=True)
    embed.add_field(name="Creation Date", value=str(api_whois_promptapi_out.json()["result"]["creation_date"]), inline=True)
    embed.add_field(name="Expiration date", value=str(api_whois_promptapi_out.json()["result"]["expiration_date"]), inline=True)
    embed.add_field(name="Emails", value=str(api_whois_promptapi_out.json()["result"]["emails"]), inline=True)
    await message.channel.send(embed=embed)

    #delete the "please wait" message
    await bot.http.delete_message(channel_id_whois, msg_id_whois)

@bot.command()
async def changelog (message):
    #send changelog embed
    embed=discord.Embed(title="Changelog (Bot version: V2.1.0)", color=0x0088ff)
    embed.set_author(name=config["Embeds"]["template"]["author"], icon_url=config["Embeds"]["template"]["icon_url"])
    embed.set_thumbnail(url="https://img.icons8.com/plasticine/100/000000/approve-and-update.png")
    embed.add_field(name="V2.1.0", value="- Added DNS lookup", inline=False)
    embed.add_field(name="V2.0.0", value="- Bot backend has been rewritten for stability, reliability, security and making it much more faster. Thanks to <@608636292301062184> for the help. \n \n - added **Please Wait** messages when performing a command.", inline=False)
    embed.add_field(name="V1.2.2", value="- Added more whois information.\n \n" + "- Whois is more user friendly to read.", inline=False)
    embed.add_field(name="V1.1.2", value="- Fixed an vulnerability that allows users to add extra arguments to commands. Thanks to <@180006576428417024> for reporting this.", inline=False)
    embed.add_field(name="V1.1.1", value="- Big update to whois! Added new whois elements data.", inline=False)
    embed.add_field(name="V1.0.1", value="- Added a changelog \n \n - Fixed formatting on cloudflare scan. \n \n - Optimized the code", inline=False)
    embed.set_footer(text=config["Embeds"]["template"]["footer"])
    await message.channel.send(embed=embed)

@bot.command()
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
        embed.set_author(name=config["Embeds"]["template"]["author"], icon_url=config["Embeds"]["template"]["icon_url"])
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/866002022464487444/866427540738801705/credit-card-icon-png-4424.png")
        embed.set_footer(text=config["Embeds"]["template"]["footer"])
        await message.channel.send(embed=embed)

    
    else:
        #send responce
        embed=discord.Embed(title="Status for bank identification number", description=bincheck_input, color=0x83ff61)
        embed.set_author(name=config["Embeds"]["template"]["author"], icon_url=config["Embeds"]["template"]["icon_url"])
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/866002022464487444/866427540738801705/credit-card-icon-png-4424.png")
        embed.add_field(name="BIN Status:", value=ready_output_bincheck, inline=True)
        embed.set_footer(text=config["Embeds"]["template"]["footer"])
        await message.channel.send(embed=embed)

    await bot.http.delete_message(channel_id_bincheck, message_id_bincheck)
    
@bot.command()
async def domainlist (message, sublist_responce):
    
    #send "please wait message"
    please_wait_message = await message.channel.send(embed=please_wait)

    #get message id
    message_id_domainlist = please_wait_message.id

    #get channel id
    channel_id_domainlist = message.channel.id

    sublist_output = os.popen("pdlist " + sublist_responce)

    try:
        embed=discord.Embed(title="subdomains for " + sublist_responce, description=sublist_output.read()[564:], color=0x83ff61)
        embed.set_author(name=config["Embeds"]["template"]["author"], icon_url=config["Embeds"]["template"]["icon_url"])
        embed.set_thumbnail(url="https://image.flaticon.com/icons/png/512/1490/1490342.png")
        embed.set_footer(text=config["Embeds"]["template"]["footer"])
        await message.channel.send(embed=embed)
        
    except:
        embed=discord.Embed(title="OOPS!", description="```" + "Sorry, there was an error. It could be that the domain " + sublist_responce + " has too many subdomains to be listed here." + "```", color=0xf40101)
        embed.set_author(name=config["Embeds"]["template"]["author"], icon_url=config["Embeds"]["template"]["icon_url"])
        embed.set_thumbnail(url="https://cdn.icon-icons.com/icons2/1380/PNG/512/vcsconflicting_93497.png")
        embed.set_footer(text=config["Embeds"]["template"]["footer"])
        await message.channel.send(embed=embed)

    await bot.http.delete_message(channel_id_domainlist, message_id_domainlist)

@bot.command()
async def cloudflare (message, cloudflare_responce):
    #send "please wait message"
    please_wait_message = await message.channel.send(embed=please_wait)

    #get message id
    message_id_cloudflare = please_wait_message.id

    #get channel id
    channel_id_cloudflare = message.channel.id

    cloudflare_output = os.popen("python3 cloudfail.py -t " + cloudflare_responce)

    embed=discord.Embed(title="Real IP for " + cloudflare_responce, description=cloudflare_output.read()[317:], color=0x83ff61)
    embed.set_author(name=config["Embeds"]["template"]["author"], icon_url=config["Embeds"]["template"]["icon_url"])
    embed.set_thumbnail(url="https://img.icons8.com/color/100/000000/cloudflare.png")
    embed.set_footer(text=config["Embeds"]["template"]["footer"])
    await message.channel.send(embed=embed)

    await bot.http.delete_message(channel_id_cloudflare, message_id_cloudflare)

@bot.command()
async def ping (message):
    before = time.monotonic()
    message = await message.channel.send("Pong")
    ping = (time.monotonic() - before) * 1000
    await message.channel.send(content=f"That took {int(ping)}ms")

@bot.command()
async def fullwhois (message, fullwhois_domain):
    #send "please wait message"
    please_wait_message = await message.channel.send(embed=please_wait)

    #get message id
    message_id_fullwhois = please_wait_message.id

    #get channel id
    channel_id_fullwhois = message.channel.id

    raw_fullwhois_api = requests.get("http://api.ipstack.com/" + fullwhois_domain + "?access_key=" + config["Api_keys"]["busters_api"], headers=headers)
    raw_whois_api_promptapi = requests.get("https://api.promptapi.com/whois/query?domain=" + fullwhois_domain, headers=headers)

    formatting_replace_fullwhois = str(raw_fullwhois_api.json()).replace(",", "\n").replace("'", "").replace("[{", "").replace("{", "").replace("}}", "")
    
    formatting_replace_promptapi = str(raw_whois_api_promptapi.json()).replace("{", "").replace('"', "").replace("_", " ").replace(",", "\n").replace("'", "").replace("}}", "")

    embed=discord.Embed(title="here is the full Whois output of " + fullwhois_domain, description=formatting_replace_fullwhois[12:] + "\n\n" + "**Some more information, these may be duplicates**" + "\n\n" + formatting_replace_promptapi[7:], color=0x83ff61)
    embed.set_author(name=config["Embeds"]["template"]["author"], icon_url=config["Embeds"]["template"]["icon_url"])
    embed.set_thumbnail(url="https://cdn.pixabay.com/photo/2017/05/24/07/05/searching-2339723_1280.png")
    embed.set_footer(text=config["Embeds"]["template"]["footer"])
    await message.channel.send(embed=embed)

    await bot.http.delete_message(channel_id_fullwhois, message_id_fullwhois)

@bot.command()
async def webping (message, webping_responce):
    #send "please wait message"
    please_wait_message = await message.channel.send(embed=please_wait)

    #get message id
    message_id_webping = please_wait_message.id

    #get channel id
    channel_id_webping = message.channel.id

    sanitized_word_output = re.match("([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}",webping_responce).group(0)
    
    output_ping = os.popen("ping -c 3 " + str(sanitized_word_output))
    
    if output_ping.read() == "":
        embed=discord.Embed(title="ping for " + str(sanitized_word_output), description="I don't seem to know this domain. Is it a valid domain and don't include the http or https protocol.", color=0xf40101)
        embed.set_author(name=config["Embeds"]["template"]["author"], icon_url=config["Embeds"]["template"]["icon_url"])
        embed.set_thumbnail(url="https://img.icons8.com/fluent/100/000000/ping-pong.png")
        embed.set_footer(text=config["Embeds"]["template"]["footer"])
        await message.channel.send(embed=embed)
    else:
        output_ping = os.popen("ping -c 3 " + str(sanitized_word_output))
        
        embed=discord.Embed(title="ping for " + str(sanitized_word_output), description=output_ping.read(), color=0xf40101)
        embed.set_author(name=config["Embeds"]["template"]["author"], icon_url=config["Embeds"]["template"]["icon_url"])
        embed.set_thumbnail(url="https://img.icons8.com/fluent/100/000000/ping-pong.png")
        embed.set_footer(text=config["Embeds"]["template"]["footer"])
        await message.channel.send(embed=embed)

    await bot.http.delete_message(channel_id_webping, message_id_webping)

@bot.command()
async def dns (message, dns_input):

    #send "please wait message"
    please_wait_message = await message.channel.send(embed=please_wait)

    #get message id
    message_id_dnslookup = please_wait_message.id

    #get channel id
    channel_id_dnslookup = message.channel.id

    sanitized_word_output_dnsenum = re.match("([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}",dns_input).group(0)
    
    output_dns = os.popen("dnsenum " + str(sanitized_word_output_dnsenum))

    remove_odd_shit = str(output_dns.read().replace("[1;34m", "").replace("[0m", "")).replace("[1;31m", "")[50:]

    embed=discord.Embed(title="Grabbing DNS records for " + dns_input, description=remove_odd_shit + "\n**Note: You should not rely on this feature and conduct your own test as this feature may not display all DNS records**", color=0xf40101)
    embed.set_author(name=config["Embeds"]["template"]["author"], icon_url=config["Embeds"]["template"]["icon_url"])
    embed.set_thumbnail(url="https://img.icons8.com/fluent/100/000000/ping-pong.png")
    embed.set_footer(text=config["Embeds"]["template"]["footer"])
    await message.channel.send(embed=embed)

    await bot.http.delete_message(channel_id_dnslookup, message_id_dnslookup)








bot.run(config["Bot_config"]["Main_Bot_Token"])

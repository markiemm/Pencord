from discord.ext import commands, tasks
from config import BOT_PREFIX, VERSION, BOT_TOKEN, TEST_BOT_TOKEN, PRESENCE
import discord
import platform
import os
import whois




bot = commands.Bot(command_prefix=BOT_PREFIX)
bot.remove_command("help")


for filename in os.listdir('./modules'):
    if filename.endswith('.py'):
        bot.load_extension(f'modules.{filename[:-3]}')



@bot.event
async def on_ready():
    # bot.user instead of bot.user.name to print the bot with the discriminator
    print(f"Logged in as {bot.user}")
    print(f"Discord.py API version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print("-"*22)
    await bot.change_presence(activity=discord.Game(PRESENCE))




admin_input = input("What bot do you want to run the script on: \n(1) - Main bot\n(2) - Test bot\n")
if admin_input == "1":
    bot.run(BOT_TOKEN)
elif admin_input == "2":
    bot.run(TEST_BOT_TOKEN)
else:
    print("You entered an incorrect choice")


@bot.event
async def on_message(message):

    if message.author == bot.user:
        return

    


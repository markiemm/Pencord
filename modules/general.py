from discord.ext import commands
import discord


class General(commands.Cog):
    def __init__(self, client):
        self.client = client



    @commands.command()
    async def help(self, message):
        await message.channel.send("hello")

        



def setup(client):
    client.add_cog(General(client))
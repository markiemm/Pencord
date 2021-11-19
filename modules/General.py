from discord.ext import commands
import discord
import json
from Template.info import AUTHOR, COLOR, ICON, THUMBNAIL
from config import BOT_PREFIX

class General(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, message):
        help_embed=discord.Embed(title="Pencord Command List", description=f"Prefix for this server is {BOT_PREFIX}", color=COLOR)
        help_embed.set_author(name=AUTHOR, icon_url=ICON)
        help_embed.set_thumbnail(url=THUMBNAIL)
        help_embed.add_field(name="General", value="```Help```", inline=True)
        help_embed.add_field(name="Pentest", value="```Whois```", inline=True)
        await message.send(embed=help_embed)



def setup(client):
    client.add_cog(General(client))
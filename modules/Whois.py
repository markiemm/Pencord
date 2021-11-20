from discord import user
from discord.ext import commands
import whois
import discord
from Template.pentest import AUTHOR, ICON, THUMBNAIL, COLOR


class Whois(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def whois(self, message, userinput):
        query = whois.whois(userinput)

        help_embed=discord.Embed(title="Whois", description=f"Here is the whois for {userinput}", color=COLOR)
        help_embed.set_author(name=AUTHOR, icon_url=ICON)
        help_embed.set_thumbnail(url=THUMBNAIL)

        help_embed.add_field(name="Domain", value=query.domain, inline=True)
        help_embed.add_field(name="Update Time", value=query.get('updated_date')[0], inline=True)
        help_embed.add_field(name="Expiration time", value=query.get('expiration_date'), inline=True)
        
        #need to figure out a better solution to handle email data
        help_embed.add_field(name="Emails", value="```" + str(query.get('emails')).replace("['", "").replace("',", "\n").replace("']", "").replace("'", "") + "```", inline=True)
        await message.send(embed=help_embed)

    @commands.command()
    async def whois2(self, message, userinput):
        await message.channel.send(whois.whois(userinput))


        

        
        



def setup(client):
    client.add_cog(Whois(client))
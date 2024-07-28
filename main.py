import discord
from discord.ext import commands
from discord import app_commands
import os
import functions
import requests
import datetime, time
import json


secretFile = open("hackathon week 1/OpenAI-Reddit-Toxicity-Calculator-main/clientsecret.json", "r")
secrets = json.load(secretFile)
DISCORD_KEY = secrets['DISCORD_KEY']


intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


async def getMessages(interaction: discord.Interaction):
    messages = [message async for message in interaction.channel.history(limit=10)]
    messageContents = []
    for i in messages:
        messageContents.append(i.content)
        
    return messageContents


@client.event
async def on_ready():

    #await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening ,name="^help"))
    await client.change_presence(activity=discord.Streaming(
        name="HeadStarter", url="https://www.twitch.tv/monketech"))

    await tree.sync()
    print("bot is up and running")



@tree.command(name="invite_bot",
              description="provides an invite link for the bot")
async def invite(interaction: discord.Interaction):

    await interaction.response.send_message(
        "https://discord.com/oauth2/authorize?client_id=1266847438837252268&permissions=563226979064896&integration_type=0&scope=bot"
    )


#shows all commands available from this bot
@tree.command(name="help")
async def help(interaction: discord.Interaction):
    helpEmbed = discord.Embed(title="**Commands**",
                              colour=0xFF7CEF)

    helpEmbed.add_field(
        name="Toxicity Bot",
        value="`/checkToxicity`",
        inline=True)
    helpEmbed.add_field(name="INVITE LINK", value="`/invite_bot`", inline=True)
    helpEmbed.set_thumbnail(
        url=
        ''
    )

    numServers = len(client.guilds)
    helpEmbed.set_footer(text="I am in " + str(numServers) + " servers.")

    await interaction.response.send_message(embed=helpEmbed)


@tree.command(name="check_toxicity")
async def check_toxicity(interaction: discord.Interaction):
    finalMessage = discord.Embed(title="Toxicity", colour=0xFF7CEF)
    
    messages = await getMessages(interaction)
    toxicityLevel = await functions.checkToxicity(messages)
    finalMessage.add_field(
        name="Result",
        value=f"`The toxicity value of the channel is {toxicityLevel[0]} out of 100. The main toxicity category is {toxicityLevel[1]}`",
        inline=True
    )
    

    numServers = len(client.guilds)
    finalMessage.set_footer(text="I am in " + str(numServers)  + " servers.")
    await interaction.response.send_message(embed=finalMessage)



# @tree.command(name="filler command")
# async def getName(interaction: discord.Interaction, filler: str):
#     await interaction.response.send_message(embed=filler)


# @tree.command(name="filler command")
# async def getdaily(interaction: discord.Interaction, hypixelguild: str):
    
#     await interaction.edit_original_response(embed=finalText)



client.run(DISCORD_KEY)
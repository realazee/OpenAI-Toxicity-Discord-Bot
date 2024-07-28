import discord
from discord.ext import commands
from discord import app_commands
import os
import functions
import requests
import datetime, time
import json


secretFile = open("clientsecret.json", "r")
secrets = json.load(secretFile)
DISCORD_KEY = secrets['DISCORD_KEY']


intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


async def getMessages(interaction: discord.Interaction, count: int):
    messages = [message async for message in interaction.channel.history(limit=count)]
    messageContents = []
    for i in messages:
        messageContents.append(i.content)
        
    return messageContents


async def getUserMessages(interaction: discord.Interaction, member: discord.Member, count: int):
    messages = [message async for message in interaction.channel.history(limit=1000)]
    userMessages = [msg for msg in messages if msg.author == member]
    if len(userMessages) < 1:
        return None
    
    messageContents = []
    for i in range(min(len(userMessages),count)):
        messageContents.append(userMessages[i].content)

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
@tree.command(name="help",
              description="A help menu for the Toxicity Calculator Bot")
async def help(interaction: discord.Interaction):
    helpEmbed = discord.Embed(title="**Commands**",
                              colour=0xFF7CEF)

    helpEmbed.add_field(
        name="Toxicity Checker",
        value="`/check_toxicity [limit]`",
        inline=True)
    helpEmbed.add_field(
        name="User Toxicity Checker",
        value="`/check_user_toxicity [user] [limit]`",
        inline=True)
    helpEmbed.add_field(name="INVITE LINK", value="`/invite_bot`", inline=True)
    helpEmbed.set_thumbnail(
        url=
        ''
    )

    numServers = len(client.guilds)
    helpEmbed.set_footer(text="I am in " + str(numServers) + " servers.")

    await interaction.response.send_message(embed=helpEmbed)


@tree.command(name="check_toxicity",
              description="Checks the toxicity level of the current channel based on the num most recent messages"
)
async def check_toxicity(interaction: discord.Interaction, num: int):
    finalMessage = discord.Embed(title="Toxicity", colour=0xFF7CEF)
    if num > 100 or num < 1:
        await interaction.response.send_message("Please enter a value between 1 and 100", ephemeral=True)
    else:
        await interaction.response.defer()
        messages = await getMessages(interaction, num)
        toxicityLevel = await functions.checkToxicity(messages)
        if toxicityLevel[2]:
            finalMessage.add_field(
                name="Result",
                value=f"`The toxicity value of the channel is {toxicityLevel[0]} out of 100. The main toxicity category is {toxicityLevel[1]}`",
                inline=True
            )
        else:
            finalMessage.add_field(
                name="Result",
                value=f"`The toxicity value of the channel is {toxicityLevel[0]} out of 100. The chat is not toxic.`",
                inline=True
            )

    numServers = len(client.guilds)
    finalMessage.set_footer(text="I am in " + str(numServers)  + " servers.")
    await interaction.edit_original_response(embed=finalMessage)


@tree.command(name="check_user_toxicity",
              description="Checks the toxicity level of a user in the current channel"
              )
async def check_user_toxicity(interaction: discord.Interaction, member: discord.Member, num: int):
    finalMessage = discord.Embed(title="Toxicity", colour=0xFF7CEF)
    if num > 100 or num < 1:
        await interaction.response.send_message("Please enter a value between 1 and 100", ephemeral=True)

    else:
        await interaction.response.defer()
        messages = await getUserMessages(interaction, member, num)
        if messages == None:
            await interaction.response.send_message("Not enough recent messages", ephemeral=True)

        toxicityLevel = await functions.checkToxicity(messages)
        if toxicityLevel[2]:
            finalMessage.add_field(
                name="Result",
                value=f"`The toxicity value of {member} is {toxicityLevel[0]} out of 100. The main toxicity category is {toxicityLevel[1]}`",
                inline=True
            )
        else: 
            finalMessage.add_field(
                name="Result",
                value=f"`The toxicity value of {member} is {toxicityLevel[0]} out of 100. The user in this chat is not toxic.`",
                inline=True
            )
    
    numServers = len(client.guilds)
    finalMessage.set_footer(text="I am in " + str(numServers)  + " servers.")
    await interaction.edit_original_response(embed=finalMessage)


client.run(DISCORD_KEY)
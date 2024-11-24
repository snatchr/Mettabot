#Imports
import discord.ext.commands
from roblox import Client
from discord.ext import commands
from discord import app_commands
from dotenv import find_dotenv, load_dotenv
from ast import literal_eval

import rblxopencloud
import os
import discord
import discord.ext
import storage
import requests
#Setting up some stuff
envpath = find_dotenv()
load_dotenv(envpath)
token = os.getenv("BotToken")
game = rblxopencloud.Experience(3498834789, os.getenv("ApiKey"))
datastore = game.get_data_store("DataStore")
bot = commands.Bot(command_prefix="R!", intents=discord.Intents.all())
roblox = Client()
#Debugging
@bot.event
async def on_ready():
    print("Logged in as " + bot.user.name)
    try:
      synced = await bot.tree.sync()
      print(f"Synced {len(synced)} command(s)")
    except Exception as e:
       print(f"Error syncing commands: {e}")
#Commands
@bot.command()
async def hello(ctx):
    await ctx.send("Hello!")

@bot.command()
async def whois(ctx, username):
    user = await roblox.get_user_by_username(username)
    if user:
     displayname = user.display_name
     joindate = user.created.date()
     isbanned = user.is_banned
     description = user.description
     hasplayedutr = bool(user.get_badge_awarded_dates([2127151760]))
     followers = await user.get_follower_count()
     embed=discord.Embed(title=displayname + "(@" + username + ")", color=0xff0000)
     embed.add_field(name="Join Date", value=joindate, inline=True)
     embed.add_field(name="Banned", value=isbanned, inline=True)
     embed.add_field(name="Followers", value=followers, inline=True)
     embed.add_field(name="Description", value=description, inline=True)
     embed.set_footer(text="Played UTR: " + str(hasplayedutr))
     await ctx.send(embed=embed)
@bot.command()
async def getspecificstat(ctx, id, itemtype):
    value, info = datastore.get('Player' + str(id))
    if value and info:
     res = {key: value[key] for key in value.keys()
        & {itemtype}}
     await ctx.send(res)
    else:
     await ctx.send("Failed.")
@bot.command()
async def getstats(ctx, id):
    value, info = datastore.get('Player' + str(id))
    if value and info:
     player = await roblox.get_user(id)
     playername = player.display_name
     playeruser = player.name
     res1 = {key: value[key] for key in value.keys() & {'Weapons'}}
     res2 = {key: value[key] for key in value.keys() & {'Armors'}}
     res3 = {key: value[key] for key in value.keys() & {'SOULs'}}
     res4 = {key: value[key] for key in value.keys() & {'Food'}}
     res5 = {key: value[key] for key in value.keys() & {'EXP'}}
     res6 = {key: value[key] for key in value.keys() & {'Gold'}}
     res7 = {key: value[key] for key in value.keys() & {'Resets'}}
     res8 = {key: value[key] for key in value.keys() & {'LOVE'}}
     res9 = {key: value[key] for key in value.keys() & {'TrueResets'}}
     embed=discord.Embed(title=playername + " (@" + playeruser + ")", color=0xff0000)
     embed.add_field(name="LOVE", value=res8, inline=True)
     embed.add_field(name="EXP", value=res5, inline=True)
     embed.add_field(name="Gold", value=res6, inline=True)
     embed.add_field(name="Resets", value=res7, inline=True)
     embed.add_field(name="True Resets", value=res9, inline=True)
     embed.add_field(name="Weapons", value=res1, inline=False)
     embed.add_field(name="Armors", value=res2, inline=False)
     embed.add_field(name="SOULs", value=res3, inline=False)
     embed.add_field(name="Food", value=res4, inline=True)
     await ctx.send(embed=embed)
    else:
     await ctx.send("Failed.")
@bot.tree.command(name="slashcommandtest")
async def test(interaction: discord.Interaction):
   await interaction.response.send_message("hi spongebob")

#@bot.tree.command(name="getuserid", description="Gets the roblox user ID of a discord user.")
#@app_commands.describe(user='The discord user.')
#async def test(interaction: discord.Interaction):
#   response = requests.get('https://api.blox.link/v4/public/guilds/789699000047370261/discord-to-roblox/214858075650260992',  headers={"Authorization" : "key"})
#   await interaction.response.send_message(str(response.json()))

@bot.event
async def on_command_error(ctx, error):
   if isinstance(error, commands.BadArgument):
      embed=discord.Embed(color=0x090707)
      embed.add_field(name="Error: Bad Argument (Discord)", value="One of the arguments that was input is incorrect.", inline=False)
      await ctx.send(embed=embed)
   elif isinstance(error, commands.MissingRequiredArgument):
      embed=discord.Embed(color=0x090707)
      embed.add_field(name="Error: Missing Required Argument (Discord)", value="Command input is missing an argument that is required.", inline=False)
      await ctx.send(embed=embed)
   elif isinstance(error, commands.TooManyArguments):
      embed=discord.Embed(color=0x090707)
      embed.add_field(name="Error: Too many arguments (Discord)", value="Exception raised when the command was passed too many arguments and its Command.ignore_extra attribute was not set to True.", inline=False)
      await ctx.send(embed=embed)
   elif isinstance(error, commands.CommandNotFound):
      embed=discord.Embed(color=0x090707)
      embed.add_field(name="Error: Command not found (Discord)", value="Exception raised when trying to execute a command that does not exist.", inline=False)
      await ctx.send(embed=embed)
   elif isinstance(error, rblxopencloud.exceptions.PermissionDenied):
      embed=discord.Embed(color=0x090707)
      embed.add_field(name="Error: Permission Denied", value="API key does not have all of the necessary permissions.", inline=False)
      await ctx.send(embed=embed)
   elif isinstance(error, rblxopencloud.exceptions.InvalidKey):
      embed=discord.Embed(color=0x090707)
      embed.add_field(name="Error: Permission Denied", value="API key is invalid. Please re-check.", inline=False)
      await ctx.send(embed=embed)
# @getstats.error
# async def getstats_error(ctx, error):
#    if isinstance(error, commands.BadArgument):
#       embed=discord.Embed(color=0x090707)
#       embed.add_field(name="Error: Bad Argument", value="Exception raised when a parsing or conversion failure is encountered on an argument to pass into a command.", inline=False)
#       await ctx.send(embed=embed)
#    elif isinstance(error, commands.MissingRequiredArgument):
#       embed=discord.Embed(color=0x090707)
#       embed.add_field(name="Error: Missing Required Argument", value="Exception raised when parsing a command and a parameter that is required is not encountered.", inline=False)
#       await ctx.send(embed=embed)
#    elif isinstance(error, commands.TooManyArguments):
#       embed=discord.Embed(color=0x090707)
#       embed.add_field(name="Error: Too many arguments", value="Exception raised when the command was passed too many arguments and its Command.ignore_extra attribute was not set to True.", inline=False)
#       await ctx.send(embed=embed)
#    elif isinstance(error, commands.CommandNotFound):
#       embed=discord.Embed(color=0x090707)
#       embed.add_field(name="Error: Command not found", value="Exception raised when trying to execute a command that does not exist.", inline=False)
#       await ctx.send(embed=embed)
# @getspecificstat.error
# async def getspecificstat_error(ctx, error):
#    if isinstance(error, commands.BadArgument):
#       embed=discord.Embed(color=0x090707)
#       embed.add_field(name="Error: Bad Argument", value="Exception raised when a parsing or conversion failure is encountered on an argument to pass into a command.", inline=False)
#       await ctx.send(embed=embed)
#    elif isinstance(error, commands.MissingRequiredArgument):
#       embed=discord.Embed(color=0x090707)
#       embed.add_field(name="Error: Missing Required Argument", value="Exception raised when parsing a command and a parameter that is required is not encountered.", inline=False)
#       await ctx.send(embed=embed)
#    elif isinstance(error, commands.TooManyArguments):
#       embed=discord.Embed(color=0x090707)
#       embed.add_field(name="Error: Too many arguments", value="Exception raised when the command was passed too many arguments and its Command.ignore_extra attribute was not set to True.", inline=False)
#       await ctx.send(embed=embed)
# @whois.error
# async def whois_error(ctx, error):
#    if isinstance(error, commands.BadArgument):
#       embed=discord.Embed(color=0x090707)
#       embed.add_field(name="Error: Bad Argument", value="Exception raised when a parsing or conversion failure is encountered on an argument to pass into a command.", inline=False)
#       await ctx.send(embed=embed)
#    elif isinstance(error, commands.MissingRequiredArgument):
#       embed=discord.Embed(color=0x090707)
#       embed.add_field(name="Error: Missing Required Argument", value="Exception raised when parsing a command and a parameter that is required is not encountered.", inline=False)
#       await ctx.send(embed=embed)
#    elif isinstance(error, commands.TooManyArguments):
#       embed=discord.Embed(color=0x090707)
#       embed.add_field(name="Error: Too many arguments", value="Exception raised when the command was passed too many arguments and its Command.ignore_extra attribute was not set to True.", inline=False)
#       await ctx.send(embed=embed)
       
#Running
bot.run(token)

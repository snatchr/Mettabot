#Imports
from roblox import Client
from discord.ext import commands
from dotenv import find_dotenv, load_dotenv
from ast import literal_eval
from keep_alive import keep_alive
keep_alive()

import rblxopencloud
import os
import discord
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
       
#Running
bot.run(token)
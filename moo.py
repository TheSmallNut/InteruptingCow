import discord
import json
import tokens
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions


def openJsonDoc(nameOfDoc="people"):
    with open(f'{str(nameOfDoc)}.json', 'r') as f:
        data = json.load(f)
    return data


people = openJsonDoc()


def getGuildIndex(guild):
    for i in range(len(people["guilds"])):
        if people["guilds"][i]["id"] == guild.id:
            return int(i)
    return -1


def writeJsonDoc(dumpData=people, location="people"):
    with open(f'{location}.json', 'w') as f:
        json.dump(dumpData, f, indent=4)


def get_prefix(client, message):
    return people["guilds"][getGuildIndex(message.guild)]["prefix"]


bot = discord.Client()
bot = commands.Bot(command_prefix=get_prefix)


@ bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")


@ bot.event
async def on_guild_join(guild):
    people["guilds"].append({})
    location = people["guilds"][-1]
    location["id"] = guild.id
    location["name"] = guild.name
    location["prefix"] = "$"
    location["region"] = guild.region
    location["mooUser"] = []
    writeJsonDoc()


@ bot.event
async def on_message(ctx):
    await bot.process_commands(ctx)


@ bot.command(name="mooUser", aliases=["mU", "mu", "moo", "MOO", "MOOUSER", "mooMember"])
@ has_permissions(manage_channels=True)
async def _mooUser(ctx, member: discord.member):
    print(member)

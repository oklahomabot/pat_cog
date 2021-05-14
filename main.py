import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

intents = discord.Intents.all()
intents.members = True
prefix = '!ok '

load_dotenv()
dTOKEN = os.getenv('dTOKEN')
client = commands.Bot(command_prefix=prefix,
                      intents=intents, owner_id=int(os.getenv('OwnerID')))

# cog_list from all .py files in folder cogs
cogs = [fn[:-3] for fn in os.listdir(os.path.join(
        './', 'cogs')) if fn.endswith('.py')]

# cog loader
for cog in cogs:
    try:
        client.load_extension(f'cogs.{cog}')
    except Exception as e:
        print(f'Could not load cog {cog}: {str(e)}')
    else:
        print(f'{cog} cog loaded')


def list_guilds():
    for g in client.guilds:
        print(f'{g.name:25} ({g.id}) - {g.member_count} members')


@client.event
async def on_ready():
    print(
        f'We have logged in as {client.user} a member of {len(client.guilds)} guilds')
    list_guilds()
    await client.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching, name=f'for {prefix} command'))


client.run(dTOKEN)

import os
import discord
import aiohttp
from discord.ext import commands
from PIL import Image
from io import BytesIO
from functools import partial


class pat(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.owner = discord.ClientUser

        # create a ClientSession
        self.session = aiohttp.ClientSession(loop=client.loop)

    @staticmethod
    def make_pat_gif(avatar):
        folder = os.path.join('./', 'cogs', 'pat', 'images')
        sizex, sizey = 112, 112
        avatar_sizes = [(90, 70), (90, 70), (95, 60), (97, 55),
                        (100, 50), (97, 55), (95, 60), (90, 70)]
        background = Image.open(os.path.join(folder, 'background.png'))
        frames = []
        for img_num in range(8):
            frame = background.copy()
            av = avatar.resize(avatar_sizes[img_num])
            av_width = avatar_sizes[img_num][0]
            av_height = avatar_sizes[img_num][1]
            hand = Image.open(os.path.join(
                folder, 'hands', f'{str(img_num)}.png'))
            frame.alpha_composite(
                av, dest=((sizex-av_width)//2, sizey-av_height))
            frame.alpha_composite(hand, dest=((0, int(1.5*(70-av_height)))))
            frames.append(frame)
        outfile = os.path.join(folder, 'output.gif')
        frames[0].save(outfile, 'GIF', disposal=2, transparency=0, save_all=True,
                       append_images=frames[1:], optimize=False, duration=12, loop=0)
        return outfile

    @commands.command(aliases=['pet_pat'], hidden=False)
    async def pat(self, ctx, user=None):
        '''
        Good Boy ...
        Returns gif image using mentioned user
        '''

        user = await get_guild_member(ctx, user)
        avatar = await make_avatar(user)

        # create partial function so we don't have to stack the args in run_in_executor
        fn = partial(self.make_pat_gif, avatar)
        outfile = await self.client.loop.run_in_executor(None, fn)
        await ctx.send(file=discord.File(outfile))
        os.remove(outfile)


async def make_avatar(user):
    asset = user.avatar_url_as(static_format='png')
    data = BytesIO(await asset.read())
    im = Image.open(data)
    im = make_RGBA(im)
    return im


async def get_guild_member(ctx, user=None):
    try:
        user = await commands.converter.MemberConverter().convert(ctx, user)
    except:
        user = ctx.author
    return user


def make_RGBA(im):
    if im.mode == 'RGBA':
        return im
    im = im.convert('RGBA')
    im.putalpha(255)
    return im


def setup(client):  # Cog setup command
    client.add_cog(pat(client))

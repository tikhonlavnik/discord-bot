import discord
from discord.ext.commands import Bot

from config import Config
from utils.vk_utils import Vk


bot = Bot(command_prefix="/", intents=discord.Intents.all())


@bot.event
async def on_ready():
    print(f"{bot.user.name} is working")


@bot.command(name="get_info")
async def get_info(ctx, vk_link):
    try:
        vk_id = vk_link.split("/")[-1]
        info = Vk.get_vk_entity_info(vk_id)
        title = discord.Embed(title=f"VK Info - {vk_id}", color=discord.Color.blue())
        await ctx.send(embed=title)
        await ctx.send(info)
    except Exception as e:
        print(e)
        title = discord.Embed(
            title=f"Ошибка - неверная ссылка", color=discord.Color.red()
        )
        await ctx.send(embed=title)


if __name__ == "__main__":
    bot.run(Config.BOT_TOKEN)

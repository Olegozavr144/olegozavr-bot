from discord.ext import commands
import os

bot = commands.Bot(command_prefix="#", case_insensitive=True)


@bot.event
async def on_ready():
    print(f"{bot.user.name} приветствует!")


@bot.event
async def on_command_error(ctx, error):
    print(f"{ctx.author} не прав!")
    print(f"{error} Обалдеть!")


@bot.command(name="ping", aliases=["пинг"], help="Ну кароч такие дела")
async def ping(ctx):
    await ctx.send(f"pong {ctx.author.mention}")


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.run(os.environ.get("BOT_TOKEN", open("token.txt").readline()))

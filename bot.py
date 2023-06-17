import discord
from discord.ext import commands
import requests 
import keygen

api = "http://5.249.163.196:1337"
tkn = "MTExOTUzODU2Mjk1ODg4ODk5MA.GqXI12.o2ZH4NEt1mJYidfHE4PdFjclvzGmVi6N9xz9mc"
client = commands.Bot(command_prefix=".", intents=discord.Intents.all())

@client.event
async def on_ready():
    print("Bot is ready")

@client.event
async def on_command_error(ctx, error): 
    if isinstance(error, commands.CommandNotFound):
        return
    em = discord.Embed(title="Error", description=f"```{error}```", color=00000)
    await ctx.send(embed=em)

@client.command()
@commands.cooldown(1, 60, commands.BucketType.user)
async def status(ctx, guild_id= None):
    msg = await ctx.send("Fetching.....")
    if guild_id == None:
        r = requests.get(api + "/status")
        if r.status_code == 200:
            if r.json() == []:
                return await msg.edit("No running tasks.")
            embed = discord.Embed(title="Running Tasks", description="", color=00000)
            for guild in r.json():
                print(type(guild))
                total = open("guilds/"+guild+"-total.txt", "r").read()
                added = open("guilds/"+guild+".txt", "r").read()
                print(total, added)
                remaining = int(total) - int(added)
                embed.description += f"Guild: `{guild}`\nAdded: `{added}/{total}`\nRemaining: `{remaining}`\nSpeed: `60/m`\n\n"

            await ctx.send(embed=embed)
        else:
            await ctx.send("Error: API didn't respond.")
    else:
        r = requests.get(api + "/status")
        if r.status_code == 200:
            if guild_id not in r.json():
                return await ctx.send("No Running task found for guild: " + guild_id)
            else:
                total = open("guilds/"+guild_id+"-total.txt", "r").read()
                added = open("guilds/"+guild_id+".txt", "r").read()
                remaining = int(total) - int(added)
                em = discord.Embed(title=f"Status - {guild_id}", description="", color=00000)
                em.description += f"Guild: `{guild_id}`\nAdded: `{added}/{total}`\nRemaining: `{remaining}`\nSpeed: `60/m`\n\n"
                await ctx.send(embed=em)
        else:
            await ctx.send("Error: API didn't respond.")

        # await ctx.send(f"Guild: {guild} | Status: Running")
        
@client.command(aliases=['gen'])
async def generate(ctx, key_type:str, start:int, total:int, uses=None):
    if not ctx.author.guild_permissions.administrator:
        return await ctx.send("unauthorized")
    if "exploit" not in ctx.author.name.lower():
        return await ctx.send("unauthorized")
    key, url = keygen.generate_key(key_type=key_type, total=total, start=start, uses=uses)
    em = discord.Embed(title="Key Generated", description=f"Key: `{key}`\nType: `{key_type}`\nAmount: `{total}`\n\nBot Invite: [Click here to Invite]({url})\n\nNote: It will start automatically as soon as you add the bot, if didn't start re add without kicking the bot and let the redirected page load. If the redirected page dosen't load, copy paste it and type command .redeem <redirected-url> in your ticket to trigger joiner.", color=00000)
    await ctx.send(embed=em)
    
@client.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def redeem(ctx, url):
    r = requests.get(url)
    em = discord.Embed(description=f"{r.json()}", color=00000)
    return await ctx.send(embed=em)

@client.command()
async def ltc(ctx): 
    await ctx.send("LeUUjdR44S9314Y3LQUW1JeS4HCsDt6mK1")
    await ctx.send("ltc addy ^^")

@client.command()
async def mail(ctx): 
    await ctx.send("**requested1337@protonmail.com**")
    await ctx.send("Coinbase / Binance mail ^")

@client.command()
async def upi(ctx):
    await ctx.send("exploit@fam")

@client.command()
async def calc(ctx, *, expression):
    sol = eval(expression)
    await ctx.send(f"{expression} = {sol}")
client.run(tkn)
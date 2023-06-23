import discord 
from discord.ext import commands 
import asyncio, re, os
client = commands.Bot(command_prefix = '.', self_bot = True)

@client.event
async def on_ready():
    os.system("cls")
    print("connnected;", client.user) 
          
invite_regex = r'has (\d+) invites'

@client.event 
async def on_message(msg):
    try: 
      if not msg.guild.id == 1119537103106228275:
          return
      if not "ticket" in msg.channel.name: 
          return 
      if not msg.author.id == 557628352828014614: 
          return
      if not "welcome" in msg.content.lower(): 
          return
      member = msg.mentions[0]
      f = open("claimed.txt", "r").read().splitlines()
      if str(member.id) in f:
          return await msg.channel.send("You have already claimed your invite reward, if you wanna purchase members, let us know amount, and type.")
      await msg.channel.send(f"-i {member.id}")
      await asyncio.sleep(1)
      async for message in msg.channel.history(limit=1):
          if not message.author.id == 899899858981371935:
              return await msg.channel.send("Failed to fetch invites, please re create ticket and do not send any message in ticket.")
          em_desc = message.embeds[0].description
          # print(em_desc+"\n\n")
          matches = re.search(invite_regex, em_desc)
          if matches:
              invites = int(matches.group(1))
              print(f"{member} | Invites: {invites}")
              if invites == 0: 
                  return await msg.channel.send("You don't have any invites, if you wanna purchase members, let us know amount, and type.")
              await msg.channel.send(f"-invited {member.id}")
              await msg.channel.send(f"-clearinvites {member.id}")
              f = open("claimed.txt", "a")
              f.write(f"{member.id}\n")
              if invites < 6:
                  tokens = invites*45
                  return await msg.channel.send(f".gen offline 0 {tokens}")
              elif invites < 11:
                  tokens = invites*55
                  return await msg.channel.send(f".gen offline 0 {tokens}")
              elif invites < 15:
                  tokens = invites*65
                  return await msg.channel.send(f".gen offline 0 {tokens}")
              elif invites >= 15:
                  return await msg.channel.send(f".gen offline 0 1000")
              else:
                  return await msg.channel.send("Failed to fetch invites, please re create ticket and do not send any message in ticket.")
          else:
              print("No invites found.")
              return await msg.channel.send("Failed to fetch invites, please re create ticket and do not send any message in ticket.")
          
    except:
        return 


client.run("MTA4NTg4MzI0ODgxNjcwMTQ2MA.GCkqpn.QHnUIO87omDkPqZXo9byOoTGZj-txbz4u4AvPg")

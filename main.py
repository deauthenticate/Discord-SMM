import os, sys
import json, time
import requests
from flask import Flask, request, jsonify, redirect
from threading import Thread

os.system("clear")
app = Flask(__name__)

API_ENDPOINT = 'https://canary.discord.com/api/v9'

def update_join_count(guild_id):
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


def add_to_guild(access_token, userID , guild_Id, key_type):
    tkn = 'MTEwNDA3NzQ1NDIzMjAwMjY2MA.G6VpKs.owC4YB7uPj_5QNdiyuS8m5qnoScZd4bMLJZ5Mc' if key_type == 'offline' else 'MTEwNTcyMjMwMzk3MjY1MTA4OA.GlqJ8A.g-lST32PyBVQ3-US3ggTGQ-RSdjVABkqyUntvk'
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
            return 
          c = update_join_count(guild_Id)
          print(f"{c} [{key_type.upper()}]: successfully added {userID} to {guild_Id}")
          break
        elif response.status_code == 429:
           if 'retry_after' in response.text:
               sleepxd = int(response.json()['retry_after'])
               print("sleeping for:", sleepxd, "seconds")
               time.sleep(sleepxd)
               continue
           else:
             os.system("kill 1")
        elif "missing perm" in response.text.lower():
          return "perms error"
        break

def joiner(guild_id, key_type, start_from, amount):
    with open(f'{key_type}.txt', 'r') as f:
        count = 0
        for line in f:
            if count < start_from:
                count += 1
                continue
            if count >= start_from + amount:
                break
            user_id, access_token, re = line.strip().split(':')
            ok = add_to_guild(access_token, user_id, guild_id, key_type)
            count += 1
            try:
              if "perms error" in ok:
                print("bot removed")
                break
            except:
              pass





@app.route('/')
def home():
    return jsonify({'discord': 'exploit#1337'}), 400

@app.route('/callback')
def callback():
    try:
      code = request.args.get('code')
      guild_id = request.args.get('guild_id')
      key = request.args.get('state')  
    except:
      return "error"
    with open('keys.json', 'r') as f:
      keys_data = json.load(f)
    key_data = keys_data.get(key)
    if key_data is None:
        return jsonify({'error': 'Invalid key'}), 400

    uses_remaining = key_data['uses']
    if uses_remaining == 0:
        return jsonify({'error': 'Key already redeemed or has no uses remaining'}), 400

    key_data['uses'] -= 1
    with open('keys.json', 'w') as f:
        json.dump(keys_data, f, indent=4)
    key_type = key_data['type']
    amount = key_data['amount']
    start_from = key_data['start']
    Thread(target=joiner, args=(guild_id, key_type, start_from, amount)).start()
    uses_remaining -= 1
    return jsonify({
        'key': key,
        'uses_remaining': uses_remaining,
        'type': key_type,
        'amount': amount,
        'status': 'success',
        'guild': str(guild_id)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1337)

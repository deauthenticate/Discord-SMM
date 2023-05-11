import sys
import random
import string
import json

if len(sys.argv) < 5:
    print('Usage: python generator.py type start total [uses]')
    sys.exit(1)

key_type = sys.argv[1]
total = int(sys.argv[3])
start = int(sys.argv[2])

uses = int(sys.argv[4]) if len(sys.argv) >= 6 else None
if uses is not None:
    uses = int(uses)

key = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

new_key = {
    key: {
        'uses': uses if uses is not None else 1,
        'amount': total,
        'type': key_type,
        'start': start
    }
}

with open('keys.json', 'r+') as f:
    data = json.load(f)
    data.update(new_key)
    f.seek(0)
    json.dump(data, f, indent=4)

client_id = '1104077454232002660' if key_type == 'offline' else '1105722303972651088'

redirect_uri = 'https://tokens-puller.void1337.repl.co/callback'
state = key

discord_url = f"https://discord.com/api/oauth2/authorize?client_id={client_id}&permissions=1&redirect_uri={redirect_uri}&response_type=code&scope=identify%20bot&state={state}"

print(f'New key generated: {key}')
print(f'Discord bot URL: {discord_url}')

f = open("a.txt", "a")
f.write(discord_url + "\n\n")

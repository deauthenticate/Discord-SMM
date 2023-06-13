import sys
import random
import string
import json
from dhooks import Webhook
hook = Webhook("https://discord.com/api/webhooks/1118083019614453870/8qzbD7DMP9ntp6rS-qeO3UpkMcV7xglrS3A-AG8vIhs_NLLuWj3d5O1sP8g0gSdYSDtp")
offline_client_id = "1116662925214613555"
online_client_id = "1116678826139848813"
redirect_uri = 'http://5.249.163.196:1337/callback'

if len(sys.argv) < 5:
    print('Usage: python generator.py type start total [uses]')
    sys.exit(1)
key_type = sys.argv[1]
total = int(sys.argv[3])
start = int(sys.argv[2])

try:
  uses = int(sys.argv[4])
except:
  uses = 1


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

client_id = offline_client_id if key_type == 'offline' else online_client_id
state = key

discord_url = f"https://discord.com/api/oauth2/authorize?client_id={client_id}&permissions=1&redirect_uri={redirect_uri}&response_type=code&scope=identify%20bot&state={state}"

print(f'New key generated: {key}')
print(f'Discord bot URL: {discord_url}')
hook.send(discord_url)

f = open("a.txt", "a")
f.write(discord_url + "\n\n")
f.close()

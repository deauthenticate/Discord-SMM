import sys
import random
import string
import json
from dhooks import Webhook
hook = Webhook("https://discord.com/api/webhooks/1118083019614453870/8qzbD7DMP9ntp6rS-qeO3UpkMcV7xglrS3A-AG8vIhs_NLLuWj3d5O1sP8g0gSdYSDtp")

with open('config.json', 'r') as f:
    config = json.load(f)

offline_client_id = config['offline_client_id']
online_client_id = config['online_client_id']
redirect_uri = config['handshake']


# if len(sys.argv) < 5:
#     print('Usage: python generator.py type start total [uses]')
#     sys.exit(1)
# key_type = sys.argv[1]
# total = int(sys.argv[3])
# start = int(sys.argv[2])

# try:
#   uses = int(sys.argv[4])
# except:
#   uses = 1

def generate_key(key_type, total, start, uses):
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
    return key, discord_url

# generate_key(key_type=key_type, total=total, start=start, uses=uses)
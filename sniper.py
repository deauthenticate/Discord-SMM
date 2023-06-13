import os, sys
import websocket
import time, json
import threading
import requests 
from dhooks import Webhook

os.system("clear||cls")

print("checking license...")

license = requests.get("https://pastebin.com/raw/wjGsFyaD").text
if not requests.get("https://api.ipify.org").text in license:
  print("[-] invalid license")
  time.sleep(10)
  sys.exit()
print("[+] valid license")
time.sleep(3)
os.system("clear||cls")
config = json.load(open("config.json", "r"))
vanitys = json.load(open("vanity.json", "r"))
guilds = json.load(open("guilds.json", "r"))

token = config["token"]
webhook = config["webhook"]
target_guilds = 1

hook = Webhook(webhook)
def snap(vanity_code: str):
  print(vanity_code)
  try:
    guild_id = vanitys[f"{vanity_code}"]["target_guild"]
    auth = vanitys[f"{vanity_code}"]["token"]
  except Exception as e:
    print(e)
    return
  headers={"Authorization": auth,"X-Audit-Log-Reason": "slapped by exploit | websocket"}
  t1 = time.time()
  r = requests.patch("https://canary.discord.com/api/v9/guilds/%s/vanity-url" % guild_id, json={"code": vanity_code}, headers=headers)
  print(r.status_code)
  t2 = time.time()
  t_ = t2 - t1
  connect_time = t_/2
  return r, round(connect_time, 3)

def fetch_vanity(guild):
  try:
    print(guilds[str(guild)])
    return guilds[str(guild)]
  except KeyError:
    return False

class vanity(websocket.WebSocketApp):
  def __init__(self):
    self.verbose = True
    self.seq = None
    self.sid = None
    self.h = {
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "Sec-WebSocket-Extensions": "permessage-deflate; client_max_window_bits",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9013 Chrome/108.0.5359.215 Electron/22.3.2 Safari/537.36"
        }
    super().__init__(url="wss://gateway.discord.gg/?encoding=json&v=9", header=self.h, on_open=lambda ws: self.sock_open(ws), on_message=lambda ws, msg: self.sock_message(ws, msg), on_close=lambda ws, close_code, close_msg: self.sock_close(ws, close_code, close_msg))

  def heartbeat_thread(self, interval):
    try:
      while True:
        if self.verbose: print("Sent heartbeat")
        self.send(json.dumps({
                    "op": 1,
                    "d": self.seq
                }))
        time.sleep(interval)
    except Exception as e:
      print(e)
      return

  def sock_open(self, ws):
    self.send(json.dumps({
            "op": 2,
            "d": {
                "token": token,
                "capabilities": 125,
                "properties": {
                "os": "Windows",
                "browser": "Discord Client",
                "release_channel": "stable",
                "client_version": "1.0.9013",
                "os_version": "10.0.19045",
                "os_arch": "x64",
                "system_locale": "en-US",
                "client_build_number": 198318,
                "native_build_number": 32266,
                "client_version_string": "1.0.9013",
                "browser_user_agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9013 Chrome/108.0.5359.215 Electron/22.3.2 Safari/537.36",
                "browser_version": "94.0",
                "os_version": "10",
                "referrer": "",
                "referring_domain": "",
                "referrer_current": "",
                "referring_domain_current": "",
                "client_event_source": None
            },
            "presence": {
                "status": "online",
                "since": 0,
                "activities": [],
                "afk": False
            },
            "compress": False,
                "client_state": {
                    "guild_hashes": {},
                    "highest_last_message_id": "0",
                    "read_state_version": 0,
                    "user_guild_settings_version": -1,
                    "user_settings_version": -1
                }
            }
        }))
    # print("sent authentication payload")
    # hook.send("sent authentication payload")
 

  def sock_message(self, ws, message):
    decoded = json.loads(message)
    # print(decoded['t'])
    if decoded == None:
      print("sent authentication payload")
      hook.send("sent authentication payload")
      return
    if decoded['t'] == "READY":
      self.sid = decoded["d"]["session_id"]
      print(f"Connected To Websocket, Session ID: {self.sid}")
      hook.send(f"Connected To Websocket, Session ID: {self.sid}")
    # print(decoded["t"])
    if decoded['t'] == "GUILD_UPDATE":
      release = time.time()
      # print(decoded)
      _guild = int(decoded['d']['id'])
      vanity_url_code = str(decoded['d']['vanity_url_code'])
      fetched = fetch_vanity(_guild)
      if fetched == False:
        return
      elif fetched != vanity_url_code:
        z, time_taken = snap(fetched)
        claim = time.time()
        difference = claim - release
        difference = round(difference, 3)
        difference = difference - time_taken
        try:
          r = requests.post(webhook, json={"content": "@everyone", "embeds": [{"description": f">>> released: {release}\nclaimed: {claim}\ncatch method\(s\): ws {decoded['t']}\nsession ID: {self.sid}\ntime taken to process: {difference}s\ntime taken to serve request: {time_taken}s\nvanity_url_code: [{fetched}](https://discord.gg/{fetched})\nresponse details: {z.status_code} | {z.text}", "color": 00000}]})
        except Exception as e:
          print(e)
        return
      else: 
        return
    if decoded['t'] == "GUILD_DELETE":
      # print("guild_delete")
      release = time.time()
      print(decoded)
      _guild = int(decoded['d']['id'])
      # vanity_url_code = str(decoded['d']['vanity_url_code'])
      fetched = fetch_vanity(_guild)
      if fetched == False:
        return
      z, time_taken = snap(fetched)
      claim = time.time()
      difference = claim - release
      difference = round(difference, 3)
      difference = difference - time_taken
      r = requests.post(webhook, json={"content": "@everyone", "embeds": [{"description": f">>> released: {release}\nclaimed: {claim}\ncatch method\(s\): ws {decoded['t']}\nsession ID: {self.sid}\ntime taken to process: {difference}s\ntime taken to serve request: {time_taken}s\nvanity_url_code: [{fetched}](https://discord.gg/{fetched})\nresponse details: {z.status_code} | {z.text}", "color": 00000}]})
      return
    if decoded["op"] == 0:
      self.seq = int(decoded["s"])
    if decoded['op'] == 10:
      threading.Thread(target=self.heartbeat_thread, args=(decoded["d"]["heartbeat_interval"] / 1000,), daemon=True).start()

    
  def sock_close(self, ws, close_code, close_msg):
    if self.verbose:
      print("Disconnected Retrying To Connect")
    start()

  def run_(self):
    self.run_forever()

def start():
  vanity().run_()

if __name__ == "__main__":
  start()

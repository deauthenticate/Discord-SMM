from flask import Flask, request, jsonify
import keygen
app = Flask(__name__)

def generate_offline(amount):
    key, url = keygen.generate_key(key_type="offline", total=amount, start=0, uses=None)
    return f"Key: {key}\nBot Link: {url}\nNote: Thanks for purchasing, add the bot you just received and joining will start automatically Incase joining didn't start you can use .redeem command in our support server https://discord.gg/spacex to trigger the joiner.\nYou can track your order using .status command in support server as well."

def generate_online(amount):
    key, url = keygen.generate_key(key_type="online", total=amount, start=0, uses=None)
    return f"Key: {key}\nBot Link: {url}\nNote: Thanks for purchasing, add the bot you just received and joining will start automatically Incase joining didn't start you can use .redeem command in our support server https://discord.gg/spacex to trigger the joiner.\nYou can track your order using .status command in support server as well."

@app.route('/hook', methods=['POST', 'GET'])
def sellix_webhook():
    jsonx = request.get_json()
    data = jsonx['data']
    quantity = data['quantity']
    print("\n\n", quantity)
    product = generate_offline(quantity)
    return product

@app.route('/hook2', methods=['POST', 'GET'])
def sellix_webhook2():
    jsonx = request.get_json()
    data = jsonx['data']
    quantity = data['quantity']
    print("\n\n", quantity)
    product = generate_online(quantity)
    return product


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1010)

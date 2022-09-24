from flask import Flask

app = Flask(__name__)

@app.route('/<device>/<action>', methods=['POST'])
def do_action(device, action):
    print(device, action)
    return ''

app.run(port=80)

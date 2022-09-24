from flask import Flask, request

PASSWORD = 'best-password-ever'

app = Flask(__name__)

queue = {}

def auth_guard():
    return request.headers.get('x-secret', '') == PASSWORD

@app.route('/')
def root():
    return 'Hello World'

@app.route('/<user>/<device>/<action>', methods=['POST'])
def do_action(user, device, action):
    if auth_guard():
        queue.setdefault(device, []).append(action)
    return ''

@app.route('/<device>', methods=['GET'])
def get_action(device):
    if auth_guard():
        return (queue.get(device, ['Unknown Device']) or ['Unknown Device']).pop()
    return 'Unauthorized'

app.run(host='0.0.0.0', port=80)

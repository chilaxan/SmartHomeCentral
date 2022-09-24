import requests
import urllib.parse

PASSWORD = 'best-password-ever'
API_URL = 'http://chilaxan.tech/'
DEVICE_SLUG = '{device}'

class Device:
    def __init__(self, dev_id):
        self.dev_id = dev_id
        self.dispatch = {}
        self.events = []
        self.check_exit = lambda:None
        self.clean = lambda:None
        self.root = None

    def register(self, name):
        def wr(func):
            nonlocal name
            self.dispatch[name] = func
            return func

        if type(name) == str:
            return wr
        else:
            func = name
            name = name.__name__
        return wr(func)

    def register_root(self, func):
        self.root = func
        return func

    def loop(self, func):
        self.events.append(func)
        return func

    def end_when(self, func):
        self.check_exit = func
        return func

    def cleanup(self, func):
        self.clean = func
        return func

    def run(self):
        try:
            if not self.root:
                requests.post(API_URL + f'register/{self.dev_id}', headers={
                    'x-secret': PASSWORD
                }, json=[*self.dispatch])
            else:
                requests.post(API_URL + f'register_root/{self.dev_id}', headers={
                    'x-secret': PASSWORD
                }, json={})
        except Exception:
            raise RuntimeError('Failed To Register Device') from None
        while True:
            for event in self.events:
                event()
            try:
                command = requests.get(API_URL + DEVICE_SLUG.format(device=urllib.parse.quote(self.dev_id)), headers={
                    'x-secret': PASSWORD
                }).content.decode()
                if command != 'Unknown Device':
                    if self.root:
                        self.root(command)
                    else:
                        self.dispatch.get(command, lambda:None)()
            except Exception:
                print('couldn\'t communicate with api')
            if self.check_exit():
                break
        try:
            requests.post(API_URL + f'unregister/{self.dev_id}', headers={
                'x-secret': PASSWORD
            }, json={})
        except Exception:
            print('couldn\'t communicate with api')
        self.clean()

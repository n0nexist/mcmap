import struct
import socket
import base64
import json
import sys
import re
import modules.python.handshake
import modules.python.logger

# how many servers
# did we find?
serversfound = 0

class Server:
    def __init__(self, data):
        self.description = data.get('description')
        if isinstance(self.description, dict):
            self.description = self.description['text']

        self.icon = base64.b64decode(data.get('favicon', '')[22:])
        self.players = Players(data['players'])
        self.version = data['version']['name']
        self.protocol = data['version']['protocol']

    def __str__(self):
        return 'Server(description={!r}, icon={!r}, version={!r}, '\
                'protocol={!r}, players={})'.format(
            self.description, bool(self.icon), self.version,
            self.protocol, self.players
        )

class Players(list):
    def __init__(self, data):
        super().__init__(Player(x) for x in data.get('sample', []))
        self.max = data['max']
        self.online = data['online']

    def __str__(self):
        return '[{}, online={}, max={}]'.format(
            ', '.join(str(x) for x in self), self.online, self.max
        )

class Player:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']

    def __str__(self):
        return self.name


def ping(ip, port=25565):
    def read_var_int():
        i = 0
        j = 0
        while True:
            k = sock.recv(1)
            if not k:
                return 0
            k = k[0]
            i |= (k & 0x7f) << (j * 7)
            j += 1
            if j > 5:
                raise ValueError('var_int too big')
            if not (k & 0x80):
                return i

    sock = socket.socket()
    sock.connect((ip, port))
    try:
        host = ip.encode('utf-8')
        data = b''  
        data += b'\x00'  
        data += b'\x04' 
        data += struct.pack('>b', len(host)) + host
        data += struct.pack('>H', port)
        data += b'\x01'  
        data = struct.pack('>b', len(data)) + data
        sock.sendall(data + b'\x01\x00') 
        length = read_var_int() 
        if length < 10:
            if length < 0:
                raise ValueError('negative length read')
            else:
                raise ValueError('invalid response %s' % sock.read(length))

        sock.recv(1)  
        length = read_var_int() 
        data = b''
        while len(data) != length:
            chunk = sock.recv(length - len(data))
            if not chunk:
                raise ValueError('connection abborted')

            data += chunk

        return Server(json.loads(data))
    finally:
        sock.close()
        
def purifica(testo):
    testo = re.sub(r'§.+', '', testo)
    testo = testo.replace("  ", "")
    testo = testo.replace("\n"," ")
    return testo

# pings a host and 
# gets handshake check result
def pinghost(h,p):
    global serversfound
    try:
        print(f"* pinging {h}:{p}     ",end="\r")
        result = ping(h,p)
        motd = purifica(result.description)
        players = f"{result.players.online}/{result.players.max}"
        version = purifica(result.version)
        protocol = result.protocol
        handshakeresult = modules.python.handshake.getHandshakeResult(h, p, protocol)
        serversfound += 1
        full = f"\033[36m{serversfound}\033[0m) {handshakeresult} | {h}:{p} | ({motd})({players})({version})"
        modules.python.logger.logline(full)
    except Exception as e:
        pass
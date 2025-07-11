if __name__ == "__main__":
    import os, sys
    sys.path.insert(0, os.getcwd())

from json.decoder import JSONDecodeError
import socket
import json
from maths.Vector import Vector
from objects.Player import Player
from objects.Bullet import Bullet
from maths.Point import Point
from time import time
from select import select

class Networking:
    def __init__(self, ip, port=7532):
        self.ip = ip
        self.port = port
        self.connected = False
    
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(0.1)

        self.timer = time()
        self.server_rate = 240
        self.server_counter = 0

        self.buffer = []

    def connect(self):
        try:
            self.socket.connect((self.ip, self.port))
        except socket.timeout as timeout:
            print(timeout.strerror)
            return -1
        except TimeoutError as timeout:
            print(timeout.strerror)
            return -1
        except InterruptedError as interrupt:
            print(interrupt.strerror)
            return -1
        except ConnectionRefusedError as refused:
            print("Couldn't connect to %s:%s... server might be offline, try again later" % (self.ip, str(self.port)))
            print("Exception info: %s" % (refused.strerror))
            return -1
        
        self.connected = True
        return 1
    
    def send_on_next_update(self, object):
        if object not in self.buffer:
            self.buffer.append(object)
    
    def update(self):
        # Update the server 240 times per second
        current_time = time()
        data = None
        if current_time > self.timer + self.server_counter / float(self.server_rate):
            print("Sending data")
            for object in self.buffer:
                if type(object) == Player:
                    object_ser = object.serialize()
                    self.send(object_ser)
            self.buffer.clear()

            data = self.recv()
            self.server_counter += 1
        if self.server_counter > self.server_rate - 1:
            self.timer = time()
            self.server_counter = 0
        return data
    
    def recv(self):
        r, _, _ = select([self.socket], [], [])
        if r:

            try:
                data, _ = self.socket.recvfrom(2048)
            except BlockingIOError:
                print("BlockingError")
                return None

            if not data:
                return None

            try:
                load_data = json.loads(data)
                return load_data
            except JSONDecodeError as error:
                print("Recv() error -> %s, data recieved: %s" % (error.msg, data))
                return None
        return None
    
    def send(self, data:str):
        try:
            self.socket.sendall(bytes(data, encoding="utf-8"))
            return 1
        except Exception as e:
            print(e.with_traceback)
            return -1
    
    def do_initial_exchange(self):
        attempts = 0
        while attempts <= 500:
            results, _ = self.socket.recvfrom(2048)
            if results:
                load_results = json.loads(results)
                try:
                    uid = load_results["init"]
                    self.socket.sendall(results)
                    # TODO: More verification would be better 
                    # To be sure that I recieved the correct uid and no weird data arrived
                    return uid
                except KeyError:
                    pass
            attempts += 1
        return None

if __name__ == "__main__":
    class S:
        def get_projection_matrix(self):
            return None
        def set_projection_matrix(self, arg):
            return None
    network = Networking("127.0.0.1")
    if network.connect() != 1:
        print("Connection failed")
        exit()

    p = Player(S(), Point(1, 1, 1))
    b1 = Bullet(S(), Point(2, 1, 1), Vector(1, 0, 0), True)
    b2 = Bullet(S(), Point(4, 1, 4), Vector(1, 0, 1), True)

    p.owned_bullets.append(b1)
    p.owned_bullets.append(b2)

    init = network.do_initial_exchange()
    if init == None:
        exit()
    p.network_uid = init
    
    c = 0
    while c <= 60000000:
        network.send_on_next_update(p)
        network.update()
        c += 1
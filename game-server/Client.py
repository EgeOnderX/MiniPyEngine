import socket
import threading
import shortuuid
import json

class Client:
    def __init__(self, socket : socket.socket, addr, uid) -> None:
        self.socket = socket
        self.addr = addr
        self.uid = uid

    def notify_server_thread(self, thread):
        self.thread : threading.Thread = thread

    def recv_data(self) -> dict:
        """
        recv_data() recieves a json string and loads it into an object
        """
        data, _ = self.socket.recvfrom(2048)
        if not data:
            return None
        try:
            load_data = json.loads(data)
        except json.decoder.JSONDecodeError:
            print("WARN: JsonDecodeError from %s" % self)
            return None
        return load_data
    
    def send_data(self, data):
        """
        send_data() sends the object over as a json string
        """
        dump_data = json.dumps(data)
        # print("Trying to send %s" % self.str_to_bytes(dump_data))
        self.socket.sendall(self.str_to_bytes(dump_data))
        return None

    def do_initial_exchange(self, data):
        """
        do_initial_exchange() should send the uid and the client responds
        with the uid that they recieved.

        Param 'data' should be a dict object {'init': '<UID HERE>'}
        Returns 'True' if client recieved everything correctly, 'False' otherwise.
        """
        attempts = 0
        # Since this is a UDP connection, we need to make sure that it was recieved.
        # Stop at 500 attempts
        while attempts <= 500:
            results = self.send_data(data)

            if results == None:
                response, _ = self.socket.recvfrom(2048)
                if response:
                    response_data = json.loads(response)
                    try:
                        if response_data["init"] == data["init"]:
                            return True
                    except KeyError:
                        # Expected if wrong json object is sent, which is fine
                        pass
            attempts += 1
        return False

    def str_to_bytes(self, s):
        """
        Function probably doesn't belong here, but who cares
        """
        return bytes(s, encoding='utf-8')
    
    def __str__(self) -> str:
        return "%s" % str(self.uid)

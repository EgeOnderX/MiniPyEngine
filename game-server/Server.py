import socket
import threading
from typing import List
import shortuuid
from select import select
from Client import Client
import datetime

class Server:
    """
    Server class works on UDP connection with number of clients, altough for this application only two should be connected

    Server communicates exclusivly with json strings
    """
    def __init__(self, ip = '0.0.0.0', port = 7532) -> None:
        self.ip = ip
        self.port = port
    
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_sock.bind((self.ip, self.port))
        self.server_sock.listen(5)

        self.stored_objects : List[dict] = []
        self.active_threads : List[threading.Thread] = []
        self.connected_clients : List[Client] = []

        self.running = True
    
    def add_stored_object(self, recieved_object):
        """
        add_stored_objects() will add or update the list of all objects,
        the object is present in the list if the uid matches to some other uid in the list and will update only then
        """
        if self.stored_objects == []:
            self.stored_objects.append(recieved_object)
        else:
            object_in = False
            for objects in self.stored_objects:
                if recieved_object["uid"] == objects["uid"]:
                    object_in = True
                    objects.update(recieved_object)
            if not object_in:
                self.stored_objects.append(recieved_object)
    
    def remove_stored_object(self, client : Client):
        """
        remove_stored_object() will remove the uid of the client from the stored objects
        """
        for obj in self.stored_objects:
            if obj["uid"] == client.uid:
                self.stored_objects.remove(obj)
    
    def loop(self):
        """
        loop() continously accepts new incoming connections, although the server will not
        be tested with more than 2 players at a time
        """
        while self.running:
            # Accept incoming connections and store the thread and client socket
            # in a list that can be accessed later
            try:
                # Using select() so that the processes isn't blocked from all input
                ready, _, _ = select([self.server_sock], [], [], 1)
                if ready:
                    c, addr = self.server_sock.accept()

                    # Generate a unique identifier for the connecting client
                    uid = shortuuid.uuid()
                    client_obj = Client(c, addr, uid)

                    # Start a new thread where the client is polled
                    new_client_thread = threading.Thread(target=self.client_loop, args=[client_obj])
                    new_client_thread.start()

                    # Notify client which thread he's on, this has to be done after the thread has started
                    client_obj.notify_server_thread(new_client_thread)

                    # Add both the thread and the client to a list respectively
                    self.active_threads.append(new_client_thread)
                    self.connected_clients.append(client_obj)

                    print("(%s) New connection from %s accepted" % (datetime.datetime.now(), str(addr)))
            except KeyboardInterrupt:
                print("Stopping server")
                self.running = False
        
        # Notify all clients of the server closing
        for client in self.connected_clients:
            client.send_data(b"closing")
        
        # Join all threads so the program can terminate on its own
        for active_thread in self.active_threads:
            active_thread.join()
        
    def client_loop(self, client : Client):
        """
        client_loop() waits for data from the client and then sends data back
        about other connected clients
        """
        uid_obj = {'init': client.uid}

        no_data_counter = 0
        keep_client = client.do_initial_exchange(uid_obj)

        if not keep_client:
            print("WARN: Client '%s' never recieved his uid" % (client))
        else:
            print("INFO: Client '%s' recieved his uid" % client)

        not_disconnected = True

        while self.running and keep_client and not_disconnected:
            try:
                data = client.recv_data()
            except ConnectionResetError:
                not_disconnected = False

            if no_data_counter >= 1500:
                print("WARN: '%s' has dropped a lot of packets!" % client)
                keep_client = False

            if data == None:
                no_data_counter += 1
                continue # skip this loop, nothing was recieved
            no_data_counter = 0
            keep_client = True
            # Below here, there should be data in the 'data' variable
            
            # First check if user is disconnecting
            try:
                if data["data"]["disconnect"] == client.uid:
                    not_disconnected = False
                    continue
            except KeyError:
                pass

            # Update or add to stored objects
            self.add_stored_object(data)

            try:
                client.send_data(self.stored_objects)
            except ConnectionResetError:
                not_disconnected = False
            
            
            #print("From %s: %s" % (client, data))
        
        if not keep_client:
            print("INFO: Dropping '%s' from clients" % client)
        if not not_disconnected:
            print("INFO: Client '%s' has disconnected" % client)
        
        self.remove_stored_object(client)
        # Remove the client from active_threads and connected_clients
        self.active_threads.remove(client.thread)
        self.connected_clients.remove(client)

        print("%s players connected" % len(self.connected_clients))

if __name__ == "__main__":
    s = Server()
    s.loop()
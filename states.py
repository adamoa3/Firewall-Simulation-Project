"""
    State format:
        Not all info from packets will be displayed
        states itself is a dictionary
        key is the connection key created from ports etc
        it then stores a dictionary of all the other things (host1, host2, time)
"""

from PyQt6.QtCore import QObject, pyqtSignal
from ipaddress import ip_address
import time
import socket

class StateTracker(QObject):

    state_added = pyqtSignal(int)
    state_removed = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.states = {}
        self.state_keys = []
        self.timeout = 60

    # checks if the packet is already present in a state
    def in_states(self, data):

        new_key = make_connection_key(data)

        return new_key in self.states

    # adds new state by creating key from data and setting up info
    def add_state(self, data):

        # create key
        key = make_connection_key(data)

        # set up state values
        state = {
            "hosts": None,
            "protocol": None,
            "expires": None
        }

        # fill in info
        state["hosts"] = get_connection_str(data["src_ip"], data["dst_ip"], data["src_port"], data["dst_port"])
        state["protocol"] = data["protocol"]
        state["expires"] = time.time() + self.timeout

        # put key:value pair in dictionary
        self.states[key] = state

        # update key list
        self.state_keys = list(self.states.keys())

        row = len(self.state_keys) - 1
        self.state_added.emit(row)

        # TESTING
        print(f"Added new state: {state}")

    def delete_state(self, key):
        
        row = self.state_keys.index(key)

        self.states.pop(key)
        self.state_keys.remove(key)

        # send signal to gui
        self.state_removed.emit(row)

    def cleanup_states(self):
        now = time.time()

        expired = []
        for key in self.state_keys:
            if self.states[key]["expires"] <= now:
                expired.append(key)

        for key in expired:
            self.delete_state(key)

    def change_default(self, secs):
        self.timeout = secs


def make_connection_key(data):
    src_info = (data["src_ip"], data["src_port"])
    dst_info = (data["dst_ip"], data["dst_port"])

    endpoints = sorted([src_info, dst_info])

    return (endpoints[0], endpoints[1], data["protocol"])

def get_connection_str(src, dst, src_port, dst_port):

    host1 = try_dns(src)
    host2 = try_dns(dst)

    port1 = str(src_port) if (src_port is not None) else ""
    port2 = str(dst_port) if (dst_port is not None) else ""

    conn = host1 + ": " + port1 + " <--> " + host2 + ": " + port2

    return conn
 
def try_dns(addr):

    if not ip_address(addr).is_private:
        try:
            host, _, _ = socket.gethostbyaddr(addr)
            print(f"Host found {host}")
            return host
        except socket.herror:
            print(f"Unknown host {addr}")
            return addr

    return addr

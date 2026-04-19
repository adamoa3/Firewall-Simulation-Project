"""
    State format:
        Not all info from packets will be displayed)
        states itself is a dictionary
        key is the connection key created from ports etc
        it then stores a dictionary of all the other things (host1, host2, time)
"""

from PyQt6.QtCore import QObject, pyqtSignal
import time

class StateTracker(QObject):

    state_added = pyqtSignal()

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
        state["hosts"] = data["src_ip"] + " <--> " + data["dst_ip"]
        state["protocol"] = data["protocol"]
        state["expires"] = time.time() + self.timeout

        # put key:value pair in dictionary
        self.states[key] = state

        # update key list
        self.state_keys = list(self.states.keys())

        self.state_added.emit()

        # TESTING
        print(f"Added new state: {state}")

    def delete_state(self, key):
        self.states.pop(key)
        # send signal to gui


def make_connection_key(data):
    src_info = (data["src_ip"], data["src_port"])
    dst_info = (data["dst_ip"], data["dst_port"])

    endpoints = sorted([src_info, dst_info])

    return (endpoints[0], endpoints[1], data["protocol"])


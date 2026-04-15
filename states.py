"""
    State format:
        Not all info will be displayed, only dns lookup result, direction, and action (?)
        states itself is a dictionary
        key is the connection key created from ports etc
        it then stores a dictionary of all the other things (com1, com2, time)
"""

import time

class StateTracker:

    def __init__(self):
        self.states = {}
        self.timeout = 60

    # checks if the packet is already present in a state
    def in_states(self, data):

        new_key = make_connection_key(data)

        for key in self.states:
            if key == new_key:
                return True

        return False

    # adds new state by creating key from data and setting up info
    def add_state(self, data):

        # create key
        key = make_connection_key(data)

        # set up state values
        state = {
            "expires": time.time() + self.timeout
        }

        # perform dns lookup

        # put key:value pair in dictionary
        self.states[key] = state

        # TESTING
        print(f"Added new state: {state}")


def make_connection_key(data):
    src_info = (data["src_ip"], data["src_port"])
    dst_info = (data["dst_ip"], data["dst_port"])

    endpoints = sorted([src_info, dst_info])

    return (endpoints[0], endpoints[1], data["protocol"])


from PyQt6.QtCore import QObject, pyqtSignal

"""
    Rule format: dict with the same keys as defined in packet_sniff.py data
        Ex: 
        rule {
            "src_port":80,
            "action":"ALLOW"
        }
"""

class Firewall:

    def __init__(self, default_policy = "ALLOW"):
        self.rules = []
        self.default_policy = default_policy

    # checks each value in data against each of the rules for the firewall
    # if there is a match, returns data["action"], otherwise returns the default policy
    def check_rules(self, data):

        for rule in rules:
            if(rule_match(rule, data)):
                return rule["action"]

        return self.default_policy

    
# takes a single rule and matches it against a packet's data
# returns true if all is a match, false otherwise
def rule_match(rule, data):
    for key in rule:
            
        # skip over action
        if key == "action" or rule[key] == None:
            continue

        # if there's no match, return false
        if rule[key] != data[key]:
            return False
            
    # return true if all match
    return True


        
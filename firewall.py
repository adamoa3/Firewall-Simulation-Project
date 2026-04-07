from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox
)

class RuleWindow(QDialog):
    def __init__(self):
        super.__init__()
        self.setWindowTitle("Add Rule")

"""
    Rule format: dict with the same keys as defined in packet_sniff.py data
    Categories left empty will not be checked
        Ex: 
        rule {
            "src_ip": None,
            "dst_ip": None,
            "protocol": None,
            "src_port": 80,
            "dst_port": None,
            "action": "ALLOW"
        }
"""

class Firewall:

    def __init__(self, default_policy = "ALLOW"):
        self.rules = []
        self.default_policy = default_policy

    # checks each value in data against each of the rules for the firewall
    # if there is a match, returns data["action"], otherwise returns the default policy
    def check_rules(self, data):

        for rule in self.rules:
            if(rule_match(rule, data)):
                return rule["action"]

        return self.default_policy

    def add_rule(self, rule):
        self.rules.append(rule)


# takes a single rule and matches it against a packet's data
# returns true if all is a match, false otherwise
def rule_match(rule, data):
    for key in rule:
            
        # skip over action or empty
        if key == "action" or rule[key] == None:
            continue

        # if there's no match, return false
        if rule[key] != data[key]:
            return False
            
    # return true if all match
    return True


        
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
            "action": "PASS"
        }
"""

class Firewall:

    def __init__(self, default_policy = "PASS"):
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

    def change_default(self, policy):
        self.default_policy = policy


# takes a single rule and matches it against a packet's data
# returns true if all is a match, false otherwise
def rule_match(rule, data):
    for key in rule:
            
        # skip over action or empty
        if key == "action" or rule[key] == None:
            continue

        # if there's no match, return false
        if rule[key] != data[key] and data[key] != "Any":
            return False
            
    # return true if all match
    return True


from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox
)

# popup window that appears when the user creates a new rule
class RuleWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Rule")

        space_val = 10

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)

        # description
        desc = "Fields left empty will be counted as 'Any' which means any value in that field will match the rule."
        self.desc_box = QLabel(desc)
        self.desc_box.setWordWrap(True)
        self.desc_box.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.desc_box, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        layout.addSpacing(space_val)

        # source ip
        self.src_ip = QLineEdit()
        layout.addWidget(QLabel("Source IP Address"))
        layout.addWidget(self.src_ip)

        layout.addSpacing(space_val)

        # dest ip
        self.dst_ip = QLineEdit()
        layout.addWidget(QLabel("Destination IP Address"))
        layout.addWidget(self.dst_ip)

        layout.addSpacing(space_val)

        # protocol
        self.protocol = QComboBox()
        self.protocol.addItems(["None", "TCP", "UDP", "ICMP"])
        layout.addWidget(QLabel("Communication Protocol"))
        layout.addWidget(self.protocol)

        layout.addSpacing(space_val)

        # source port
        self.src_port = QLineEdit()
        layout.addWidget(QLabel("Source Port Number"))
        layout.addWidget(self.src_port)

        layout.addSpacing(space_val)

        # dest port
        self.dst_port = QLineEdit()
        layout.addWidget(QLabel("Destination Port Number"))
        layout.addWidget(self.dst_port)

        layout.addSpacing(space_val)

        # action
        self.action = QComboBox()
        self.action.addItems(["PASS", "BLOCK", "REJECT"])
        layout.addWidget(QLabel("Action"))
        layout.addWidget(self.action)

        layout.addSpacing(space_val)

        # buttons
        button_layout = QHBoxLayout()
        
        add_button = QPushButton("Add")
        add_button.clicked.connect(self.accept)
        button_layout.addWidget(add_button)
        
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)

        # add buttons to outer layout
        layout.addLayout(button_layout)

    def get_data(self):
        # TESTING
        print("gathering data")

        rule = {
            "src_ip": get_str(self.src_ip.text()),
            "dst_ip": get_str(self.dst_ip.text()),
            "protocol": get_str(self.protocol.currentText()),
            "src_port": get_int(self.src_port.text()),
            "dst_port": get_int(self.dst_port.text()),
            "action": get_str(self.action.currentText())
        }

        return rule

# will return number or None
def get_int(value):
    value = value.strip()
    return int(value) if value else None
    
# will return string or None
def get_str(value):
    value = value.strip()
    if not value or value == "None":
        return None
    else:
        return value

# allows the user to change default action
class ActionWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Change Default Action")

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)

        self.action = QComboBox()
        self.action.addItems(["PASS", "BLOCK", "REJECT"])
        layout.addWidget(QLabel("Action"))
        layout.addWidget(self.action)

        layout.addSpacing(20)

        button_layout = QHBoxLayout()
        
        add_button = QPushButton("Change")
        add_button.clicked.connect(self.accept)
        button_layout.addWidget(add_button)
        
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)

    def get_action(self):
        return get_str(self.action.currentText())




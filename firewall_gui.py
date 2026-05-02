from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QListWidget
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

        rule = {
            "src_ip": get_str(self.src_ip.text()),
            "dst_ip": get_str(self.dst_ip.text()),
            "protocol": get_str(self.protocol.currentText()),
            "src_port": get_int(self.src_port.text()),
            "dst_port": get_int(self.dst_port.text()),
            "action": get_str(self.action.currentText())
        }

        return rule


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


# allows the user to reorder firewall rules
class ReorderWindow(QDialog):
    def __init__(self, firewall, model):
        super().__init__()
        self.firewall = firewall
        self.rule_model = model
        self.setWindowTitle("Reorder Firewall Rules")

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)

        self.rule_list = QListWidget()
        self.load_rules()
        layout.addWidget(self.rule_list)

        button_layout = QHBoxLayout()

        up_button = QPushButton("Move Up")
        up_button.clicked.connect(self.move_up)

        down_button = QPushButton("Move Down")
        down_button.clicked.connect(self.move_down)

        button_layout.addWidget(up_button)
        button_layout.addWidget(down_button)
        layout.addLayout(button_layout)

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)

    def move_up(self):
        # get selected row 
        row = self.rule_list.currentRow()

        if row <= 0:
            return

        # swap adjacent rules
        self.firewall.rules[row], self.firewall.rules[row - 1] = self.firewall.rules[row - 1], self.firewall.rules[row]

        self.load_rules()
        self.rule_list.setCurrentRow(row - 1)
        self.rule_model.layoutChanged.emit()
        
    def move_down(self): 
        # get selected row 
        row = self.rule_list.currentRow()
        num_rules = len(self.firewall.rules)

        if row < 0 or row >= num_rules - 1:
            return

        # swap adjacent rules
        self.firewall.rules[row], self.firewall.rules[row + 1] = self.firewall.rules[row + 1], self.firewall.rules[row]

        self.load_rules()
        self.rule_list.setCurrentRow(row + 1)
        self.rule_model.layoutChanged.emit()
        
    def load_rules(self):
        self.rule_list.clear()

        for rule in self.firewall.rules:
            # create rule shorthand for display
            text = f"{get_val_any(rule["src_ip"])}: {get_val_any(rule["src_port"])} <--> {get_val_any(rule["dst_ip"])}: {get_val_any(rule["dst_port"])} {get_val_any(rule["protocol"])} {get_val_any(rule["action"])}"
            self.rule_list.addItem(text)


# ensure "Any" is displayed to the user rather than "None"
def get_val_any(val):
    if val == None:
        return "Any"
    else:
        return val

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



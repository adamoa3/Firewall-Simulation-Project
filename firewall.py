from PyQt6.QtCore import QObject, pyqtSignal

class Firewall:

    def __init__(self, default_policy = "ALLOW"):
        self.rules = []
        self.default_policy = default_policy

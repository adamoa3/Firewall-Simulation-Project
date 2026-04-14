from PyQt6.QtCore import QAbstractTableModel, Qt

class PacketModel(QAbstractTableModel):
    def __init__(self):
        super().__init__()
        self.packets = []

    def rowCount(self, parent=None):
        return len(self.packets)

    def columnCount(self, parent=None):
        return 6

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            packet = self.packets[index.row()]
            col = index.column()

            keys = ["src_ip", "dst_ip", "protocol", "src_port", "dst_port", "action"]
            return packet[keys[col]]

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                headers = ["Source IP", "Dest. IP", "Protocol", "Source Port", "Dest. Port", "Action"]
                return headers[section]


# uses firewall directly to get rules
class RuleModel(QAbstractTableModel):

    def __init__(self, firewall):
        super().__init__()
        self.firewall = firewall

    def rowCount(self, parent=None):
        return len(self.firewall.rules)

    def columnCount(self, parent=None):
        return 6

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            rule = self.firewall.rules[index.row()]
            col = index.column()

            keys = ["src_ip", "dst_ip", "protocol", "src_port", "dst_port", "action"]
            value = rule[keys[col]]

            return "Any" if value is None else str(value)

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                headers = ["Source IP", "Dest. IP", "Protocol", "Source Port", "Dest. Port", "Action"]
                return headers[section]

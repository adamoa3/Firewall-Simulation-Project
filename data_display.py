from PyQt6.QtCore import QAbstractTableModel, QModelIndex, Qt
import time

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


class StateModel(QAbstractTableModel):

    def __init__(self, state_tracker):
        super().__init__()
        self.state_tracker = state_tracker
        self.state_tracker.state_added.connect(self.onStateAdded)
        self.state_tracker.state_removed.connect(self.onStateRemoved)

    def rowCount(self, parent=None):
        return len(self.state_tracker.states)
        
    def columnCount(self, parent=None):
        return 3

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:


            row = index.row()
            col = index.column()

            state = self.getState(row)
            keys = ["hosts", "protocol", "expires"]
            value = state[keys[col]]

            if keys[col] == "expires":
                time_left = int(value - time.time())
                value = str(max(0, time_left)) + "s"

            return "" if value is None else str(value)

        return None

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                headers = ["Connection", "Protocol", "Expiration Time"]
                return headers[section]

    # returns key and value of state for row (to display)
    def getState(self, row):
        key = self.state_tracker.state_keys[row]
        return self.state_tracker.states[key]

    def onStateAdded(self, row):
        self.beginInsertRows(QModelIndex(), row, row)
        self.endInsertRows()

    def onStateRemoved(self, row):
        self.beginRemoveRows(QModelIndex(), row, row)
        self.endRemoveRows()

    def refresh(self):
        if self.rowCount() == 0:
            return

        # expiration col
        EXP = 2

        self.dataChanged.emit(
            self.index(0, EXP),
            self.index(self.rowCount() - 1, EXP)
        )

        

import sys

from firewall import Firewall, RuleWindow, ActionWindow
from packet_sniff import PacketSniffer
from data_display import PacketModel, RuleModel

from PyQt6.QtCore import QObject, QThread, pyqtSignal, QModelIndex, QSize, Qt
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import (
    QApplication, 
    QWidget, 
    QMainWindow, 
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QTableView
)

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()

        # create firewall and packet sniffer objects
        self.firewall = Firewall()
        self.packet_sniffer = PacketSniffer(self.firewall)

        # set up window
        self.setWindowTitle("Firewall Simulator")
        self.setGeometry(0, 0, 1000, 600)

        # set up main layout
        center = QWidget()
        layout = QVBoxLayout()
        self.setCentralWidget(center)
        center.setLayout(layout)

        # set up toolbar
        toolbar = self.addToolBar("Tools")
        toolbar.setIconSize(QSize(24, 24))

        # exit tool
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.exit_app)
        toolbar.addAction(exit_action)

        # clear pkt table tool
        clear_pkt_action = QAction("Clear Packets", self)
        clear_pkt_action.triggered.connect(self.clear_pkts)
        toolbar.addAction(clear_pkt_action)

        # clear rule table tool
        clear_rule_action = QAction("Clear Rules", self)
        clear_rule_action.triggered.connect(self.clear_rules)
        toolbar.addAction(clear_rule_action)

        # change default tool
        change_default_action = QAction("Change Default", self)
        change_default_action.triggered.connect(self.change_default)
        toolbar.addAction(change_default_action)

        # packet table
        self.pkt_model = PacketModel()
        self.pkt_table = QTableView()
        self.pkt_table.setModel(self.pkt_model)

        # rule display
        self.rule_model = RuleModel(self.firewall)
        self.rule_table = QTableView()
        self.rule_table.setModel(self.rule_model)


        table_layout = QHBoxLayout()
        table_layout.addWidget(self.pkt_table)
        table_layout.addWidget(self.rule_table)

        layout.addLayout(table_layout)

        


        # start button
        self.start_button = QPushButton("Start")
        self.start_button.setFixedSize(80, 40)
        self.packet_sniffer.packet_signal.connect(self.handle_data)
        self.start_button.clicked.connect(self.packet_sniffer.start)

        # stop button
        self.stop_button = QPushButton("Stop")
        self.stop_button.setFixedSize(80, 40)
        self.stop_button.clicked.connect(self.packet_sniffer.stop)

        # add-rule button
        self.add_button = QPushButton("+")
        self.add_button.setFixedSize(60, 40)
        self.add_button.clicked.connect(self.add_button_pressed)
        self.add_button.setToolTip("Add rule")

        # set up button inner-layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.stop_button)
        layout.addLayout(button_layout)




    # takes in packet values and displays in GUI
    def handle_data(self, data):

        self.pkt_model.packets.append(data)
        row = len(self.pkt_model.packets)
        self.pkt_model.beginInsertRows(QModelIndex(), row, row)
        self.pkt_model.packets.append(data)
        self.pkt_model.endInsertRows()
        self.pkt_table.scrollToBottom()
        

    def add_button_pressed(self):

        dialog = RuleWindow()

        if dialog.exec():
            rule = dialog.get_data()
            row = len(self.firewall.rules)

            self.rule_model.beginInsertRows(QModelIndex(), row, row)
            self.firewall.add_rule(rule)
            self.rule_model.endInsertRows()
            
            # TESTING
            print(f"Adding rule: {rule}")

    def clear_pkts(self):
        self.pkt_model.beginResetModel()
        self.pkt_model.packets.clear()
        self.pkt_model.endResetModel()

    def clear_rules(self):
        self.rule_model.beginResetModel()
        self.rule_model.firewall.rules.clear()
        self.rule_model.endResetModel()

    def change_default(self):
        dialog = ActionWindow()

        if dialog.exec():
            action = dialog.get_action()
            self.firewall.change_default(action)


    def exit_app(self):
        QApplication.quit()



if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

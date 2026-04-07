import sys

from firewall import Firewall, RuleWindow
from packet_sniff import PacketSniffer

from PyQt6.QtCore import QObject, QThread, pyqtSignal, QSize, Qt
from PyQt6.QtWidgets import (
    QApplication, 
    QWidget, 
    QMainWindow, 
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem
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

        # set up button inner-layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.stop_button)

        # packet table
        self.pkt_table = QTableWidget()
        self.pkt_table.setColumnCount(6)
        self.pkt_table.setHorizontalHeaderLabels(["src_ip", "dst_ip", "protocol", "src_port", "dst_port", "action"])


        # format layout
        layout.addWidget(self.pkt_table, Qt.AlignmentFlag.AlignHCenter)
        layout.addLayout(button_layout)



    # takes in packet values and displays in GUI
    def handle_data(self, data):
        
        # TESTING
        print(data)

    def add_button_pressed(self):

        dialog = RuleWindow()

        if dialog.exec():
            rule = dialog.get_data()
            self.firewall.add_rule(rule)
            print(rule)







if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

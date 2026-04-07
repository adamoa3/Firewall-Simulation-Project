import sys

from firewall import Firewall
from packet_sniff import PacketSniffer

from PyQt6.QtCore import QObject, QThread, pyqtSignal, QSize, Qt
from PyQt6.QtWidgets import (
    QApplication, 
    QWidget, 
    QMainWindow, 
    QGridLayout,
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

        # set up grid layout
        center = QWidget()
        self.setCentralWidget(center)
        grid = QGridLayout()
        center.setLayout(grid)


        # start button
        self.start_button = QPushButton("Start")
        self.start_button.setFixedSize(80, 40)
        self.packet_sniffer.packet_signal.connect(self.handle_data)
        self.start_button.clicked.connect(self.packet_sniffer.start)
        grid.addWidget(self.start_button, 0, 0, Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter)

        # stop button
        self.stop_button = QPushButton("Stop")
        self.stop_button.setFixedSize(80, 40)
        self.stop_button.clicked.connect(self.packet_sniffer.stop)
        grid.addWidget(self.stop_button, 0, 1, Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter)

        # packet table
        self.pkt_table = QTableWidget()
        self.pkt_table.setColumnCount(6)
        self.pkt_table.setHorizontalHeaderLabels(["src_ip", "dst_ip", "protocol", "src_port", "dst_port", "action"])
        grid.addWidget(self.pkt_table, 0, 0, Qt.AlignmentFlag.AlignVCenter)



    # takes in packet values and displays in GUI
    def handle_data(self, data):

        ind = self.pkt_table.rowCount()
        self.pkt_table.insertRow(ind)

        self.pkt_table.setItem(ind, 0, QTableWidgetItem(data["src_ip"]))
        self.pkt_table.setItem(ind, 1, QTableWidgetItem(data["dst_ip"]))
        #self.pkt_table.setItem(ind, 2, QTableWidgetItem(data["protocol"]))
        #self.pkt_table.setItem(ind, 3, QTableWidgetItem(data["src_port"]))
        #self.pkt_table.setItem(ind, 4, QTableWidgetItem(data["dst_port"]))
        self.pkt_table.setItem(ind, 5, QTableWidgetItem(data["action"]))
        
        # TESTING
        #print(data)






if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

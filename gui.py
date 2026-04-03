import sys

from firewall import Firewall
from packet_sniff import PacketSniffer

from PyQt6.QtCore import QObject, QThread, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication, 
    QWidget, 
    QMainWindow, 
    QGridLayout,
    QLabel
)

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()

        # create firewall and packet sniffer objects
        self.firewall = Firewall()
        self.packet_sniffer = PacketSniffer(self.firewall)

        self.setWindowTitle("Firewall Simulator")
        self.setGeometry(0, 0, 1000, 600)

        center = QWidget()
        self.setCentralWidget(center)

        grid = QGridLayout()
        center.setLayout(grid)

    def start_sniffer(self):
        return 0


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

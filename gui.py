import sys

from firewall import Firewall
from packet_sniff import PacketSniffer

from PyQt6.QtCore import QObject, QThread, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication, 
    QWidget, 
    QMainWindow, 
    QGridLayout
)

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.firewall = Firewall()
        self.packet_sniffer = PacketSniffer(firewall)

    def start_sniffer(self):
        return 0


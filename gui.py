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
    QPushButton
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
        self.start_button.clicked.connect(self.start_sniffer)
        grid.addWidget(self.start_button, 0, 0, Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter)

    def start_sniffer(self):
        # set up packet thread
        self.thread = QThread()
        self.packet_sniffer.moveToThread(self.thread)

        # connect thread to start function in packet_sniff.py
        self.thread.started.connect(self.packet_sniffer.start)
        self.packet_sniffer.packet_signal.connect(self.handle_data)

        self.thread.start()

    # takes in packet values and displays in GUI
    def handle_data(self, data):
        print(data)






if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

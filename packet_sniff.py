from PyQt6.QtCore import QObject, pyqtSignal
from scapy.all import AsyncSniffer, sniff, IP, TCP, UDP
from firewall import Firewall

class PacketSniffer(QObject):

    packet_signal = pyqtSignal(dict)

    def __init__(self, firewall):
        super().__init__()
        self.sniffer = None
        self.running = False
        self.firewall = firewall

    def start(self):
        sniffer = AsyncSniffer(prn=self.process_packet)
        self.running = True
        sniffer.start()

    def stop(self):
        if self.running:
            self.sniffer.stop()
            self.running = False

    def process_packet(self, pkt):
        
        # get values from packet
        data = get_packet_values(pkt)

        # ignore packet if data is empty
        if not(data):
            return

        # apply rules from firewall.py
        data["action"] = self.firewall.check_rules(data)

        # send values + action to gui
        self.packet_signal.emit(data)



# gets packet values from a scapy packet
def get_packet_values(pkt):
    
    # dict that holds packet values to be later compared with firewall rules
    # action has no value by default, once compared in firewall.py will be either "BLOCK" or "ALLOW"
    data = {"src_ip": None,
            "dst_ip": None,
            "src_port": None,
            "dst_port": None,
            "protocol": None,
            "action": None}

    if pkt.haslayer(IP):
        data["src_ip"] = pkt[IP].src
        data["dst_ip"] = pkt[IP].dst
    else:
        return []
    
    if pkt.haslayer(TCP):
        data["src_port"] = pkt[TCP].sport 
        data["dst_port"] = pkt[TCP].dport 
        data["protocol"] = "TCP"

    if pkt.haslayer(UDP):
        data["src_port"] = pkt[UDP].sport 
        data["dst_port"] = pkt[UDP].dport
        data["protocol"] = "UDP" 

    return data


# TESTING

if __name__ == "__main__":
    firewall = Firewall()
    firewall.add_rule({
            "src_ip": None,
            "dst_ip": None,
            "protocol": None,
            "src_port": 443,
            "dst_port": None,
            "action": "BLOCK"})
    sniffer = PacketSniffer(firewall)
    sniffer.start()


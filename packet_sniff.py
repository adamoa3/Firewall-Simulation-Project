from PyQt6.QtCore import QObject, pyqtSignal
from scapy.all import sniff, IP, TCP, UDP
from firewall import Firewall

class PacketSniff(QObject):

    #packet_signal = pyqtSignal(dict)

    def __init__(self, firewall):
        self.firewall = firewall

    def start(self):
        super().__init__()
        sniff(prn=self.process_packet)

    def process_packet(self, pkt):
        
        # get values from packet
        data = get_packet_values(pkt)

        # ignore packet if data is empty
        if not(data):
            return

        # apply rules from firewall.py
        data["action"] = firewall.check_rules(data)

        # TESTING print data
        print(data)
        print()

        # send values + action to gui
        #packet_signal.emit(data)



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


# Test

if __name__ == "__main__":
    firewall = Firewall()
    sniffer = PacketSniff(firewall)
    sniffer.start()


from PyQt6.QtCore import QObject, pyqtSignal
from scapy.all import sniff, IP, TCP, UDP
from firewall import Firewall

class PacketSniff(QObject):

    send_packet = pyqtSignal(dict)

    def __init__(self, firewall):
        self.firewall = firewall

    def start(self):
        # run QObject initialization
        super().__init__()

        # start packet sniffing
        sniff(prn=self.process_packet)

    def process_packet(self, pkt):
        
        # get values from packet
        data = get_packet_values(pkt)
        
        # TESTING print data
        print(data)
        print()

        # apply rules from firewall.py
        data["action"] = check_rules(firewall, data)

        # send values + action to gui
        send_packet.emit(data)



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
    sniffer = PacketSniff()
    sniffer.start()


from PyQt6.QtCore import QObject, pyqtSignal
from scapy.all import sniff, IP, TCP, UDP

class PacketSniff(QObject):
    send_packet = pyqtSignal(dict)

    def start(self):
        sniff(prn=self.process_packet)

    # Processes packets, passed into sniff function
    def process_packet(self, pkt):
        
        # get values from packet
        data = get_packet_values(pkt)
        print(data)
        print()

        # apply rules from firewall.py

        # send values + action to gui


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
        #print(f"Source IP: {src_IP}\nDestination IP: {dst_IP}")
    
    if pkt.haslayer(TCP):
        data["src_port"] = pkt[TCP].sport 
        data["dst_port"] = pkt[TCP].dport 
        data["protocol"] = "TCP"
        #print(f"Source Port: {src_port}\nDestination Port: {dst_port}")

    if pkt.haslayer(UDP):
        data["src_port"] = pkt[UDP].sport 
        data["dst_port"] = pkt[UDP].dport
        data["protocol"] = "UDP" 
        #print(f"Source Port: {src_port}\nDestination Port: {dst_port}")

    return data


# Test

if __name__ == "__main__":
    sniffer = PacketSniff()
    sniffer.start()


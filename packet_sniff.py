from PyQt6.QtCore import QObject, pyqtSignal
from scapy.all import AsyncSniffer, sniff, IP, TCP, UDP, ICMP
from firewall import Firewall
from ipaddress import ip_address
from states import StateTracker

class PacketSniffer(QObject):

    packet_signal = pyqtSignal(dict)

    def __init__(self, firewall, state_tracker):
        super().__init__()
        self.sniffer = None
        self.running = False
        self.firewall = firewall
        self.state_tracker = state_tracker

    def start(self):

        print("Starting sniffer")

        self.sniffer = AsyncSniffer(prn=self.process_packet)
        self.running = True
        self.sniffer.start()

    def stop(self):

        print("Stopping sniffer")

        if self.running:
            self.sniffer.stop()
            self.running = False

    def process_packet(self, pkt):
        
        # get values from packet
        data = get_packet_values(pkt)

        # ignore packet if data is empty
        if not(data):
            return

        # check states first, if not present check firewall rules
        if self.state_tracker.in_states(data):
            # allow through
            data["action"] = "ST_PASS"
        else:
            # apply rules from firewall.py
            data["action"] = self.firewall.check_rules(data)

            # add state if packet passed
            if data["action"] == "PASS":
                self.state_tracker.add_state(data)

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
            "interface": None,
            "direction": None,
            "action": None}

    # source/destination ip
    if pkt.haslayer(IP):
        data["src_ip"] = pkt[IP].src
        data["dst_ip"] = pkt[IP].dst
    else:
        return []
    
    # tcp
    if pkt.haslayer(TCP):
        data["src_port"] = pkt[TCP].sport 
        data["dst_port"] = pkt[TCP].dport 
        data["protocol"] = "TCP"

    # udp
    if pkt.haslayer(UDP):
        data["src_port"] = pkt[UDP].sport 
        data["dst_port"] = pkt[UDP].dport
        data["protocol"] = "UDP" 

    # icmp
    if pkt.haslayer(ICMP):
        data["src_port"] = None
        data["dst_port"] = None
        data["protocol"] = "ICMP"

    # local vs internet
    if data["src_ip"] != None and ip_address(data["src_ip"]).is_private:
        data["interface"] = "LAN"
    else:
        data["interface"] = "WAN"

    # direction
    if ip_address(data["src_ip"]).is_private and not ip_address(data["dst_ip"]).is_private:
        data["direction"] = "OUTBOUND"
    elif not ip_address(data["src_ip"]).is_private and ip_address(data["dst_ip"]).is_private:
        data["direction"] = "INBOUND"
    else:
        data["direction"] = "INTERNAL"

    return data


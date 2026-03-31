from scapy.all import sniff, IP, TCP, UDP

# Processes packets, passed into sniff function
def process_packet(pkt):

    # dict that holds packet values to be later compared with firewall rules
    data = {"src_ip": None,
            "dst_ip": None,
            "src_port": None,
            "dst_port": None,
            "protocol": None,
            "blocked": False}

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

    print(data)
    print()

# Test
packets = sniff(count=10, prn=process_packet)
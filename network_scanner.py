import scapy.all as scapy
import optparse

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="target", help="Target IP address / IP range.")
    (options, arguments) = parser.parse_args()
    return options


def scan(ip):
    arp_request = scapy.ARP(pdst = ip)
    broadcast = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout = 1, verbose = False)[0]
    
    clients_list = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        clients_list.append(client_dict)
        # print(element[1].psrc+"\t\t"+element[1].hwsrc)
    return clients_list

def print_results(clients_list):
    print("IP\t\t\tMAC Address\n-----------------------------------------------------")
    for element in clients_list:
        print(element["ip"]+"\t\t"+element["mac"])

def main():
    options = get_arguments()
    scan.results = scan(options.target)
    print_results(scan.results)

if __name__ == "__main__":
    main()
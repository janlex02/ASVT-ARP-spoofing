import subprocess
import optparse
import re

def get_argumets():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest = "interface", help = "Interface to change mac")
    parser.add_option("-m", "--mac", dest = "new_mac", help = "New mac")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("Please specify an interface, use --help for more information")
    elif not options.new_mac:
        parser.error("Please specify a new mac, use --help for more information")
    return options

def get_current_mac(interface):
    ifconfig_results = subprocess.check_output(["ifconfig", interface]).decode()
    current__mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_results)
    if current__mac:
        print("[+]  Your current MAC is: " + str(current__mac.group(0)))
        return current__mac.group(0)
    else:
        print(f"[-]  Could not find MAC address of {interface} interface")
        return None

def is_valid_mac(mac):
    if re.match(r"^([0-9A-Fa-f]{2}[:]){5}([0-9A-Fa-f]{2})$", mac):
        return True
    else:
        print("[!]  You have entered an invalid MAC address")
        return False

def change_mac(interface, new_mac):
    print("[+]  Changing MAC address for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def main():
    options = get_argumets()
    if not is_valid_mac(options.new_mac):
        return
    current_mac = get_current_mac(options.interface)
    if current_mac == options.new_mac:
        print("[!]  Your MAC address is already: " + str(options.new_mac))
        return
    if current_mac == None:
        return
    change_mac(options.interface, options.new_mac)

    new_mac = get_current_mac(options.interface)
    if new_mac == options.new_mac:
        print(f"[+]  MAC has been successfully changed to {new_mac}")
    else:
        print(f"[-]  Failed to change MAC address. Current MAC is still {new_mac}")
# main()
if __name__ == "__main__":
    try:
        main()
    except:
        print("[-]  Something went wrong")

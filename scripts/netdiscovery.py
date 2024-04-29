import netifaces
import re
from nmap import PortScanner
import json
import addons.utils as utils

#########
## Utils functions
#########

def validate_ip(ip):
    pattern = re.compile(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')
    return bool(pattern.match(ip.split('/')[0]))

def get_network_info():
    # Obtenez les informations sur l'interface réseau par défaut de la machine
    interface = netifaces.gateways()['default'][netifaces.AF_INET][1]
    interface_info = netifaces.ifaddresses(interface)

    # Obtenez l'adresse IP et le masque de sous-réseau de l'interface
    ip_address = interface_info[netifaces.AF_INET][0]['addr']
    netmask = interface_info[netifaces.AF_INET][0]['netmask']
    prefix = sum(bin(int(x)).count('1') for x in netmask.split('.'))
    return {
        "ip_address": ip_address,
        "prefix": prefix
    }

#########
# Main functions
#########

def run_script(**args):
    needed_args = ["ip_address"]

    if not all(arg in args for arg in needed_args):
        raise ValueError("Missing arguments")

    ip_address = args["ip_address"]

    if 'prefix' in args:
        prefix = int(args['prefix'])
    else:
        prefix = 32

    if 'scan_vuln' in args and args['scan_vuln']:
        scan_vuln = True
    else:
        scan_vuln = False

    if 'all_ports' in args and args['all_ports']:
        all_ports = True
    else:
        all_ports = False

    if 'update_db' in args and args['update_db']:
        update_db = True
    else:
        update_db = False

    if not validate_ip(ip_address):
        raise ValueError("Invalid IP address")

    sc = PortScanner()
    result = sc.scan(ip_address +'/'+str(prefix), arguments=("-p- " if all_ports else "") + "-Pn -sV -O" + (" --script=vuln" if scan_vuln else "") + (" --script-updatedb" if update_db else ""))
    return result

def help():
    return {
        "description": "Discover network devices using nmap",
        "parameters": {
            "ip_address": {
                "description": "IP address to scan",
                "required": True,
                "type": "string",
            },
            "prefix": {
                "description": "Prefix of the IP address",
                "required": False,
                "type": "integer"
            },
            "scan_vuln": {
                "description": "Scan for vulnerabilities",
                "required": False,
                "type": "boolean"
            },
            "all_ports": {
                "description": "Scan all ports",
                "required": False,
                "type": "boolean"
            },
            "update_db": {
                "description": "Update the script database (requires root/admin privileges)",
                "required": False,
                "type": "boolean"
            }
        }
    }

def display_result(result: dict):
    print("---------------------------------------------")
    # Afficher les adresses IP scannées
    for h in result['scan']:
        print('Host : %s (%s)' % (h, result['scan'][h]['hostnames'][0]['name']))

        # Afficher la détection d'OS sur la même ligne
        if 'osmatch' in result['scan'][h]:
            print('OS Detection: %s' % ', '.join([match['name'] for match in result['scan'][h]['osmatch']]))
        else:
            print('No OS detection available')

        # Afficher les ports ouverts pour l'adresse IP actuelle avec les détails de service et d'OS
        if 'tcp' not in result['scan'][h]:
            print('Device found but No tcp port open')
        else:
            for p in result['scan'][h]['tcp'].keys():
                port_info = result['scan'][h]['tcp'][p]
                print('Port : %s\tState : %s\tService : %s\tVersion : %s' % (p, port_info['state'], port_info['name'], port_info['version']))
                vulns = []
                if 'script' in port_info:
                    for script in port_info['script']:
                        output = port_info['script'][script]
                        if "VULNERABLE:" in output:
                            vulns += re.findall(r'CVE-\d{4}-\d{4}', output)

                vulns = list(set(vulns))

                if vulns:
                    print('Vulnerabilities found : %s' % ', '.join(vulns))
                else:
                    print('No vulnerabilities found')

def format_to_table(res):
    return {
        "headers": ["IP Address", "Hostname", "OS", "Ports", "Vulnerabilities"],
        "rows": [
            [
                h,
                res['scan'][h]['hostnames'][0]['name'] if 'hostnames' in res['scan'][h] else 'N/A',
                ', '.join([match['name'] for match in res['scan'][h]['osmatch']]) if 'osmatch' in res['scan'][h] else 'N/A',
                '\n'.join(map(lambda e: str(e) + ": " + (res['scan'][h]['tcp'][e]['name'] or "unknown"), [p for p in res['scan'][h]['tcp'].keys()])) if 'tcp' in res['scan'][h] else 'N/A',
                ", ".join(set(', '.join(json.dumps(cve) for cve in filter((lambda x: x.__len__() > 0), (re.findall(r'CVE-\d{4}-\d{4}', json.dumps(res['scan'][h]['tcp'][p]['script'] if "script" in res['scan'][h]['tcp'][p] else [])) for p in res['scan'][h]['tcp']))).replace('"', '').replace('[', '').replace(']', '').split(", ")))
            ] for h in res['scan']
        ]
    }

def gui_inputs():
    return [
        {"label": "IP Address", "id": "ip_address", "type": "text"},
        {"label": "CIDR", "id": "prefix", "type": "number"},
        {"label": "Scan Vulnerabilities", "id": "scan_vuln", "type": "checkbox"},
        {"label": "Scan All Ports", "id": "all_ports", "type": "checkbox"},
        {"label": "Update Script Database (requires root/admin privileges)", "id": "update_db", "type": "checkbox"}
    ]

def additional_functions():
    return {
        "validate_ip": validate_ip,
        "get_network_info": get_network_info
    }

#########
# Test function
#########

def main():
    res = run_script(ip_address='10.33.52.21', prefix=32, scan_vuln=False)
    display_result(res)

if __name__ == '__main__':
    main()
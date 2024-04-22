import netifaces
import re
from nmap import PortScanner

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
        prefix = args['prefix']
    else:
        prefix = 32

    if 'scan_vuln' in args:
        scan_vuln = args['scan_vuln']
    else:
        scan_vuln = False

    if not validate_ip(ip_address):
        raise ValueError("Invalid IP address")

    sc = PortScanner()
    result = sc.scan(ip_address +'/'+str(prefix), arguments="-Pn -sV -O" + (" --script=vuln" if scan_vuln else ""))
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
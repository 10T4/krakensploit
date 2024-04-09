import nmap
import netifaces
import re

def print_author_info():
    print("---{Author : 1OTA & Ibaraki Douji}-----------")

def validate_ip(ip):
    pattern = re.compile(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')
    return bool(pattern.match(ip))

def scan_network_devices_and_services():
    # Obtenez les informations sur l'interface réseau par défaut de la machine
    interface = netifaces.gateways()['default'][netifaces.AF_INET][1]
    interface_info = netifaces.ifaddresses(interface)

    # Obtenez l'adresse IP et le masque de sous-réseau de l'interface
    ip_address = interface_info[netifaces.AF_INET][0]['addr']
    netmask = interface_info[netifaces.AF_INET][0]['netmask']
    prefix = sum(bin(int(x)).count('1') for x in netmask.split('.'))
    print("---------------------------------------------")
    print('your Network : ',ip_address +'/'+str(prefix))
    print("---------------------------------------------")

    # Scanner to all network where is actually device
    sc = nmap.PortScanner()
    sc.scan(ip_address +'/'+str(prefix))

    # Afficher les adresses IP scannées
    for h in sc.all_hosts():
        print("---------------------------------------------")
        print('Host : %s (%s)' % (h, sc[h].hostname() or "Unknown"))

        # Afficher les ports ouverts pour l'adresse IP actuelle
        if 'tcp' not in sc[h]:
            print('No open ports found')
        else :
            for p in sc[h]['tcp'].keys():
                print('Port : %s\tState : %s' % (p, sc[h]['tcp'][p]['state']))

def scan_specific_ip(ip):
    np = nmap.PortScanner()
    np.scan(ip, arguments="-Pn -sV -O")  # Ajout de -O pour la détection d'OS

    # Afficher les adresses IP scannées
    for h in np.all_hosts():
        print("---------------------------------------------")
        print('Host : %s (%s)' % (h, np[h].hostname() or h))
        
        # Afficher la détection d'OS sur la même ligne
        if 'osmatch' in np[h]:
            print('OS Detection: %s' % ', '.join([match['name'] for match in np[h]['osmatch']]))
        else:
            print('No OS detection available')

        # Afficher les ports ouverts pour l'adresse IP actuelle avec les détails de service et d'OS
        if 'tcp' not in np[h]:
            print('Device found but No tcp port open')
        else:
            for p in np[h]['tcp'].keys():
                port_info = np[h]['tcp'][p]
                print('Port : %s\tState : %s\tService : %s\tVersion : %s' % (p, port_info['state'], port_info['product'], port_info['version']))

print('Tool to scan and exploit your network and service !')
print_author_info()

while True:  # boucle pour continuer l'exécution jusqu'à ce que l'utilisateur choisisse de quitter
    print("-----------{Main Menu}-----------")
    print('1 - Scan your network devices and services')
    print('2 - Directory web page discovery')
    print('3 - Quit')
    print("---------------------------------------------")

    resp = input('Enter the number: ')

    if resp == '1':
        while True:  # boucle pour continuer l'exécution jusqu'à ce que l'utilisateur choisisse de revenir au menu principal*
            print("-----------{Scan Menu}-----------")
            print('Do you want to scan the entire network or a specific IP?')
            print('1 - Scan entire network')
            print('2 - Scan specific IP')
            print('0 - Back to main menu')
            print("---------------------------------------------")

            sub_resp = input('Enter the number: ')
            
            if sub_resp == '1':
                scan_network_devices_and_services()
            elif sub_resp == '2':
                print("---------------------------------------------")
                scnet = input('Enter the target IP address: ')
                if validate_ip(scnet):
                    scan_specific_ip(scnet)
                else:
                    print("Invalid IP address format.")
            elif sub_resp == '0':
                break  # sortir de la boucle pour revenir au menu principal
            else:
                print("Invalid input. Please enter a valid option.")
    elif resp == '2':
        # code pour la découverte des pages web
        pass
    elif resp == '3':
        print("Exiting the program.")
        break  # sortir de la boucle et donc terminer le programme
    else:
        print("Invalid input. Please enter a valid option.")

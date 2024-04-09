import nmap
import netifaces
import re
import json

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


#Scanner to all network where is actually device
def scallnet():
    sc = nmap.PortScanner()
    sc.scan(ip_address +'/'+str(prefix))

    # Afficher les adresses IP scannées
    for h in sc.all_hosts():
        print("---------------------------------------------")
        print('Host : %s (%s)' % (h, sc[h].hostname()))

    # Afficher les ports ouverts pour l'adresse IP actuelle
        if 'tcp' not in sc[h]:
            print ('Not Devices Found')
        else :
            for p in sc[h]['tcp'].keys():
                print('Port : %s\tState : %s' % (p, sc[h]['tcp'][p]['state']))

#def scspefnet():
# Fonction pour valider l'entrée de l'utilisateur
def validate_ip(ip):
    pattern = re.compile(r'^[1-9]\.[0-9]\.[0-9]\.[-9]$')
    return bool(pattern.match(ip))

scnet = input('scan target ip: ')

np = nmap.PortScanner()
np.scan(scnet, arguments="-Pn -sV -O")  # Ajout de -O pour la détection d'OS

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





 

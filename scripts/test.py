import requests
import re

def search_credentials(url, liste_mots):
    try:
        # Récupérer le contenu de la page HTTP
        response = requests.get(url)
        content = response.text

        # Boucler à travers la liste des mots et les rechercher dans le contenu de la page
        for mot in liste_mots:
            if re.search(r'\b' + re.escape(mot) + r'\b', content, re.IGNORECASE):
                print(f"Mot '{mot}' trouvé dans le contenu de la page:")
                print(content)
    
    except requests.RequestException as e:
        print("Une erreur s'est produite lors de la récupération de la page:", e)

# Fonction pour lire la liste de mots à partir d'un fichier texte
def lire_liste_mots(nom_fichier):
    with open(nom_fichier, "r") as f:
        return f.read().splitlines()

# Exemple d'utilisation
url = "http://172.20.10.4/robots.txt"  # Remplacez par l'URL de la page que vous souhaitez parcourir
liste_mots = lire_liste_mots("liste_mots.txt")  # Remplacez "liste_mots.txt" par le nom de votre fichier de mots
search_credentials(url, liste_mots)

import requests
import re

def search_credentials(url, mots_fichier):
    try:
        # Récupérer le contenu de la page HTTP
        response = requests.get(url)
        content = response.text

        # Charger les mots depuis le fichier
        with open(mots_fichier, 'r', encoding='utf-8') as file:
            mots = [mot.strip() for mot in file.readlines()]

        # Recherche des lignes contenant les mots dans le contenu de la page
        lines = content.split('\n')
        for line in lines:
            for mot in mots:
                if re.search(r'\b' + re.escape(mot) + r'\b', line, re.IGNORECASE):
                    print(f"Ligne contenant '{mot}' trouvée:")
                    print(line)
                    break  # Sortir de la boucle une fois qu'un mot est trouvé

    except requests.RequestException as e:
        print("Une erreur s'est produite lors de la récupération de la page:", e)

# Exemple d'utilisation
url = "http://172.20.10.4/robots.txt"  # Remplacez par l'URL de la page que vous souhaitez parcourir
fichier_mots = "user.txt"  # Remplacez par le chemin de votre fichier contenant la liste de mots
search_credentials(url, fichier_mots)

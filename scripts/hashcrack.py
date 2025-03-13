import hashlib
import os
import re

#########
## Utils functions
#########

HASH_TYPES = {
    32: ["MD5", "NTLM"],
    40: ["SHA-1"],
    56: ["SHA-224"],
    64: ["SHA-256"],
    96: ["SHA-384"],
    128: ["SHA-512"],
    16: ["MySQL 323"],
    13: ["DES Unix"],
    34: ["CRC-32"],
    60: ["bcrypt"],
    98: ["SHA-512 Crypt"],
}

HEX_PATTERN = re.compile(r"^[0-9a-fA-F]+$")


def get_default_wordlist():
    """
    Vérifie si le fichier rockyou.txt est présent dans le répertoire word_list du projet.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    wordlist_path = os.path.join(script_dir, "..", "word_lists", "rockyou.txt")
    print(f"Chemin recherchée : {wordlist_path}")

    return wordlist_path if os.path.exists(wordlist_path) else None

def detect_hash_type(hash_str):
    """
    Détecte le type de hash en fonction de sa longueur et de son format.
    """
    length = len(hash_str)
    possible_types = HASH_TYPES.get(length, ["Unknown"])

    if HEX_PATTERN.match(hash_str):
        return possible_types
    else:
        return ["bcrypt"] if length == 60 else ["Unknown"]


def hash_word(word, hash_type):
    """
    Hache un mot donné avec l'algorithme spécifié.
    """
    hash_func = {
        "MD5": hashlib.md5,
        "SHA-1": hashlib.sha1,
        "SHA-256": hashlib.sha256,
        "SHA-512": hashlib.sha512
    }.get(hash_type)

    return hash_func(word.encode()).hexdigest() if hash_func else None


def crack_hash(hash_str, hash_type, wordlist_path):
    if not wordlist_path or not os.path.exists(wordlist_path):
        return None

    print(f"🔍 CRACKING THIS HASH: {hash_str} ({hash_type}) | WORDLIST: {wordlist_path}...")

    try:
        with open(wordlist_path, "r", encoding="latin-1") as file:
            for line in file:
                password = line.strip()
                hashed_password = hash_word(password, hash_type)

                if hashed_password == hash_str:
                    return password

        print("❌ HASH NOT CRACKED !")
    except Exception as e:
        None
    return None

#########
# Main functions
#########

def run_script(**args):
    if "hash" not in args:
        raise ValueError("Missing required argument: 'hash'")

    hash_input = args["hash"].strip()
    detected_types = detect_hash_type(hash_input)

    result = {
        "hash": hash_input,
        "detected_types": detected_types
    }

    if args.get("crack", False):
        wordlist_path = args.get("wordlist") or get_default_wordlist()

        if not wordlist_path:
            return result

        for hash_type in detected_types:
            if hash_type in ["MD5", "SHA-1", "SHA-256", "SHA-512"]:
                cracked_password = crack_hash(hash_input, hash_type, wordlist_path)
                if cracked_password:
                    result["cracked_password"] = cracked_password
                    break 

    return result


def help():
    return {
        "description": "This script is used to detect and crack hash types.",
        "parameters": {
            "hash": {
                "description": "The hash to analyze",
                "required": True,
                "type": "string"
            },
            "crack": {
                "description": "Enable hash cracking mode",
                "required": False,
                "type": "boolean"
            },
            "wordlist": {
                "description": "Custom wordlist file for cracking",
                "required": False,
                "type": "string"
            }
        }
    }


def gui_inputs():
    return [
        {"label": "Hash", "id": "hash", "type": "text"},
        {"label": "Enable cracking", "id": "crack", "type": "checkbox"},
        {"label": "Wordlist (optional)", "id": "wordlist", "type": "file"}
    ]


def display_result(result):
    print(f"📌 Hash: {result['hash']}")
    print(f"🔍 Hash type: {', '.join(result['detected_types'])}")

    if "cracked_password" in result:
        print(f"✅ PASSWORD FOUND: {result['cracked_password']}")
    else:
        print("❌ NOT PASSWORD FOUND")


def format_to_table(res):
    return {
        "headers": ["Hash", "Detected Types", "Cracked Password"],
        "rows": [[res["hash"], ", ".join(res["detected_types"]), res.get("cracked_password", "Not found")]]
    }


def additional_functions():
    return {}

#########
# Test function
#########

def main():
    res = run_script(hash="", crack=True)
    display_result(res)


if __name__ == '__main__':
    main()
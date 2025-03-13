import argparse
import os
import time
from krakensploit.addons.scriptManager import scripts

import time

import time

def loading_effect():
    purple = "\033[95m"
    blue = "\033[94m"
    brown = "\033[33m"
    reset = "\033[0m"
    
    lines = [
        "                              @-                              ",
        "                          **------+@                          ",
        "                     =------------------=                     ",
        "                 @-----------@@@@-----------@                 ",
        "               ---------=@@@@@@@@@@@@----------               ",
        "             -----------@@@@@@@@@@@@@@-----------@            ",
        "           =-----------@@@@@@@@@@@@@@@@------------           ",
        "         @------------=@-@@@@@@@@@@@@-@-------------+         ",
        "        -----------=---@*-@@@@@@@@@@=-@----=----------        ",
        "       ----------@@%@---@@@#@@@@@@*@@@=-#@%@@----------       ",
        "      -----------@--==--@#---@@@@=--*@--@---@=----------      ",
        "     =-----@@+@+=@@------@@@@@@@@@@@@------@@=#@=@@------     ",
        "     ------@---@-=@@@----@@@@@@@@@@@@----@@@--@---@------     ",
        "    -------@@-----=-@@@@@@@@@@@@@@@@@@@@@@-------@@-------    ",
        "    ---------@@@+---=@@@@@@@@@@@@@@@@@@@@=----@@@---------    ",
        "    -----@@@@=--*@@@@+@@@@@=@@@@=@=@@@@@=@@@@+---@@@@-----    ",
        "   @-----@---@----@@@@@-@@=@@-@@-@@=@@=@@@@@----@---@=----@   ",
        "   @-----@@@@@-@@@+=--@@@-@@=-@@==@@=@@@--=@@@+-@@@@@-----@   ",
        "    ----------==----=-=-------===-------------------------    ",
        "    ---------@@@@@@-@@-@@@@@@@@@@-@@@@@-@@@@@@@@----------    ",
        "    ---------@@@@@@=@@-@@@@@@@@@@+@@@@@-@@@@@@@@----------    ",
        "     --------@@-=@@-@@=@@@@@@@@*@+@@@@@-@@@@@-@@=--------     ",
        "     #--------@@@@@=+@-@@@@@-+@*=-@@@@@-@@+-@@@---------#     ",
        "      --------@@=@@*=--@@@@@-@@@@-@@@@@-@-@@@@@=--------      ",
        "       -------@@=@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@=-------       ",
        "        ------@@=@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@=------        ",
        "         @----@@=@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@=---=@         ",
        "           ---@@-@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@=---           ",
        "             -@@@==-------------------------@@@--             ",
        "               =@@@@@@@@@@@@@@@@@@@@@@@@@@@=@@-               ",
        "                 @--------------------------@                 ",
        "                     --------------------                     ",
        "                          @--------@                          ",
        "                              @-                              "
    ]
    
    for line in lines:
        colored_line = ""
        for char in line:
            if char == "@":
                if lines.index(line) < 18:
                    colored_line += purple + char + reset
                else:
                    colored_line += brown + char + reset
            elif char == "-":
                colored_line += blue + char + reset
            else:
                colored_line += char
        print(colored_line)
        time.sleep(0.03)

loading_effect()

def parse_args():
    parser = argparse.ArgumentParser(description='Kraken CLI')
    parser.add_help = False

    parser.add_argument("script", type=str, help="The script to run")
    parser.add_argument("args", nargs=argparse.REMAINDER, help="Arguments to pass to the script")

    return parser.parse_args()

def main():
    args = parse_args()
    
    if not args.script in scripts:
        print("Invalid script")
        return
    
    script = scripts[args.script]

    if "--help" in args.args:
        help = script.help()

        sParam = ""

        for param in help['parameters']:
            paramInfo = help['parameters'][param]
            sParam += " --" + param
            if paramInfo['type'] != "bool":
                if paramInfo['required']:
                    sParam += "=<" + paramInfo['type'] + ">"
                else:
                    sParam += "=[" + paramInfo['type'] + "]"

        print("Usage: " + os.path.basename(__file__) + " " + args.script + sParam)
        print()
        print("Description: " + help['description'])
        print()
        print("Parameters:")
        for param in help['parameters']:
            paramInfo = help['parameters'][param]
            print("  " + param + " (" + paramInfo['type'] + "): " + paramInfo['description'])

        return
    
    argsDict = {}
    for arg in args.args:
        if "=" in arg:
            key, value = arg.split("=")
            argsDict[key.split("--")[1]] = value
        else:
            argsDict[arg.split("--")[1]] = True

    res = script.run_script(**argsDict)
    script.display_result(res)


if __name__ == "__main__":
    main()

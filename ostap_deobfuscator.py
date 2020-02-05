#! /usr/bin/python3
# Ostap deobfuscator feb-2020
# Use raw JSE file (not beautified) as parameter

import re
import sys

try:
    import jsbeautifier
    beautify = True
except ModuleNotFoundError:
    beautify = False


def rep_func(matchobj):
    int_1 = int(matchobj.group(1))
    int_2 = int(matchobj.group(2))
    char = chr(abs(int_2 - int_1))

    if char == '"':
        char = '\\"'
    cad = '"{}"'.format(char)

    return cad


if __name__ == "__main__":
    
    if len(sys.argv) != 2:
        print("Give me the Ostap JSE file as a parameter")
        exit(1)

    in_path = sys.argv[1]
    out_path = in_path + "_deobf.js"

    with open(in_path, "r") as fd:
        buff = fd.read()

    raw_patt = r"\(function\(\w+(?:\,\w+)?\){.*?]=(\d+);\s?.*?]=(\d+);.*?}\)\(.*?\)"
    compiled = re.compile(raw_patt)

    if not compiled.search(buff):
        print("[-] Sorry, I can't deobfuscate this script :(")
        exit(1)

    buff = compiled.sub(rep_func, buff)
    buff = buff.replace("'+'", "")
    buff = buff.replace('"+"', "")

    print("[+] Deobfuscation OK")

    # Dump code
    with open(out_path, "w") as fd:
        if beautify:
            buff = jsbeautifier.beautify(buff)

        fd.write(buff)

    if not beautify:
        print("[!] I couldn't beautify the code for you (pip install jsbeautifier?)")
        print("[i] Now you should beautify it:\n\thttps://beautifier.io/\n\thttps://www.npmjs.com/package/js-beautify")

    print("[i] Check {} file!".format(out_path))

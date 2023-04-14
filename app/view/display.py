#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import msvcrt

display_width = 60

def show_menu(menu,msg=""):
    os.system("cls")
    print(f"\n--- {md.BOLD}" + menu['title'].upper() + f"{md.END} " + "-"*(display_width-8-len(menu['title'].upper())) + "---")
    
    for option_field in menu['fields']:
        if option_field['title'] != "":
            print(f"\n   {md.UNDERLINE + md.BOLD}"+option_field['title']+f"{md.END}")
        else:
            print("")

        if option_field['text'] != "":
            print("   "+option_field['text'] + f"{md.END}")

        for option in option_field['option']:
            if option['name'] != "" or option['key'] != "":
                if len(option['key']) > 1 and not option['key'].isdigit():
                    print(f"   {md.BOLD}{option['key']}{md.END}: {option['name']}{md.END}")
                else:
                    print(f"   {option['key']}. {option['name']}{md.END}")

    print("\n"+"-"*display_width)
    if msg != "":
        print(f"{msg}{md.END}")
    else:
        print("")

def text_input(msg=""):
    print(msg, end="", flush=True)
    return input()

def choice_input(msg=""):
    print(msg, end="", flush=True)
    try:
        user_input = msvcrt.getch()
        return user_input.decode()
    except:
        return ""

def secret_input(msg=""):
    print(msg, end="", flush=True)  # affiche le message sans saut de ligne
    hidden_input = ""
    while True:
        key = msvcrt.getch()  # lit un caractère à partir du clavier
        if key == b'\r':  # si on appuie sur "Entrée"
            print()  # affiche un saut de ligne
            return hidden_input
        elif key == b'\x08':  # si on appuie sur "Retour arrière"
            if hidden_input:
                hidden_input = hidden_input[:-1]
                print('\b \b', end='', flush=True)  # efface le caractère précédent
        else:
            hidden_input += key.decode()  # ajoute le caractère saisi au mot de passe
            print('*', end='', flush=True)  # affiche un astérisque


def dprint(string, offset=0, width=0):
    words = string.split(' ')
    result = []
    current = ''
    for word in words:
        if len(current) + len(word) + 1 <= width:
            if current == '':
                current = word
            else:
                current += ' ' + word
        else:
            result.append(current)
            current = word
    result.append(current)
    for line in result:
        print(" "*offset+line)

class md:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    GREY = '\033[235m'
    DARKGREY = '\033[240m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
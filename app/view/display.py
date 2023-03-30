#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import msvcrt

def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def show_menu(menu,msg="",input_text="",hide_input=False):
    try:
        clear()
        print("\n=== " + "\033[1m" + menu['title'].upper() + "\033[0m " + "="*(65-len(menu['title'].upper())))
        
        for option_field in menu['corps']:
            if option_field['title'] != "":
                print("\n\033[1m   "+option_field['title']+"\033[0m")
            else:
                print("")

            if option_field['text'] != "":
                print("\033[3m   "+option_field['text']+"\033[0m\n")

            for option in option_field['option']:
                print(f"   {option['key']}. {option['name']}")

        print("\n"+"-"*70)
        if msg != "":
            print(f"{msg}")
        else:
            print("")

    except KeyError:
        print("Menu error")


def wait_input(prompt="", hide=False):
    if hide:
        print(prompt, end="", flush=True)  # affiche le prompt sans saut de ligne
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
    else:
        return input(prompt)
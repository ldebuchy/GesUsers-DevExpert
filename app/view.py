#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import controller

def start_menu():
    print("Bienvenue sur le gestionaire d'utilisateurs")
    print("1. Créer un utilisateur")
    print("2. Obtenire une information sur un utilisateur")
    print("3. Supprimer un utilisateur")
    user_input = input("Que voulez-vous faire ? ")
    if user_input == "1":
        controller.model.create_user()
    if user_input == "2":
        a = controller.model.get_user(101)
    if user_input == "3":
        controller.model.delete_user()

start_menu()
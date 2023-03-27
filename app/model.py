#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys
import pickle



# Création de la classe User
class User():
    def __init__(self, user_name, first_name, last_name, password, role=[]):
        self.id = 0
        self.user_name = user_name
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.suspended = False
        self.role = []

user_list = {}

# Création de deux utilisateurs
jhon = User("jdoe", "Jhon", "Doe", "123456")
mike = User("msirus", "Mike", "Sirus", "123456")

# Ajout des utilisateurs à la liste
user_list.append(jhon)
user_list.append(mike)
user_list = {"100": jhon,"101": mike}

# export des données dans le fichier users.pickle
with open("users.pickle", "wb") as file:
    pickle.dump(user_list, file)

# import des données depuis le fichier users.pickle
with open("users.pickle", "rb") as file:
    user_list = pickle.load(file)

# Affichage des données
try:
    print(user_list["101"].last_name)
except:
    print("User not found")
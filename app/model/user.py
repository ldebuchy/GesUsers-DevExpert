#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys
from random import randint

import pickle
import hashlib
sys.path.insert(1, f'{os.path.dirname(__file__)}/../../data')

super_admin_id = 490

#fonction de hash pour mdp
def hash_password(password):
    salt="chaine aleatoire"
    hashed_password=hashlib.sha256((password+salt).encode()).hexdigest() #sha256() s'attend a recevoir des bytes alors on  utilise encode() qui permet de convertir le string en bytes
    return hashed_password                                              # on utilise ensuite hexidigest qui permet de convertir le binaire en hexadecimal

# export des données dans le fichier users.pickl
def export_users(data):
    with open("data/users.pickle", "wb") as file:
        pickle.dump(data, file)

# import des données depuis le fichier users.pickle
def import_users():
    with open("data/users.pickle", "rb") as file:
        return pickle.load(file)

class User():
    def __init__(self, first_name, last_name, password):
        self.id = randint(100, 999)
        while self.id in import_users():
            self.id = randint(100, 999)
        self.user_name = first_name[0].lower() + last_name.lower()
        i = 0
        while self.user_name in import_users():
            self.user_name = first_name[0].lower() + last_name.lower() + str(i)
            i += 1
        self.password = hash_password(password)
        self.first_name = first_name
        self.last_name = last_name
        self.suspended = False
        self.role = []
        self.login_attempts=0
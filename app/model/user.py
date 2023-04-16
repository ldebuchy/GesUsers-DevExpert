#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys
from random import randint

import pickle
import hashlib
sys.path.insert(1, f'{os.path.dirname(__file__)}/../../data')

super_admin_id = 490

# export des données dans le fichier users.pickle
def export_users(data):
    with open("data/users.pickle", "wb") as file:
        pickle.dump(data, file)

# import des données depuis le fichier users.pickle
def import_users():
    with open("data/users.pickle", "rb") as file:
        return pickle.load(file)

class User():
    def __init__(self):
        self.id = None
        self.user_name = None
        self.password = None
        self.first_name = None
        self.last_name = None
        self.suspended = False
        self.login_attempts=0
        self.role = []

    def save(self):
        users = import_users()
        users.update({self.id: self})
        export_users(users)


    def generate_id(self):
        self.id = randint(100, 999)
        while self.id in import_users():
            self.id = randint(100, 999)
        return self.id

    def generate_username(self):
        self.user_name = self.first_name[0].lower() + self.last_name.lower()
        i = 0
        while self.user_name in import_users():
            self.user_name = self.first_name[0].lower() + self.last_name.lower() + str(i)
            i += 1
        return self.user_name
    
    def set_password(self, password):
        self.password = self.hash_password(password)
        self.save()

    def add_role(self, role):
        if role not in self.role:
            self.role.append(role)
        self.save()

    def remove_role(self, role):
        if role in self.role:
            self.role.remove(role)
        self.save()

    def edit_first_name(self, first_name):
        self.first_name = first_name
        self.save()

    def edit_last_name(self, last_name):
        self.last_name = last_name
        self.save()

    def suspend(self):
        self.suspended = True
        self.save()

    def unsuspend(self):
        self.suspended = False
        self.save()

    def delete(self):
        users = import_users()
        del users[self.id]
        export_users(users)

    #fonction de hash pour mdp
    def hash_password(self, password):
        salt="chaine aleatoire"
        hashed_password=hashlib.sha256((password+salt).encode()).hexdigest() #sha256() s'attend a recevoir des bytes alors on  utilise encode() qui permet de convertir le string en bytes
        return hashed_password                                              # on utilise ensuite hexidigest qui permet de convertir le binaire en hexadecimal
    
    def check_password(self, password):
        return self.password == self.hash_password(password)
    
def create_user(first_name, last_name, password):
    user = User()
    user.generate_id()
    user.edit_first_name(first_name)
    user.edit_last_name(last_name)
    user.generate_username()
    user.set_password(password)
    user.save()
    return user
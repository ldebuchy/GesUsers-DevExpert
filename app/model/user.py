#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys
from random import randint

import pickle
import hashlib
sys.path.insert(1, f'{os.path.dirname(__file__)}/../../data')

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
    def __init__(self, first_name, last_name, password, role=[],):
        self.id = randint(100, 999)
        while self.id in import_users():
            self.id = randint(100, 999)
        self.user_name = first_name[0] + last_name
        self.password = hash_password(password)
        self.first_name = first_name
        self.last_name = last_name
        self.suspended = False
        self.role = role
        self.login_attempts=0

    def get(self, var):
        if var =="user_name":
            return self.user_name
        elif var =="first_name":
            return self.first_name
        elif var =="last_name":
            return self.last_name
        elif var =="suspended":
            return self.suspended
        elif var =="role":
            return self.role

def create_user(first_name, last_name, password, role):
    if "create_user" not in role.permissions:
        return "Error: User does not have permission to create user."
    new_user = User(first_name, last_name, password, role)
    users = import_users()
    users.update({new_user.id: new_user})
    export_users(users)

def delete_user(user_id, role):
    if "delete_user" not in role.permissions:
        return "Error: User does not have permission to delete user."
    users = import_users()
    try:
        users.pop(user_id)
        export_users(users)
    except KeyError:
        pass

def suspend_user(user_id, role):
    if "suspend_user" not in role.permissions:
        return "Error: User does not have permission to suspend user."
    users = import_users()
    try:
        user = users[user_id]
        user.suspended = True
        export_users(users)
    except KeyError:
        pass

def check_permission(self, permission):
        if self.role is not None:
            return permission in self.role.permissions
        else:
            return False 
#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys
from random import randint

import pickle

sys.path.insert(1, f'{os.path.dirname(__file__)}/../../data')


# export des données dans le fichier users.pickl
def export_users(data):
    with open("data/users.pickle", "wb") as file:
        pickle.dump(data, file)

# import des données depuis le fichier users.pickle
def import_users():
    with open("data/users.pickle", "rb") as file:
        return pickle.load(file)

class User():
    def __init__(self, user_name, first_name, last_name, password):
        self.id = randint(100, 999)
        while self.id in import_users():
            self.id = randint(100, 999)
        self.user_name = user_name
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.suspended = False
        self.role = []

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

def create_user(user_name, first_name, last_name, password):
    new_user = User(user_name, first_name, last_name, password)
    users = import_users()
    users.update({new_user.id: new_user})
    export_users(users)

def delete_user(user_id):
    users = import_users()
    try:
        users.pop(user_id)
        export_users(users)
    except KeyError:
        pass
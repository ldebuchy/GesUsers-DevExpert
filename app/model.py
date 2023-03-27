#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pickle

# export des données dans le fichier users.pickl
def export_users(data):
    with open("users.pickle", "wb") as file:
        pickle.dump(data, file)

# import des données depuis le fichier users.pickle
def import_users():
    with open("users.pickle", "rb") as file:
        return pickle.load(file)

class User():
    def __init__(self, user_name, first_name, last_name, password, role=[]):
        self.id = 0
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
        
def get_user(id):
    return import_users()[str(id)]

def create_user(user_id,user_name,first_name,last_name,password):
        import_users().update({f"{user_id}":User(user_name,first_name,last_name,password)})

def delete_user(user_id):
    import_users().pop(f"{user_id}")
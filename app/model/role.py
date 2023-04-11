#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys
from random import randint

import pickle

sys.path.insert(1, f'{os.path.dirname(__file__)}/../../data')

# export des données dans le fichier roles.pickl
def export_roles(data):
    with open("data/roles.pickle", "wb") as file:
        pickle.dump(data, file)

# import des données depuis le fichier roles.pickle
def import_roles():
    with open("data/roles.pickle", "rb") as file:
        return pickle.load(file)

class Role():
    def __init__(self, name, priority, permissions=[]):
        # Trouve un id unique au role
        self.id = randint(100, 999)
        while self.id in import_roles():
            self.id = randint(100, 999)

        self.name = name  # Nom du role
        # Priorité (plus le nombre est petit plus le role à d'autorité.
        self.priority = priority

        ### Liste des permissions du role ###

        # permissions d'outrepasser toutes restrictions (à utiliser avec précaution)
        self.administrator = "administrator" in permissions

        # permission de crée, gérer et supprimer des roles
        self.manage_roles = "manage_roles" in permissions  # *

        # permissions de gérer les comptes
        self.creat_delete_user = "create_delete_user" in permissions
        self.edit_user_names = "edit_user_names" in permissions  # *
        self.reset_passwords = "reset_passwords" in permissions  # *
        self.edit_names = "edit_names" in permissions  # *
        self.suspended = "suspended" in permissions  # *

        # permissions pour gérer les documents
        self.creat_delete_documents = "create_delete_documents" in permissions
        self.read_documents = "read_documents" in permissions
        self.edit_documents = "edit_documents" in permissions

        # permissions de modifier son compte
        self.edit_account = "edit_account" in permissions

        '''
        précision sur les permissions:
        #* = Effectife uniquement si la priorité du role est structement supérieur au role ou role de l'utilisateur ciblé
        '''

def create_role(name, priority, permissions):
    new_role = Role(name, priority, permissions)
    roles = import_roles()
    roles.update({new_role.id: new_role})
    export_roles(roles)

def delete_role(role_id):
    roles = import_roles()
    try:
        roles.pop(role_id)
        export_roles(roles)
    except KeyError:
        return "Error: Role does not exist."

# admin = Role("admin", 0, ["administrator"])
# hrm = Role("hrm", 20, ["manage_roles", "create_delete_user", "edit_user_names", "reset_passwords", "edit_names", "suspended", "create_delete_documents", "read_documents", "edit_documents", "edit_account"])
# team_leader = Role("manager", 40, ["edit_user_names", "reset_passwords", "edit_names", "create_delete_documents", "read_documents", "edit_documents", "edit_account"])
# employee = Role("employee", 80, ["create_delete_documents", "read_documents", "edit_documents", "edit_account"])
# internship = Role("internship", 90, ["read_documents"])
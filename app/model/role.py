#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys
import pickle
from random import randint
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
    def __init__(self, name, priority):
        # Trouve un id unique au role
        self.id = randint(100, 999)
        while self.id in import_roles():
            self.id = randint(100, 999)

        self.name = name  # Nom du role
        # Priorité (plus le nombre est petit plus le role à d'autorité.
        self.priority = priority

        ### Liste des permissions du role ###

        # permissions d'outrepasser toutes restrictions (à utiliser avec précaution)
        self.administrator = False

        # permission de crée, gérer et supprimer des roles
        self.manage_roles = False  # *

        # permissions de gérer les comptes
        self.creat_delete_user = False
        self.edit_user_names = False  # *
        self.reset_passwords = False  # *
        self.edit_names = False  # *
        self.suspended = False  # *

        # permissions pour gérer les documents
        self.creat_delete_documents = False
        self.read_documents = False
        self.edit_documents = False

        # permissions de modifier son compte
        self.edit_account = False

        '''
        précision sur les permissions:
        #* = Effectife uniquement si la priorité du role est structement supérieur au role ou role de l'utilisateur ciblé
        '''

# Fonctions de gestion des roles

# modifie un role
def edit_role(role_id, name="", priority=-1, permissions=[]):
    roles = import_roles()
    try:
        if name != "":
            roles[role_id].name = name
        if priority != "":
            roles[role_id].priority = priority
        if permissions != []:
            roles[role_id].permissions = permissions
        export_roles(roles)
    except KeyError:
        return "Error: Role does not exist."

# Crée un nouveau role
def create_role(name, priority, permissions):
    new_role = Role(name, priority, permissions)
    roles = import_roles()
    roles.update({new_role.id: new_role})
    export_roles(roles)

# Supprime un role
def delete_role(role_id):
    roles = import_roles()
    try:
        roles.pop(role_id)
        export_roles(roles)
    except KeyError:
        return "Error: Role does not exist."
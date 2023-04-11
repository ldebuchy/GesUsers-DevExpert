#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys
sys.path.insert(1, f'{os.path.dirname(__file__)}/../../app')
import model.user as user_data
import model.role as role_data

# Fonction qui retourne un dictionnaire contenant les informations d'un utilisateur
def get_user(id):
    return convert_user_to_dict(user_data.import_users()[id])

# Fonction qui retourne un dictionnaire contenant tous les utilisateurs et leurs informations
def get_user_list():
    users = user_data.import_users()
    user_list = {}

    for user in users:
        user_list.update({users[user].id: convert_user_to_dict(users[user])})
        
    return user_list

# Fonction qui convertie un objet User en dictionnaire
def convert_user_to_dict(user):
    return {
        "id": user.id,
        "user_name": user.user_name,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "suspended": user.suspended,
        "role": user.role
    }


def get_role_list():
    roles = role_data.import_roles()
    role_list = {}

    for role in roles:
        role_list.update({roles[role].id: convert_role_to_dict(roles[role])})
        
    return role_list

def convert_role_to_dict(role):
    return {
        "id": role.id,
        "name": role.name,
        "admin": role.admin,
        "manage_roles": role.manage_roles,
        
    }